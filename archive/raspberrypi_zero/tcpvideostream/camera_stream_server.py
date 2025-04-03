import socket
import numpy as np

import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2
from cvlib.object_detection import YOLO

import pyttsx3

# YOLO configuration
weights = '../../../Object-Detection-model/yolov3.weights'
config = '../../../Object-Detection-model/yolov3.cfg'
labels = '../../../Object-Detection-model/coco.names'
yolo = YOLO(weights, config, labels)

# Text-to-Speech
tts_engine = pyttsx3.init()

# TinyPico
UDP_IP = "192.168.1.134"  # IP address of the MicroPython device
UDP_PORT = 1234           # Port where the server is listening

def announce_objects(labels_detected):
    announcement = "I see " + labels_detected
    print(f"Announcement: {announcement}")
    tts_engine.say(announcement)
    tts_engine.runAndWait()

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
                    # Apply object detection
                    bbox, label, conf = yolo.detect_objects(frame)
                    print(bbox, label, conf)

                    if conf and label and bbox:
                        for i in range(len(conf)):
                            if conf[i] > 0.96:
                                if(label[i] == 'person'):
                                    print("Saw a person")
                                    tinypico = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                    tinypico.sendto("person".encode(), (UDP_IP, UDP_PORT))
                                announce_objects(label[i])
                                break
                    
                    # Draw bounding box over detected objects
                    try:
                        out = draw_bbox(frame, bbox, label, conf)
                    except ValueError as e:
                        print(f"Error drawing bounding box: {e}")
                        continue  # Skip to the next frame
                    
                    # Display output
                    cv2.imshow("Real-time object detection", out)

                    # Press "Q" to stop
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

if __name__ == '__main__':
    start_server('0.0.0.0', 5001)
