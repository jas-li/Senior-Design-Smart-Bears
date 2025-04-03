import io
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from flask import Flask, Response, render_template_string
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

# HTML for two video feeds
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Dual Camera Stream</title>
    <style>
        .container {
            display: flex;
            justify-content: center;
            gap: 20px;
        }
        .stream {
            width: 640px;
            height: 360px;
        }
    </style>
</head>
<body>
    <div class="container">
        <img class="stream" src="{{ url_for('video_feed_0') }}">
        <img class="stream" src="{{ url_for('video_feed_1') }}">
    </div>
</body>
</html>
"""

def initialize_camera(camera_num):
    picam = Picamera2(camera_num=camera_num)
    camera_config = picam.create_video_configuration(
        main={"size": (1920, 1080), "format": "RGB888"},
        controls={"FrameDurationLimits": (33333, 33333)}
    )
    picam.configure(camera_config)
    return picam

def generate_frames(camera_num):
    picam = initialize_camera(camera_num)
    output = StreamingOutput()
    encoder = JpegEncoder()
    picam.start_recording(encoder, FileOutput(output))

    try:
        while True:
            with output.condition:
                output.condition.wait()
                frame = output.frame
                output.frame = None
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        picam.stop_recording()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/video_feed_0')
def video_feed_0():
    return Response(generate_frames(0),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_1')
def video_feed_1():
    return Response(generate_frames(1),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Check available cameras
    available_cams = Picamera2.global_camera_info()
    if len(available_cams) < 2:
        raise RuntimeError(f"Not enough cameras detected. Found {len(available_cams)} camera(s). Please check that both cameras are properly connected and enabled.")
    
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)

