import cv2
import os
import time

# Create directories if they don't exist
if not os.path.exists('left'):
    os.makedirs('left')
if not os.path.exists('right'):
    os.makedirs('right')

# Initialize the cameras
left_camera = cv2.VideoCapture(2)  # Adjust index if needed
right_camera = cv2.VideoCapture(0)  # Adjust index if needed

# Set resolution for both cameras
width, height = 1920, 1080
left_camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
left_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
right_camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
right_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Allow time for the cameras to warm up
time.sleep(2)

image_count = 0
delay = 2  # Delay between captures in seconds

print("Press 'c' to capture an image pair, 'q' to quit.")

while True:
    # Capture frames from both cameras
    ret_left, frame_left = left_camera.read()
    ret_right, frame_right = right_camera.read()

    # Display the frames
    cv2.imshow('Left Camera', frame_left)
    cv2.imshow('Right Camera', frame_right)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        # Save images
        cv2.imwrite(f'left/image_{image_count:02d}.jpg', frame_left)
        cv2.imwrite(f'right/image_{image_count:02d}.jpg', frame_right)
        print(f"Saved image pair {image_count}")
        image_count += 1
        time.sleep(delay)  # Wait before next capture
    elif key == ord('q'):
        break

# Release the cameras and close windows
cv2.destroyAllWindows()
left_camera.release()
right_camera.release()

print(f"Captured {image_count} image pairs.")

