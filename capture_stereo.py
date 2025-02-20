import cv2
import numpy as np

# Load calibration data (you need to perform calibration beforehand)
calibration_data = np.load('stereo_calibration.npz')
camera_matrix_left = calibration_data['camera_matrix_left']
dist_coeffs_left = calibration_data['dist_coeffs_left']
camera_matrix_right = calibration_data['camera_matrix_right']
dist_coeffs_right = calibration_data['dist_coeffs_right']
R = calibration_data['R']
T = calibration_data['T']

# Compute rectification transforms
image_size_left = (1920, 1080)  # Adjust to your camera resolution
image_size_right = (1280, 720)  # Adjust to your camera resolution
R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(camera_matrix_left, dist_coeffs_left,
                                            camera_matrix_right, dist_coeffs_right,
                                            image_size_right, R, T)

# Compute rectification maps
map1_left, map2_left = cv2.initUndistortRectifyMap(camera_matrix_left, dist_coeffs_left, R1, P1, image_size_left, cv2.CV_32FC1)
map1_right, map2_right = cv2.initUndistortRectifyMap(camera_matrix_right, dist_coeffs_right, R2, P2, image_size_right, cv2.CV_32FC1)

# Create StereoBM object
stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)

# Initialize video captures
cap_left = cv2.VideoCapture(0)  # Adjust index if needed
cap_right = cv2.VideoCapture(1)  # Adjust index if needed

while True:
    # Capture frames
    ret_left, frame_left = cap_left.read()
    ret_right, frame_right = cap_right.read()
    
    if not ret_left or not ret_right:
        break
    
    # Resize left frame to match right frame size
    left_frame_resized = cv2.resize(left_frame, image_size_right)
    

    # In the main loop, before computing disparity:
    left_rectified = cv2.remap(left_frame_resized, map1_left, map2_left, cv2.INTER_LINEAR)
    right_rectified = cv2.remap(right_frame, map1_right, map2_right, cv2.INTER_LINEAR)
    
    # Convert to grayscale
    gray_left = cv2.cvtColor(left_rectified, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(right_rectified, cv2.COLOR_BGR2GRAY)
    
    # Compute disparity map
    disparity = stereo.compute(gray_left, gray_right)
    
    # Normalize disparity for display
    disparity_normalized = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    
    # Apply color map for visualization
    disparity_color = cv2.applyColorMap(disparity_normalized, cv2.COLORMAP_JET)
    
    # Display results
    cv2.imshow('Left Image', frame_left)
    cv2.imshow('Right Image', frame_right_resized)
    cv2.imshow('Disparity Map', disparity_color)
    
    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap_left.release()
cap_right.release()
cv2.destroyAllWindows()