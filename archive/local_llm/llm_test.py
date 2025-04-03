#!/opt/homebrew/bin/python3.10
import ollama

text = "hi"

def process_speech_input(text):
    # Check if query is relevant
    
    # Send to llava
    response = ollama.chat(model="llava:7b", 
        messages=[
            {"role": "user", "content": text},
        ],
        )
    
    # Extract the response
    llm_response = response["message"]["content"]

    return llm_response

print(process_speech_input(text))