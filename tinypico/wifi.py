import network
import time
import socket
from machine import Pin

pin = Pin(15, Pin.OUT)

ssid = 'smartbears'
password = ''

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    print("Connecting to Wi-Fi...")
    time.sleep(1)

print("Connected to Wi-Fi!")
print("IP address:", station.ifconfig()[0])

# Define server IP and port
SERVER_IP = '192.168.1.125'  # Replace with your server's IP address
SERVER_PORT = 12345

# Create a UDP socket
udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "Hello, UDP Server!"

# Send the message to the server
udp_client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

# Receive response from the server
response, server_address = udp_client_socket.recvfrom(1024)
print(f"Received from server: {response.decode()}")

# Close the socket
udp_client_socket.close()

if response.decode() == '1':
    pin.on()   # Alternatively: pin.value(1)
    print("Pin is HIGH")
    time.sleep(1)  # Keep it high for 1 second

    # Set the pin low (0V)
    pin.off()  # Alternatively: pin.value(0)
    print("Pin is LOW")
    time.sleep(1)  # Keep it low for 1 second

