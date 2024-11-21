import io
import socket
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from threading import Condition

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

def stream_to_tcp(host, port):
    picam2 = Picamera2()
    camera_config = picam2.create_video_configuration(
        main={"size": (1280, 720), "format": "RGB888"},
        controls={"FrameDurationLimits": (33333, 33333)}  # ~30fps
    )
    picam2.configure(camera_config)
    
    output = StreamingOutput()
    encoder = JpegEncoder()
    picam2.start_recording(encoder, FileOutput(output))
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")
        
        try:
            while True:
                with output.condition:
                    output.condition.wait()
                    frame = output.frame
                    output.frame = None
                # Prepend the frame size before sending
                frame_size = len(frame).to_bytes(4, 'big')
                client_socket.sendall(frame_size + frame)
        finally:
            picam2.stop_recording()

if __name__ == '__main__':
    # Replace with the IP of the machine running the model and the desired port
    SERVER_HOST = '192.168.x.x'  # Replace with server IP
    SERVER_PORT = 5001  # Replace with server port
    stream_to_tcp(SERVER_HOST, SERVER_PORT)
