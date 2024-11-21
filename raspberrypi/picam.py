import io
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from flask import Flask, Response
from threading import Condition

app = Flask(__name__)

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

def generate_frames():
    picam2 = Picamera2()
    # Optimize configuration for higher FPS
    camera_config = picam2.create_video_configuration(
        main={"size": (1280, 720), "format": "RGB888"},
        controls={"FrameDurationLimits": (33333, 33333), "Rotation": 0}  # ~30fps
    )
    picam2.configure(camera_config)
    
    output = StreamingOutput()
    encoder = JpegEncoder()
    picam2.start_recording(encoder, FileOutput(output))

    try:
        while True:
            with output.condition:
                output.condition.wait()
                frame = output.frame
                output.frame = None
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        picam2.stop_recording()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)