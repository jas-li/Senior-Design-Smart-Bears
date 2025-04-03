from machine import Pin, PWM
import time
import random

# Set up a PWM pin (e.g., Pin 12) for motor control
pwm_pin = Pin(14, Pin.OUT)  # GPIO 12
pwm = PWM(pwm_pin)

# Set the frequency of PWM (50 Hz is common for motors)
pwm.freq(50)

# Initial duty cycle (motor starts off)
duty_cycle = 0

# Gradually increase the motor intensity (voltage)
try:
    while True:
        # Set the PWM duty cycle (0-1023)
        random_int = random.randint(0, 1023)  
        pwm.duty(random_int)
        
        # Print the current duty cycle for debugging
        print("Duty cycle: {}".format(duty_cycle))
        
        
        
        # Gradually increase the duty cycle
        duty_cycle += random_int
        
        if duty_cycle > 1023:  # Max duty cycle value for PWM
            duty_cycle = 0  # Reset to 0 for a smooth loop
        
        # Sleep for 0.1 seconds to allow for gradual increase
        time.sleep(0.1)
        
except KeyboardInterrupt:
    # When stopping the script, turn off the motor
    pwm.duty(0)
    print("\nMotor stopped.")

