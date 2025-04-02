from machine import Pin, Timer
import time
import usocket as socket

# Server configuration
SERVER_IP = "192.168.1.142"  # pi ip address
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
        
        # Check if the state has changed
        if current_state != self.last_state:
            self.last_state = current_state
            self.last_change_time = current_time
            
        # Check if state is stable for debounce period
        if time.ticks_diff(current_time, self.last_change_time) > self.debounce_ms:
            # If state is stable and different from previous stable state
            if current_state != self.stable_state:
                self.stable_state = current_state
                # For PULL_UP, 0 means pressed
                if self.stable_state == 0:
                    if not self.triggered:
                        self.triggered = True
                        return True
                else:
                    # Button released, reset triggered flag
                    self.triggered = False
                    
        return False

# Create UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Create a debounced button on pin 20
button = DebouncedButton(20)

while True:
    if button.is_pressed():
        print("Button pressed!")
        try:
            # Send message to Raspberry Pi
            udp_socket.sendto(b"BUTTON_PRESSED", (SERVER_IP, SERVER_PORT))
        except Exception as e:
            print("Error sending message:", e)
    
    time.sleep(0.01)  # Small delay to prevent CPU hogging
