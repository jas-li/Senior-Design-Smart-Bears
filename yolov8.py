import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2
from cvlib.object_detection import YOLO

# YOLO configuration
weights = '../Object-Detection-model/yolov3.weights'
config = '../Object-Detection-model/yolov3.cfg'
labels = '../Object-Detection-model/coco.names'
yolo = YOLO(weights, config, labels)

# Replace webcam with the video stream URL
video_url = "http://192.168.1.101:5000/video_feed"
video_capture = cv2.VideoCapture(video_url)

if not video_capture.isOpened():
    print("Could not open video feed")
    exit()

# Loop through frames
while video_capture.isOpened():

    # Read frame from video feed
    status, frame = video_capture.read()

    if not status:
        print("Could not read frame")
        break

    # Apply object detection
    bbox, label, conf = yolo.detect_objects(frame)

    print(bbox, label, conf)

    # Draw bounding box over detected objects
    out = draw_bbox(frame, bbox, label, conf)

    # Display output
    cv2.imshow("Real-time object detection", out)

    # Press "Q" to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()
