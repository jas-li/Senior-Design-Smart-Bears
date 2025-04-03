from machine import ADC, Pin, PWM
import time
import math

# Set up the ADC for the photoresistor on pin IO33
ldr = ADC(Pin(32))
ldr.atten(ADC.ATTN_11DB)  # Full range: 3.3v
led_brightness = 0

# Set up PWM for the LED on pin IO14
led = PWM(Pin(26))
led.freq(1000)  # Set PWM frequency to 1kHz

# Define thresholds for light sensitivity
# Higher values mean darker surroundings
BRIGHT_THRESHOLD = 3000  # Low reading = bright environment
DARK_THRESHOLD = 4000    # High reading = dark environment

# Define LED brightness range
MIN_BRIGHTNESS = 0     # Minimum brightness
MAX_BRIGHTNESS = 1023    # Maximum brightness

# Gradient effect parameters
GRADIENT_SPEED = 10      # Speed of the gradient effect (higher = faster)
GRADIENT_MIN = 0       # Minimum brightness during gradient effect
GRADIENT_MAX = 1023      # Maximum brightness during gradient effect
t = 0
while True:
    raw_value = ldr.read()
    
    if raw_value >= DARK_THRESHOLD:
        t += .3
        t %= (2 * 3.14)
        led_brightness = (math.sin(t) + 1) * 511
        print(f"PULSING: Raw Value: {raw_value}, LED Brightness: {led_brightness}")
    else:
        print(f"Bright Room: Raw Value: {raw_value}, LED Brightness: {led_brightness}")
        led_brightness = MIN_BRIGHTNESS
        print(f"PULSING2222222222: Raw Value: {raw_value}")
    
    led.duty(int(led_brightness))
    time.sleep(0.05)

