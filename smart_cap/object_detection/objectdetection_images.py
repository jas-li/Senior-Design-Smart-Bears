# Detect objects from images
# --------------------------
import cv2
import matplotlib.pyplot as plt 
from cvlib.object_detection import draw_bbox
from cvlib.object_detection import YOLO

image = cv2.imread("../Object-Detection-model/img/street2.jpg") 
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
