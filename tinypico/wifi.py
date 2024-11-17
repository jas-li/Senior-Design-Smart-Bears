import network
import time
import socket
import math
from machine import Pin, PWM


def notification(pin):
    for _ in range(3):
        pin.on()   # Alternatively: pin.value(1)
        time.sleep(.25)  # Keep it high for 1 second
        pin.off()  # Alternatively: pin.value(0)
        time.sleep(.1)  # Keep it low for 1 second
        
def loading(pin):
    pwm = PWM(pin)
    pwm.freq(50)
    for _ in range(2):
        for x in range(50):
            duty_cycle = 256 + math.floor(256 * (1 + (math.sin(2 * math.pi * x / 50))))
            pwm.duty(duty_cycle)
            time.sleep(0.05)
    pwm.duty(0)
    
    
pin = Pin(14, Pin.OUT)
pin.on()
time.sleep(10)
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
SERVER_IP = '192.168.1.101'  # Replace with your server's IP address
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

value = response.decode()

if value == '1':
    loading(pin)
elif value == '2':
    notification(pin)


