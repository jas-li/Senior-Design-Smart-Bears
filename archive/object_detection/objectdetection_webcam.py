# # Detect objects through webcam
# # -----------------------------
import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2
from cvlib.object_detection import YOLO

weights = '../Object-Detection-model/yolov3.weights'
config = '../Object-Detection-model/yolov3.cfg'
labels = '../Object-Detection-model/coco.names'
yolo = YOLO(weights, config, labels)

# open webcam
webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Could not open webcam")
    exit()

# loop through frames
while webcam.isOpened():

    # read frame from webcam 
    status, frame = webcam.read()

    if not status:
        print("Could not read frame")
        exit()

    # apply object detection
    bbox, label, conf = yolo.detect_objects(frame)

    print(label, conf)

    # draw bounding box over detected objects
    try:
        out = draw_bbox(frame, bbox, label, conf)
    except ValueError as e:
        print(f"Error drawing bounding box: {e}")
        continue  # Skip to the next frame

    # display output
    cv2.imshow("Real-time object detection", out)

    # press "Q" to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# release resources
webcam.release()
cv2.destroyAllWindows()        