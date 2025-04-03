from machine import I2C, Pin
import time

# Constants
LIDARLITE_ADDR = 0x62  # Default I2C address of LIDAR-Lite v4
I2C_SDA_PIN = 21       # Adjust based on your setup
I2C_SCL_PIN = 22       # Adjust based on your setup

# LIDAR-Lite registers
ACQ_COMMAND = 0x00
STATUS = 0x01
SIG_COUNT_VAL = 0x02
ACQ_CONFIG_REG = 0x04
DISTANCE_HIGH = 0x10
DISTANCE_LOW = 0x11

# Initialize I2C
i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=400000)

def write_register(register, value):
    """Write a value to a register."""
    i2c.writeto(LIDARLITE_ADDR, bytes([register, value]))

def read_register(register):
    """Read a single byte from a register."""
    i2c.writeto(LIDARLITE_ADDR, bytes([register]))
    data = i2c.readfrom(LIDARLITE_ADDR, 1)
    return data[0]

def read_distance():
    """Read the distance measurement."""
    high_byte = read_register(DISTANCE_HIGH)
    low_byte = read_register(DISTANCE_LOW)
    return (high_byte << 8) | low_byte

def wait_for_busy():
    """Wait for the sensor to complete its measurement."""
    while read_register(STATUS) & 0x01:
        time.sleep_ms(5)

def configure_lidar(mode=0):
    """
    Configure the LIDAR-Lite v4.
    mode: Measurement mode.
        0 - Default mode (maximum range)
        1 - Balanced performance
        2 - Short range, high speed
    """
    if mode == 0:
        sig_count_val = 0xFF
        acq_config_reg = 0x08
    elif mode == 1:
        sig_count_val = 0x80
        acq_config_reg = 0x08
    elif mode == 2:
        sig_count_val = 0x18
        acq_config_reg = 0x00
    else:
        raise ValueError("Invalid mode")
    
    write_register(SIG_COUNT_VAL, sig_count_val)
    write_register(ACQ_CONFIG_REG, acq_config_reg)

def sample_distance():
    """Trigger a range measurement and read the distance."""
    wait_for_busy()
    write_register(ACQ_COMMAND, 0x04)  # Trigger measurement
    wait_for_busy()
    return read_distance()

# Main loop
try:
    configure_lidar(mode=0)  # Configure the sensor
    print("LIDAR-Lite v4 configured. Starting measurements...")
    while True:
        distance = sample_distance()
        print(f"Distance: {distance} cm")
        time.sleep(1)  # Adjust delay as needed
except KeyboardInterrupt:
    print("Measurement stopped.")
