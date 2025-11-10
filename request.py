"""
http_requests_demo.py
A beginner-friendly but complete demo of HTTP with Python 'requests'.

Run: python http_requests_demo.py
"""

import requests
import json

# Using JSONPlaceholder - a free fake API for testing
BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT = 10  # seconds


def safe_request(method: str, url: str, **kwargs) -> requests.Response:
    """
    Wrapper around requests to add timeout, basic error handling,
    and consistent printing. Raises for non-2xx responses.
    """
    # Ensure we always have a timeout unless the caller overrides it
    kwargs.setdefault("timeout", TIMEOUT)
    
    # For development/testing, you can disable SSL verification if needed
    # kwargs.setdefault("verify", False)  # Uncomment if you have SSL issues
    
    try:
        print(f"Making {method} request to: {url}")
        resp = requests.request(method=method, url=url, **kwargs)
        
        # Print response info
        print(f"Response status: {resp.status_code}")
        if resp.headers.get('Content-Type'):
            print(f"Content-Type: {resp.headers.get('Content-Type')}")
        
        # Raise HTTPError for 4xx/5xx so we handle errors consistently
        resp.raise_for_status()
        return resp
        
    except requests.exceptions.HTTPError as e:
        print(f"[HTTP ERROR] {e} | Status: {getattr(e.response, 'status_code', '?')}")
        if hasattr(e.response, 'text'):
            print(f"Error response: {e.response.text[:200]}...")
        raise
    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out.")
        raise
    except requests.exceptions.ConnectionError as e:
        print(f"[ERROR] Connection problem: {e}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] General request error: {e}")
        raise


def demo_basic_get():
    print("\n=== 1) BASIC GET ===")
    url = f"{BASE_URL}/posts/1"
    resp = safe_request("GET", url)
    data = resp.json()
    print("JSON keys:", list(data.keys()))
    print("Title:", data.get("title"))
    print("Body:", data.get("body")[:50] + "..." if data.get("body") else None)


def demo_get_with_params():
    print("\n=== 2) GET WITH QUERY PARAMETERS ===")
    url = f"{BASE_URL}/posts"
    params = {"userId": 1, "_limit": 3}  # ?userId=1&_limit=3
    resp = safe_request("GET", url, params=params)
    print("Final URL:", resp.url)
    data = resp.json()
    print("Number of items returned:", len(data))
    if data:
        for i, item in enumerate(data[:2]):  # Show first 2
            print(f"Item {i+1}: id={item.get('id')}, title={item.get('title')}")


def demo_get_with_headers():
    print("\n=== 3) GET WITH CUSTOM HEADERS ===")
    url = f"{BASE_URL}/posts/1"
    headers = {
        "Accept": "application/json",
        "User-Agent": "MyPythonApp/1.0",
        "X-Custom-Header": "HelloWorld"
    }
    resp = safe_request("GET", url, headers=headers)
    print("Server headers sample:")
    for header in ['Content-Type', 'Date', 'Server']:
        if header in resp.headers:
            print(f"  {header}: {resp.headers[header]}")


def demo_post_json():
    print("\n=== 4) POST (CREATE) WITH JSON ===")
    url = f"{BASE_URL}/posts"
    payload = {
        "title": "Hello from requests",
        "body": "This is a demo post created via Python requests.",
        "userId": 99
    }
    # Use json= to send a JSON body; requests sets Content-Type automatically
    resp = safe_request("POST", url, json=payload)
    data = resp.json()
    print("Created resource id:", data.get("id"))
    print("Returned object keys:", list(data.keys()))


def demo_post_form_data():
    print("\n=== 4b) POST WITH FORM DATA ===")
    url = f"{BASE_URL}/posts"  # Note: This API expects JSON, but we demo form data
    form_data = {
        "title": "Form data demo",
        "body": "This would be sent as form data",
        "userId": 88
    }
    # Using form data (application/x-www-form-urlencoded)
    resp = safe_request("POST", url, data=form_data)
    data = resp.json()
    print("Form data post - returned id:", data.get("id"))


def demo_put_update():
    print("\n=== 5) PUT (UPDATE/REPLACE) WITH JSON ===")
    url = f"{BASE_URL}/posts/1"
    payload = {
        "id": 1,
        "title": "Updated title via PUT",
        "body": "Replaced content for demo.",
        "userId": 1
    }
    resp = safe_request("PUT", url, json=payload)
    updated_data = resp.json()
    print("Updated title:", updated_data.get("title"))
    print("Updated body:", updated_data.get("body"))


def demo_patch_update():
    print("\n=== 5b) PATCH (PARTIAL UPDATE) ===")
    url = f"{BASE_URL}/posts/1"
    payload = {
        "title": "Only title updated via PATCH"
    }
    resp = safe_request("PATCH", url, json=payload)
    updated_data = resp.json()
    print("After PATCH - title:", updated_data.get("title"))
    print("After PATCH - body (unchanged):", updated_data.get("body")[:30] + "..." if updated_data.get('body') else None)


def demo_delete():
    print("\n=== 6) DELETE (REMOVE) ===")
    url = f"{BASE_URL}/posts/1"
    resp = safe_request("DELETE", url)
    print("DELETE status:", resp.status_code)
    # Many APIs return 204 No Content on delete; this demo API returns {}
    if resp.text:
        print("Response text:", resp.text)
    else:
        print("No content returned (expected for DELETE)")


def demo_with_session():
    print("\n=== 7) USING A SESSION (keeps headers/cookies/conn) ===")
    with requests.Session() as sess:
        sess.headers.update({
            "User-Agent": "MyPythonApp/1.0",
            "Accept": "application/json"
        })
        # First request
        r1 = safe_request("GET", f"{BASE_URL}/posts/2")
        print("First request title:", r1.json().get("title"))

        # Second request reuses the same session
        r2 = safe_request("GET", f"{BASE_URL}/posts/3")
        print("Second request title:", r2.json().get("title"))


def demo_error_handling():
    print("\n=== 8) ERROR HANDLING DEMO ===")
    
    # Demo 404 error
    print("--- Testing 404 error ---")
    try:
        safe_request("GET", f"{BASE_URL}/nonexistent")
    except Exception as e:
        print(f"Expected error caught: {type(e).__name__}")
    
    # Demo invalid URL
    print("\n--- Testing invalid URL ---")
    try:
        safe_request("GET", "https://invalid-domain-that-does-not-exist.abc")
    except Exception as e:
        print(f"Expected error caught: {type(e).__name__}")


if __name__ == "__main__":
    print("HTTP Requests Demo with Python")
    print("=" * 40)
    
    try:
        # Run the demos in order
        demo_basic_get()
        demo_get_with_params()
        demo_get_with_headers()
        demo_post_json()
        demo_post_form_data()
        demo_put_update()
        demo_patch_update()
        demo_delete()
        demo_with_session()
        demo_error_handling()

        print("\n🎉 All demos finished successfully!")
        
    except Exception as e:
        print(f"\n💥 Demo stopped due to error: {e}")
        print("This might be due to network issues or the test API being unavailable.")