#!/opt/homebrew/bin/python3.10
import subprocess
import ollama
import argparse
import time
from PIL import Image
import google.generativeai as genai
from stream2sentence import generate_sentences
import os
from dotenv import load_dotenv

# Set up argument parser
parser = argparse.ArgumentParser(description="Process speech input with image analysis.")
parser.add_argument("image_path", help="Path to the image file")
args = parser.parse_args()

# Run whisper-stream and capture its output
whisper_process = subprocess.Popen(["./whisper-stream"], 
                                  stdout=subprocess.PIPE, 
                                  text=True,
                                  bufsize=1)

system_prompt = """
    You are an assistant for visually impaired people. Limit your response to one sentence.
"""


load_dotenv()

api_key = os.getenv("API_KEY")
# Initialize Gemini client
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

# Function to encode image to base64
# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

# Function to process speech input
def process_speech_input_ollama(text, image_path):
    # Send to llava
    response = ollama.chat(model="llava:7b", 
        messages=[
            {"role": "user", 
            "content": system_prompt + text,
            "images": [image_path]},
        ],
        )
    
    # Extract the response
    llm_response = response["message"]["content"]

    return llm_response

image = Image.open(args.image_path)
# Function to process speech input with Gemini
def process_speech_input_gemini(text, image):
    # image_parts = [
    #     {"mime_type": "image/jpeg", "data": encode_image(image_path)}
    # ]
    # prompt_parts = [
    #     system_prompt + text,
    #     image_parts[0]
    # ]
    # response = client.models.generate_content(
    # model="gemini-2.0-flash",
    # contents=[image, system_prompt + text])
    response = model.generate_content([image, system_prompt + text], stream=False)
    return response.text

# Main loop to continuously process speech
while True:
    # Read the transcribed text
    transcribed_text = whisper_process.stdout.readline().strip()

    # if the last character of transcribed_text is a question mark, run process_speech_input:
    print(transcribed_text)
    if transcribed_text.endswith('?'):
        # Get responses from both Ollama and OpenAI
        print("Generating Gemini response...")
        start_time = time.perf_counter()
        gemini_response = process_speech_input_gemini(transcribed_text, args.image_path)
        end_time_gemini = time.perf_counter()
        elapsed_time_gemini = end_time_gemini - start_time
        print(f"Gemini Response: {gemini_response}")
        print(f"{elapsed_time_gemini} seconds passed for Gemini")

        # print("Generating ollama response...")
        # ollama_response = process_speech_input_ollama(transcribed_text, args.image_path)
        # end_time_ollama = time.perf_counter()
        # elapsed_time_ollama = end_time_ollama - end_time_gemini
        # print(f"Ollama Response: {ollama_response}")
        # print(f"{elapsed_time_ollama} seconds passed for ollama")

