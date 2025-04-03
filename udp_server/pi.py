import socket
import time
import subprocess
import cv2

# UDP Setup
UDP_IP = ''
UDP_PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening on port {UDP_PORT}")

# Initialize video captures
print("Initializing video captures")
cap_left = cv2.VideoCapture(0)  # Adjust index if needed
cap_right = cv2.VideoCapture(2)  # Adjust index if needed

# Set resolution for both cameras
width, height = 1920, 1080
cap_left.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap_left.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap_right.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap_right.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

print("Waiting for button press")
while True:
    data, addr = sock.recvfrom(1024)
    if data == b'BUTTON_PRESSED':
        print("Received button press - processing...")
        
        # Run handle_OIA.py and capture output
        try:
            # Capture frames
            ret_left, frame_left = cap_left.read()
            ret_right, frame_right = cap_right.read()
            ret = cv2.imwrite("/home/pi/Senior-Design-Smart-Bears/left_capture.jpg", frame_left)
            cv2.imwrite("/home/pi/Senior-Design-Smart-Bears/right_capture.jpg", frame_right)
            if ret:
                print("Successful save")
            start_time = time.perf_counter()

            result = subprocess.check_output(['python3', 'handle_OIA.py'])
            end_time_gemini = time.perf_counter()
            elapsed_time_gemini = end_time_gemini - start_time
            print(elapsed_time_gemini)
            response = result.strip().decode().upper()
        except Exception as e:
            response = 'ERROR'
            print(f"Script failed: {e}")

        # Send result back to ESP
        sock.sendto(response.encode(), (addr[0], 54321))
        print(f"Sent response: {response}")
