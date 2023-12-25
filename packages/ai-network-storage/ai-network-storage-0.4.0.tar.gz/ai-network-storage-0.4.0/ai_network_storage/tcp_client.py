
import socket

def tcp_client():
    server_host = '34.172.161.134'  # Server's IP address
    server_port = 50051        # Server's port

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((server_host, server_port))

    # Send data to server
    message = "Hello, Server!"
    client_socket.send(message.encode('utf-8'))

    # Receive response from the server
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Response from the server: {response}")

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    tcp_client()

