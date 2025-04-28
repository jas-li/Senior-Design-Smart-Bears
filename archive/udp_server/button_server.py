from machine import Pin, PWM
import usocket as socket
import time
import network

# WiFi credentials
WIFI_SSID = "smartbears"
WIFI_PASSWORD = ""

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print("Connecting to WiFi...")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.5)
print("Connected to WiFi:", wlan.ifconfig())

# Hardware Setup
BUTTON_PIN = 14
VIBRATOR_PIN = 4
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
vibrator = PWM(Pin(VIBRATOR_PIN), freq=1000, duty=0)

# Network Config
SERVER_IP = "192.168.1.142"  # Pi's IP
SERVER_PORT = 12345
LOCAL_PORT = 54321

# State management
awaiting_response = False
last_press_time = 0

# UDP Socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('0.0.0.0', LOCAL_PORT))
udp_socket.settimeout(0.1)  # Non-blocking receive

def handle_response(response):
    global awaiting_response
    if response == b'HIGH':
        vibrator.duty(512)  # Strong vibration
    elif response == b'LOW':
        vibrator.duty(256)  # Weak vibration
    time.sleep(1)
    vibrator.duty(0)
    awaiting_response = False

while True:
    # Check for incoming messages
    try:
        data, addr = udp_socket.recvfrom(1024)
        if data in [b'HIGH', b'LOW'] and awaiting_response:
            print("Received:", data.decode())
            handle_response(data)
    except:
        pass
    
    # Handle button press
    if button.value() == 0 and not awaiting_response:
        udp_socket.sendto(b'BUTTON_PRESSED', (SERVER_IP, SERVER_PORT))
        awaiting_response = True
        print("Request sent, waiting for response...")
        time.sleep(0.5)  # Debounce