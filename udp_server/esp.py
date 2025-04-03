from machine import ADC, Pin, PWM
import usocket as socket
import network
import time
import math

# ---------- Photoresistor/LED Configuration ----------
# Photoresistor setup
ldr = ADC(Pin(32))
ldr.atten(ADC.ATTN_11DB)
led = PWM(Pin(27))
led.freq(1000)

# Light thresholds
BRIGHT_THRESHOLD = 3000
DARK_THRESHOLD = 4000

# Gradient parameters
t = 0
LAST_GRADIENT_UPDATE = 0
GRADIENT_INTERVAL = 50  # Update every 50ms

# ---------- Button/Vibration Configuration ----------
# Hardware setup
BUTTON_PIN = 14
VIBRATOR_PIN = 4
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
vibrator = PWM(Pin(VIBRATOR_PIN), freq=1000, duty=0)

# ---------- WiFi Configuration ----------
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

# Network config
SERVER_IP = "192.168.1.142"
SERVER_PORT = 12345
LOCAL_PORT = 54321

# State management
awaiting_response = False
LAST_BUTTON_CHECK = 0
BUTTON_INTERVAL = 50  # Check every 50ms

# UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('0.0.0.0', LOCAL_PORT))
udp_socket.settimeout(0.01)

def update_gradient():
    global t, LAST_GRADIENT_UPDATE
    current_time = time.ticks_ms()
    
    if current_time - LAST_GRADIENT_UPDATE >= GRADIENT_INTERVAL:
        raw_value = ldr.read()
        
        if raw_value >= DARK_THRESHOLD:
            t += 0.3
            t %= (2 * 3.14)
            led_brightness = (math.sin(t) + 1) * 511
            led.duty(int(led_brightness))
        else:
            led.duty(0)
        
        LAST_GRADIENT_UPDATE = current_time

def handle_vibration(response):
    global awaiting_response
    
    if response == b'HIGH':
        # Three vibration bursts with pauses
        for i in range(2):
            vibrator.duty(512)  # Strong vibration
            time.sleep(1)
            vibrator.duty(0)    # Pause
            if i < 1:  # No pause after last iteration
                time.sleep(0.5)
                
    elif response == b'LOW':
        # Single vibration as before
        vibrator.duty(256)
        time.sleep(1)
        vibrator.duty(0)
    
    # Reset state after pattern completes
    awaiting_response = False

def check_button():
    global awaiting_response, LAST_BUTTON_CHECK
    current_time = time.ticks_ms()
    
    if current_time - LAST_BUTTON_CHECK >= BUTTON_INTERVAL:
        if button.value() == 0 and not awaiting_response:
            udp_socket.sendto(b'BUTTON_PRESSED', (SERVER_IP, SERVER_PORT))
            awaiting_response = True
            print("Button pressed - request sent")
        LAST_BUTTON_CHECK = current_time

def check_messages():
    try:
        data, addr = udp_socket.recvfrom(1024)
        if data and awaiting_response:
            print("Received:", data.decode())
            handle_vibration(b"HIGH")
    except:
        pass

# ---------- Main Loop ----------
while True:
    # Run both systems simultaneously
    update_gradient()    # Photoresistor/LED system
    check_button()       # Button handling
    check_messages()     # Network response handling

