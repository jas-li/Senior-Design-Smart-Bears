import socket
import time
import subprocess

# UDP Setup
UDP_IP = ''
UDP_PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening on port {UDP_PORT}")

while True:
    data, addr = sock.recvfrom(1024)
    if data == b'BUTTON_PRESSED':
        print("Received button press - processing...")
        
        # Run tempcommunication.py and capture output
        try:
            result = subprocess.check_output(['python3', 'tempcommunication.py'])
            response = result.strip().decode().upper()
        except Exception as e:
            response = 'ERROR'
            print(f"Script failed: {e}")

        # Send result back to ESP
        sock.sendto(response.encode(), (addr[0], 54321))
        print(f"Sent response: {response}")