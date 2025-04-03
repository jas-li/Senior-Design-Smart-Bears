import socket
import random

# Define server IP and port
SERVER_HOST = '192.168.1.142'  # pi ip address
SERVER_PORT = 12345      

# Create UDP socket
udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server_socket.bind((SERVER_HOST, SERVER_PORT))

print(f"UDP server listening on {SERVER_HOST}:{SERVER_PORT}")

# Listen for incoming messages
while True:
    message, client_address = udp_server_socket.recvfrom(1024)  # Buffer size of 1024 bytes
    print(f"Received message: {message.decode()} from {client_address}")
    
    # Optionally send a response to the client
    response = "Message received"
    udp_server_socket.sendto(response.encode(), client_address)
