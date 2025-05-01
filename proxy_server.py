import socket
import threading

# Configuration
HOST = '127.0.0.1'
PORT = 8080
REMOTE_HOST = 'example.com'  # Replace with the target host
REMOTE_PORT = 80

def handle_client(client_socket):
    request = client_socket.recv(4096)
    if request:
        # Forward the request to the remote server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_socket:
            remote_socket.connect((REMOTE_HOST, REMOTE_PORT))
            remote_socket.sendall(request)
            response = remote_socket.recv(4096)
            client_socket.sendall(response)
    client_socket.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f'Proxy server listening on {HOST}:{PORT}')
        while True:
            client_socket, addr = server_socket.accept()
            print(f'Accepted connection from {addr}')
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == '__main__':
    start_server()
