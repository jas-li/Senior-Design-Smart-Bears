import time
import sys
import cv2
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image

start_time = time.perf_counter()

load_dotenv()

api_key = os.getenv("API_KEY")

system_instruction = """
You are an AI assistant designed to help visually impaired users, referred to as 'Senior Design Smart Bears', navigate their environment safely and confidently.
You are always provided with:
1. A regular color image of the user's forward view.
2. A depth map image showing relative distances (red = close, blue = far).
Your job is to describe only what's important based on their question**for immediate awareness, visual assitance, or navigation**:
- Mention nearby obstacles or objects directly in front.
- Highlight potential hazards if necessary for the question (e.g. steps, vehicles, poles, moving objects).
- Use clear, brief, conversational language like you're a helpful guide walking next to them.
- Provide distance estimates for objects in your response.
Avoid long explanations or visual details that don't affect the user's path or safety.
Keep responses concise and focused on action and awareness.
"""

return_phrase = "high"

# Load calibration data (you need to perform calibration beforehand)
calibration_data = np.load('/home/pi/Senior-Design-Smart-Bears/stereo_calibration.npz')
camera_matrix_left = calibration_data['camera_matrix_left']
dist_coeffs_left = calibration_data['dist_coeffs_left']
camera_matrix_right = calibration_data['camera_matrix_right']
dist_coeffs_right = calibration_data['dist_coeffs_right']
R = calibration_data['R']
T = calibration_data['T']

# Compute rectification transforms
image_size = (1920, 1080)  # Adjust to your camera resolution
R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(camera_matrix_left, dist_coeffs_left,
                                            camera_matrix_right, dist_coeffs_right,
                                            image_size, R, T)

# Compute rectification maps
map1_left, map2_left = cv2.initUndistortRectifyMap(camera_matrix_left, dist_coeffs_left, R1, P1, image_size, cv2.CV_32FC1)
map1_right, map2_right = cv2.initUndistortRectifyMap(camera_matrix_right, dist_coeffs_right, R2, P2, image_size, cv2.CV_32FC1)

# Create StereoBM object
stereo = cv2.StereoBM_create(numDisparities=80, blockSize=15)
stereo.setSpeckleWindowSize(25)
stereo.setSpeckleRange(1)
stereo.setTextureThreshold(12)  

# Initialize Gemini client
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name='gemini-2.0-flash', system_instruction=system_instruction)

# Simulated temperature check (replace with actual sensor logic)
if __name__ == "__main__":
    frame_left = cv2.imread("/home/pi/Senior-Design-Smart-Bears/left_capture.jpg")
    frame_right = cv2.imread("/home/pi/Senior-Design-Smart-Bears/right_capture.jpg")
    load_time = time.perf_counter()
    print("Load took ", load_time - start_time)
    # In the main loop, before computing disparity:
    left_rectified = cv2.remap(frame_left, map1_left, map2_left, cv2.INTER_LINEAR)
    right_rectified = cv2.remap(frame_right, map1_right, map2_right, cv2.INTER_LINEAR)

    # Convert to grayscale
    gray_left = cv2.cvtColor(left_rectified, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(right_rectified, cv2.COLOR_BGR2GRAY)

    # Compute disparity map
    disparity = stereo.compute(gray_left, gray_right)
    
    # Normalize disparity for display
    disparity_normalized = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    
    # Apply color map for visualization
    disparity_color = cv2.applyColorMap(disparity_normalized, cv2.COLORMAP_JET)
    # Save disparity map
    cv2.imwrite("/home/pi/Senior-Design-Smart-Bears/map_capture.jpg", disparity_color)

    # Load the image
    original_image = Image.open("/home/pi/Senior-Design-Smart-Bears/right_capture.jpg")
    map_image = Image.open("/home/pi/Senior-Design-Smart-Bears/map_capture.jpg")
    print("Depth Mapping Took ", time.perf_counter() - load_time)

    start_time = time.perf_counter()

    print("Generating Gemini response...")

    

    response = model.generate_content([original_image, map_image])

    end_time_gemini = time.perf_counter()
    elapsed_time_gemini = end_time_gemini - start_time

    print(f"Gemini Response: {response.text}")
    print(f"{elapsed_time_gemini} passed for Gemini")

    print(response.text)
    print(return_phrase)
    sys.exit(0)
