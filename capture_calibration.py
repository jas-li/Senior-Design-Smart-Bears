import cv2
import os
import time

# Create directories if they don't exist
if not os.path.exists('left'):
    os.makedirs('left')
if not os.path.exists('right'):
    os.makedirs('right')

# Initialize the cameras
left_camera  = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Adjust index if needed
right_camera = cv2.VideoCapture(8, cv2.CAP_V4L2)  # Adjust index if needed

# Check if cameras opened successfully
if not left_camera.isOpened() or not right_camera.isOpened():
    print("Error: Could not open one or both cameras.")
    exit()

image_count = 0
delay = 2  # Delay between captures in seconds

print("Press 'c' to capture an image pair, 'q' to quit.")

while True:
    # Capture frames from both cameras
    ret_left, frame_left = left_camera.read()
    ret_right, frame_right = right_camera.read()

    if not ret_left:
      print("Error: Could not read left.")
    if not ret_right:
      print("Error: Could not read right.")
    if not ret_left or not ret_right:
        print("Error: Could not read frame from one or both cameras.")
        break

    # Display the frames
    cv2.imshow('Left Camera', frame_left)
    cv2.imshow('Right Camera', frame_right)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        # Save images
        cv2.imwrite(f'left/image_{image_count:02d}.jpg', frame_left)
        # cv2.imwrite(f'right/image_{image_count:02d}.jpg', frame_right)
        print(f"Saved image pair {image_count}")
        image_count += 1
        time.sleep(delay)  # Wait before next capture
    elif key == ord('q'):
        break

# Release the cameras and close windows
left_camera.release()
right_camera.release()
cv2.destroyAllWindows()

print(f"Captured {image_count} image pairs.")

