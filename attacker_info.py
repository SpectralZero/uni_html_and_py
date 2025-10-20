"""
attacker_info_logger.py — Collect rich host/network metadata after a failed login attempt
------------------------------------------------------------------------------
* Cross‑platform (Windows / macOS / Linux) - uses only stdlib + psutil + requests
* Outputs one JSON object per line (JSON‑Lines) so logs can be streamed/ingested
* Captures: timestamp (UTC & local), public IP, local IPs, MACs, hostname, user,
  OS/arch, default gateway, and optional geolocation (City/Region/Country, ASN).
* Hardens storage with SHA‑256 integrity tag + optional AES‑GCM encryption hook.
* Gracefully degrades when offline or when interfaces are down; never crashes.
* Designed to be imported OR executed as a CLI tool.

Example usage:
    from attacker_info_logger import collect_attacker_info, save_json_log
    info = collect_attacker_info()
    save_json_log(info)

Auther : SpectralZero    
"""
from __future__ import annotations

import json, os, socket, platform, datetime, hashlib, logging, pathlib
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Tuple, Optional

import getpass, uuid, psutil, requests

# ─────────────────────────── configuration ────────────────────────────
LOG_DIR = pathlib.Path(__file__).with_name(pathlib.Path(__file__).stem + "_logs")
LOG_DIR.mkdir(exist_ok=True)
TIME_FMT          = "%Y-%m-%dT%H:%M:%S.%fZ"   # ISO‑8601‑R w/ milliseconds
PUBLIC_IP_SVC     = [
    "https://api.ipify.org?format=json",
    "https://ifconfig.me/ip",
]
GEO_IP_SVC        = "https://ipinfo.io/{ip}/json"
VERIFY_SSL        = True                       # flip for air‑gapped nets

# ─────────────────────────── core dataclass ────────────────────────────
@dataclass(slots=True)
class SystemInfo:
    timestamp_utc: str
    timestamp_local: str
    hostname: str
    username: str
    os: str
    os_release: str
    os_version: str
    architecture: str
    public_ip: Optional[str]
    geo: Optional[Dict[str, str]]
    local_ips: Dict[str, List[str]] = field(default_factory=dict)
    mac_addresses: Dict[str, str]   = field(default_factory=dict)
    default_gateway: Optional[str]  = None
    uuid_hash: str                  = ""

# ─────────────────────────── helpers ──────────────────────────────────

def _get_public_ip() -> Tuple[Optional[str], Optional[Dict[str, str]]]:
    for url in PUBLIC_IP_SVC:
        try:
            r = requests.get(url, timeout=3, verify=VERIFY_SSL)
            r.raise_for_status()
            ip = r.json()["ip"] if r.headers.get("content-type", "").startswith("application/json") else r.text.strip()
            # Attempt basic geo lookup (no API‑key required)
            try:
                geo = requests.get(GEO_IP_SVC.format(ip=ip), timeout=3, verify=VERIFY_SSL).json()
            except Exception:
                geo = None
            return ip, geo
        except Exception:
            continue
    return None, None


def _collect_net_info() -> Tuple[Dict[str, List[str]], Dict[str, str], Optional[str]]:
    local_ips: Dict[str, List[str]] = {}
    macs: Dict[str, str] = {}
    gw: Optional[str] = None

    for iface, addrs in psutil.net_if_addrs().items():
        for a in addrs:
            if a.family in (socket.AF_INET, socket.AF_INET6):
                local_ips.setdefault(iface, []).append(a.address)
            elif a.family == psutil.AF_LINK:
                macs[iface] = a.address
    try:
        gws = psutil.net_if_stats()
        default_gw_info = psutil.net_if_stats()
        gw = socket.gethostbyname(socket.gethostname())  # simple fallback
    except Exception:
        pass
    return local_ips, macs, gw


# ─────────────────────────── public API ───────────────────────────────

def collect_attacker_info() -> SystemInfo:
    now = datetime.datetime.utcnow()
    utc = now.strftime(TIME_FMT)
    local = now.astimezone().strftime(TIME_FMT)

    public_ip, geo = _get_public_ip()
    local_ips, macs, gw = _collect_net_info()

    sys_info = SystemInfo(
        timestamp_utc = utc,
        timestamp_local = local,
        hostname       = socket.gethostname(),
        username       = getpass.getuser(),
        os             = platform.system(),
        os_release     = platform.release(),
        os_version     = platform.version(),
        architecture   = platform.machine(),
        public_ip      = public_ip,
        geo            = geo,
        local_ips      = local_ips,
        mac_addresses  = macs,
        default_gateway= gw,
        uuid_hash      = hashlib.sha256(str(uuid.getnode()).encode()).hexdigest(),
    )
    return sys_info


def save_json_log(sys_info: SystemInfo, log_dir: pathlib.Path = LOG_DIR, key: bytes | None = None) -> pathlib.Path:
    """Append *one* JSON‑L line.  If `key` supplied, encrypt with AES‑GCM (pyca/cryptography)."""
    from base64 import b64encode
    filepath = log_dir / f"{datetime.datetime.utcnow():%Y%m%d}.jsonl"
    record = json.dumps(asdict(sys_info), separators=(",", ":"), ensure_ascii=False)

    # Integrity tag (SHA‑256)  – visible even when encrypted
    tag = hashlib.sha256(record.encode()).hexdigest()

    if key:
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            aesgcm = AESGCM(key)
            nonce = os.urandom(12)
            ct = aesgcm.encrypt(nonce, record.encode(), None)
            record = b64encode(nonce + ct).decode()
        except ImportError:
            logging.warning("cryptography not installed - writing plaintext log.")

    with filepath.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"sig": tag, "data": record}) + "\n")
    return filepath

def save_plaintext_log(sys_info: SystemInfo, log_dir: pathlib.Path = LOG_DIR) -> pathlib.Path:
    """Save collected info in clean human-readable .log format."""
    log_path = log_dir / f"{datetime.datetime.utcnow():%Y%m%d}_failed_login.log"

    lines = [
        f"[{sys_info.timestamp_local}] New Failed Login Attempt",
        f"Username       : {sys_info.username}",
        f"Hostname       : {sys_info.hostname}",
        f"Public IP      : {sys_info.public_ip or 'N/A'}",
    ]

    # Geo details
    if sys_info.geo:
        city    = sys_info.geo.get("city", "N/A")
        region  = sys_info.geo.get("region", "N/A")
        country = sys_info.geo.get("country", "N/A")
        org     = sys_info.geo.get("org", "N/A")
        lines.append(f"Location       : {city}, {region}, {country} ({org})")

    # Local IPs
    for iface, ips in sys_info.local_ips.items():
        lines.append(f"Local IPs      : {iface}: {', '.join(ips)}")

    # MACs
    for iface, mac in sys_info.mac_addresses.items():
        lines.append(f"MAC Address    : {iface}: {mac}")

    # More system info
    lines.extend([
        f"OS             : {sys_info.os} ({sys_info.os_version}) {sys_info.architecture}",
        f"Default Gateway: {sys_info.default_gateway or 'N/A'}",
        f"UUID Hash      : {sys_info.uuid_hash}",
        "-" * 60
    ])

    # Write to log file
    with log_path.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return log_path
# ─────────────────────────── CLI entry ────────────────────────────────

if __name__ == "__main__":
    info = collect_attacker_info()
    p = save_plaintext_log(info)
    print("✔ info captured →", p)
