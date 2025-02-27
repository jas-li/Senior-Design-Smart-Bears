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

# Function to process speech input
def process_speech_input(text):
    # Check if query is relevant
    system_prompt = "You are an assistant for visually impaired people. Determine if this query is relevant. Relevant queries include questions about surroundings, identifying objects, reading text, or describing colors. Respond with 'RELEVANT' or 'NOT RELEVANT' followed by your response."
    
    # Send to TinyLlama
    response = client.chat(model="tinyllama", messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ])
    
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

