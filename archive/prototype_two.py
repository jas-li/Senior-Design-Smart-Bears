#!/opt/homebrew/bin/python3.10
import subprocess
import argparse
import time
from PIL import Image
import google.generativeai as genai
from stream2sentence import generate_sentences
import os
from dotenv import load_dotenv
import cv2
import numpy as np
from cvlib.object_detection import YOLO
import cvlib as cv
from cvlib.object_detection import draw_bbox

# YOLO configuration
weights = './yolov3.weights'
config = './yolov3.cfg'
labels = './coco.names'
yolo = YOLO(weights, config, labels)

system_prompt = """
    You are an assistant for visually impaired people. You will also receive two images alongside this text. The first image is a regular color view, and the second is a disparity map view that shows relative distances. Limit your response to one sentence.
"""

load_dotenv()

api_key = os.getenv("API_KEY")

# Initialize Gemini client
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

# Function to process speech input with Gemini
def process_speech_input_gemini(text, images):
    response = model.generate_content(images + [system_prompt + text], stream=False)
    return response.text

# Load calibration data (you need to perform calibration beforehand)
calibration_data = np.load('stereo_calibration.npz')
camera_matrix_left = calibration_data['camera_matrix_left']
dist_coeffs_left = calibration_data['dist_coeffs_left']
camera_matrix_right = calibration_data['camera_matrix_right']
dist_coeffs_right = calibration_data['dist_coeffs_right']
R = calibration_data['R']
T = calibration_data['T']

# Compute rectification transforms
image_size = (1280, 720)  # Adjust to your camera resolution
R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(camera_matrix_left, dist_coeffs_left,
                                            camera_matrix_right, dist_coeffs_right,
                                            image_size, R, T)
# Compute rectification maps
map1_left, map2_left = cv2.initUndistortRectifyMap(camera_matrix_left, dist_coeffs_left, R1, P1, image_size, cv2.CV_32FC1)
map1_right, map2_right = cv2.initUndistortRectifyMap(camera_matrix_right, dist_coeffs_right, R2, P2, image_size, cv2.CV_32FC1)

# Create StereoBM object
stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)

# Initialize video captures
cap_left = cv2.VideoCapture(0)  # Adjust index if needed
cap_right = cv2.VideoCapture(1)  # Adjust index if needed

# Set resolution for both cameras
width, height = 1280, 720
cap_left.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap_left.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap_right.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap_right.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def depth_mapping(left, right):
    # In the main loop, before computing disparity:
    left_rectified = cv2.remap(left, map1_left, map2_left, cv2.INTER_LINEAR)
    right_rectified = cv2.remap(right, map1_right, map2_right, cv2.INTER_LINEAR)

    # Convert to grayscale
    gray_left = cv2.cvtColor(left_rectified, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(right_rectified, cv2.COLOR_BGR2GRAY)
    
    # Compute disparity map
    disparity = stereo.compute(gray_left, gray_right)
    
    # Estimate rotation angle from rectification matrices
    angle = np.arctan2(R1[1, 0], R1[0, 0]) * 180 / np.pi

    center = (disparity.shape[1] // 2, disparity.shape[0] // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    rotated_disparity = cv2.warpAffine(disparity, M, (disparity.shape[1], disparity.shape[0]), flags=cv2.INTER_LINEAR)

    # Normalize and apply color map to the rotated disparity
    rotated_disparity_normalized = cv2.normalize(rotated_disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    rotated_disparity_color = cv2.applyColorMap(rotated_disparity_normalized, cv2.COLORMAP_JET)
    return rotated_disparity_color

while True:
    # Capture frames
    ret_left, frame_left = cap_left.read()
    ret_right, frame_right = cap_right.read()

    if not ret_left or not ret_right:
        break

    # Display results
    cv2.imshow('Left Image', frame_left)
    cv2.imshow('Right Image', frame_right)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        depth = depth_mapping(frame_left, frame_right)
        cv2.imshow('Depth Map', depth)

        # Apply object detection
        bbox, label, conf = yolo.detect_objects(frame_left)

        # Draw bounding box over detected objects
        out = draw_bbox(frame_left, bbox, label, conf)

        # Display output
        cv2.imshow("Real-time object detection", out)
        print("Generating Gemini response...")
        start_time = time.perf_counter()
        gemini_response = process_speech_input_gemini("What is in front of me?", [Image.fromarray(out), Image.fromarray(depth)])
        end_time_gemini = time.perf_counter()
        elapsed_time_gemini = end_time_gemini - start_time
        print(f"Gemini Response: {gemini_response}")
        print(f"{elapsed_time_gemini} seconds passed for Gemini")


    # Break loop if 'q' is pressed
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap_left.release()
cap_right.release()
cv2.destroyAllWindows()