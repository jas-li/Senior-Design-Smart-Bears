import socket
from machine import Pin
import time

# Configure the UDP server
UDP_IP = "0.0.0.0"  # Listen on all available network interfaces
UDP_PORT = 1234      # The port to listen on

# Set up GPIO pin (e.g., Pin 15) as an output pin
pin = Pin(15, Pin.OUT)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP packets on {UDP_IP}:{UDP_PORT}")

# Listen for incoming packets and handle them
while True:
    data, addr = sock.recvfrom(1024)  # Receive data with a buffer size of 1024 bytes
    print(f"Received message: {data.decode()} from {addr}")
    
    if(data.decode() == 'person'):
        # Set the pin high (3.3V)
        pin.on()   # Alternatively: pin.value(1)
        print("Pin is HIGH")
        time.sleep(1)  # Keep it high for 1 second

        # Set the pin low (0V)
        pin.off()  # Alternatively: pin.value(0)
        print("Pin is LOW")
        time.sleep(1)  # Keep it low for 1 second

