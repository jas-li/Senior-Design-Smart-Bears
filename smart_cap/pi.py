import socket
import time
import subprocess
import cv2
import pyttsx3
import sys
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image

# UDP Setup
UDP_IP = ''
UDP_PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening on port {UDP_PORT}")

# Initialize video captures
print("Initializing video captures")
cap_left = cv2.VideoCapture(2)  # Adjust index if needed
cap_right = cv2.VideoCapture(0)  # Adjust index if needed

# Set resolution for both cameras
width, height = 1920, 1080
cap_left.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap_left.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap_right.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap_right.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap_left.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap_right.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Initialize stereo
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

# Initializing speech engine
speaker = pyttsx3.init()
speaker.setProperty ('rate', 150)
# Initialize LLM connection
load_dotenv()
api_key = os.getenv("API_KEY")

# Initialize Gemini client
system_instruction="""
You are an AI assistant designed to help visually impaired users, referred to as 'Senior Design Smart Bears', navigate their environment safely and confidently.
You are always provided with:
1. A regular color image of the user's forward view.
2. A depth map image showing relative distances (red = close, blue = far).

First use the regular color image to identify objects and understand what is in the user's view.
Next, if you do identify objects, use the depth mapping image with depth mapping outlines to understand the relative distances of the objects. If there is not enough information in the depth map or it is too noisy, disregard the depth mapping image when performing the following task.

Your job is to describe only what's important based on their question**for immediate awareness, visual assitance, or navigation**.
- Mention nearby obstacles or objects directly in front.
- Highlight potential hazards if necessary for the question (e.g. steps, vehicles, poles, moving objects).
- Use clear, brief, conversational language like you're a helpful guide walking next to them.
- Provide distance estimates for objects in your response.
Avoid long explanations or visual details that don't affect the user's path or safety.
Keep responses concise and focused on action and awareness.
Append the word SAFE to the end of your response if it is safe to continue walking. Append the word UNSAFE to the end of your response if it is not safe to continue walking. Only append one of the two words.
"""

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name='gemini-2.0-flash', system_instruction=system_instruction)

print("Waiting for button press")
while True:
    data, addr = sock.recvfrom(1024)
    if data == b'BUTTON_PRESSED':
        print("Received button press - processing...")
        
        start_time = time.perf_counter()
        # Run handle_OIA.py and capture output
        # Capture frames
        cap_left.grab()
        cap_right.grab()
        ret_left, frame_left = cap_left.read()
        ret_right, frame_right = cap_right.read()

        cv2.imwrite("/home/pi/Senior-Design-Smart-Bears/left_capture.jpg", frame_left)
        cv2.imwrite("/home/pi/Senior-Design-Smart-Bears/right_capture.jpg", frame_right)

        finish_capture_time = time.perf_counter()

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

        rgb_frame = cv2.cvtColor(frame_right, cv2.COLOR_BGR2RGB)
        rgb_map = cv2.cvtColor(disparity_color, cv2.COLOR_BGR2RGB)

        frame_PIL = Image.fromarray(rgb_frame)
        map_PIL = Image.fromarray(rgb_map)

        finish_depth_time = time.perf_counter()

        print("Generating Gemini response...")

        response = model.generate_content([frame_PIL, map_PIL, "Is it safe to walk forward?"])

        finish_gemini_time = time.perf_counter()

        response_text = response.text

        print(f"Response was: {response.text}")

        speaker.say("Beginning Speech." + response_text + "Ending speech")
        speaker.runAndWait()

        flag = response_text.split(" ")[-1]

        # Send result back to ESP
        sock.sendto(flag.encode(), (addr[0], 54321))
        print(f"Sent response: {flag}")

        print("Capture time", finish_capture_time - start_time)
        print("Depth time", finish_depth_time - finish_capture_time)
        print("Gemini time", finish_gemini_time - finish_depth_time)