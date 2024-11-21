# Detect objects from images
# --------------------------
import cv2
import matplotlib.pyplot as plt 
from cvlib.object_detection import draw_bbox
from cvlib.object_detection import YOLO

image = cv2.imread("../Object-Detection-model/img/stop.jpg") 
plt.imshow(image)

weights = '../Object-Detection-model/yolov3.weights'
config = '../Object-Detection-model/yolov3.cfg'
labels = '../Object-Detection-model/coco.names'
yolo = YOLO(weights, config, labels)

box, label, count = yolo.detect_objects(image)
output = draw_bbox(image, box, label, count)

# display output
cv2.imshow("object detection", output)
cv2.waitKey(0) 

# # Detect objects through webcam
# # -----------------------------
# import cvlib as cv
# from cvlib.object_detection import draw_bbox
# import cv2
# from cvlib.object_detection import YOLO

# weights = 'yolov3.weights'
# config = 'yolov3.cfg'
# labels = 'coco.names'
# yolo = YOLO(weights, config, labels)

# # open webcam
# webcam = cv2.VideoCapture(0)

# if not webcam.isOpened():
#     print("Could not open webcam")
#     exit()
    

# # loop through frames
# while webcam.isOpened():

#     # read frame from webcam 
#     status, frame = webcam.read()

#     if not status:
#         print("Could not read frame")
#         exit()

#     # apply object detection
#     bbox, label, conf = yolo.detect_objects(frame)

#     print(bbox, label, conf)

#     # draw bounding box over detected objects
#     out = draw_bbox(frame, bbox, label, conf)

#     # display output
#     cv2.imshow("Real-time object detection", out)

#     # press "Q" to stop
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
    
# # release resources
# webcam.release()
# cv2.destroyAllWindows()        