import socket

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 4444        # Port 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print(f"Connected to server {HOST}:{PORT}")
    
    while True:
        message = input("Enter message to send (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024)
        print(f"Received from server: {response.decode()}")
