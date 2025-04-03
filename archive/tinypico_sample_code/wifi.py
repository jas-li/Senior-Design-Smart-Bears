import network
import time
import socket
import math
from machine import Pin, PWM

def pulse(pin):
    for _ in range(3):
        pin.on()   
        time.sleep(0.25) 
        pin.off()  
        time.sleep(0.25)  
        
def increment(pin):
    pwm = PWM(Pin(pin))
    pwm.freq(50)

    for x in range(0, 564, 20):  # Increment from 0 to 1023 in steps of 20
        pwm.duty(x) 
        time.sleep(0.25)  

    pwm.duty(0)  # Stop the PWM after reaching maximum intensity
    
def constant(pin):
    pin.on()   
    time.sleep(2)
    pin.off()    
    
analog_pin = Pin(14, Pin.OUT)
digital_pin = Pin(15, Pin.OUT)

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

while True:
    # Send the message to the server
    udp_client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

    # Receive response from the server
    response, server_address = udp_client_socket.recvfrom(1024)
    print(f"Received from server: {response.decode()}")

    value = response.decode()

    if value == '1':
        pulse(digital_pin)
    elif value == '2':
        increment(analog_pin)
    elif value == '3':
        constant(digital_pin)
        
    time.sleep(4)
        
# Close the socket
udp_client_socket.close()



