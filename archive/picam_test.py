from picamera2 import Picamera2
import time

picam2_left = Picamera2(0)
picam2_right = Picamera2(1)

picam2_left.preview_configuration.main.size = (1920, 1080)
picam2_right.preview_configuration.main.size = (1920, 1080)

picam2_left.start()
picam2_right.start()

zero_start = time.perf_counter()

picam2_left.capture_file("left0.jpg")
picam2_right.capture_file("right0.jpg")

zero_end = time.perf_counter()

print("Finished 0")

time.sleep(10)

one_start = time.perf_counter()

picam2_left.capture_file("left1.jpg")
picam2_right.capture_file("right1.jpg")

one_end = time.perf_counter()

print("Zero time: " + str(zero_end - zero_start))
print("One time: " + str(one_end - one_start))