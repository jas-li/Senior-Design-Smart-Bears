from machine import Pin, Timer
import time
import network
import usocket as socket

# WiFi credentials
WIFI_SSID = "smartbears"
WIFI_PASSWORD = ""

# Server configuration
SERVER_IP = "192.168.1.142"  # Raspberry Pi's IP
SERVER_PORT = 12345

class DebouncedButton:
    def __init__(self, pin_num, pull=Pin.PULL_UP, debounce_ms=50):
        self.pin = Pin(pin_num, Pin.IN, pull)
        self.debounce_ms = debounce_ms
        self.timer = Timer(-1)
        self.last_state = self.pin.value()
        self.stable_state = self.pin.value()
        self.last_change_time = time.ticks_ms()
        self.triggered = False
        
    def is_pressed(self):
        current_state = self.pin.value()
        current_time = time.ticks_ms()
        
        if current_state != self.last_state:
            self.last_state = current_state
            self.last_change_time = current_time
            
        if time.ticks_diff(current_time, self.last_change_time) > self.debounce_ms:
            if current_state != self.stable_state:
                self.stable_state = current_state
                if self.stable_state == 0:  # Pressed (assuming PULL_UP)
                    if not self.triggered:
                        self.triggered = True
                        return True
                else:
                    self.triggered = False
        return False

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print("Connecting to WiFi...")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.5)
print("Connected to WiFi:", wlan.ifconfig())

# Create UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# print(f"Socket created to UDP server {SERVER_IP}:{SERVER_PORT}")

# Create button on pin 20
button = DebouncedButton(14)

while True:
    if button.is_pressed():
        print("Button pressed - sending notification")
        try:
            # Send message to Raspberry Pi
            udp_socket.sendto(b"Button pressed", (SERVER_IP, SERVER_PORT))
        except Exception as e:
            print("Error sending message:", e)
    
    time.sleep(0.01)
