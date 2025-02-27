#!/home/pi/Senior-Design-Smart-Bears/pyenv/bin/python3.11
import subprocess
from ollama import Client
from stream2sentence import generate_sentences

# Initialize Ollama client
client = Client()

# Run whisper-stream and capture its output
whisper_process = subprocess.Popen(["./whisper-stream"], 
                                  stdout=subprocess.PIPE, 
                                  text=True,
                                  bufsize=1)

system_prompt = "You are an assistant for visually impaired people. Help them understand their surroundings, identify objects, read text, or describe colors."

# Send to llava
response = client.chat(model="llava:7b", 
    messages=[
        {"role": "system", "content": system_prompt},
    ],
    options={
        "num_ctx": 2048,  # Adjust context window
        "num_gpu": 1,     # Ensure GPU usage if available
        "num_thread": 4   # Adjust based on your CPU
})

# Function to process speech input
def process_speech_input(text):
    # Check if query is relevant
    
    # Send to llava
    response = client.chat(model="llava:7b", 
        messages=[
            {"role": "user", "content": text},
        ],
        options={
            "num_ctx": 2048,  # Adjust context window
            "num_gpu": 1,     # Ensure GPU usage if available
            "num_thread": 4   # Adjust based on your CPU
    })
    
    # Extract the response
    llm_response = response["message"]["content"]

    return llm_response
    
    # Check if response indicates relevance
    if "RELEVANT" in llm_response.split()[0]:
        # Process relevant query (later you'll add camera input processing here)
        return llm_response
    else:
        return "Query not relevant to visual assistance."

# Main loop to continuously process speech
while True:
    
    # Read the transcribed text
    transcribed_text = whisper_process.stdout.readline().strip()

    # if the last character of transcribed_text is a question mark, run process_speech_input:
    print(transcribed_text)
    if transcribed_text.endswith('?'):
        response = process_speech_input(transcribed_text)
        print(f"Response: {response}")


    
    # if transcribed_text:
    #     print(transcribed_text)
    #     response = process_speech_input(transcribed_text)
    #     print(f"Response: {response}")
        
        # Here you would send the response to your TTS system
        # For example: subprocess.run(["espeak", response])

