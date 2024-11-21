import socket
import cv2
import numpy as np

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server listening on {host}:{port}")
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")
        
        with conn:
            data = b""
            while True:
                # Read frame size
                while len(data) < 4:
                    packet = conn.recv(4096)
                    if not packet:
                        return
                    data += packet
                frame_size = int.from_bytes(data[:4], 'big')
                data = data[4:]
                
                # Read the frame data
                while len(data) < frame_size:
                    packet = conn.recv(4096)
                    if not packet:
                        return
                    data += packet
                frame_data = data[:frame_size]
                data = data[frame_size:]
                
                # Decode and process the frame
                frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
                if frame is not None:
                    cv2.imshow('Frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

if __name__ == '__main__':
    start_server('0.0.0.0', 5001)
