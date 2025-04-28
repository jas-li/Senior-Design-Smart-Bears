import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
from PIL import Image

load_dotenv()

api_key = os.getenv("API_KEY")

# system_instruction="""
# You are an AI assistant designed to help visually impaired individuals navigate their surroundings and answer questions about their environment. You will receive input in the form of a natural language query from the user, an image of the scene in front of them with bounding boxes and labels around identified objects, and a stereoscopic depth map of the same view.

# Your primary goal is to provide concise and helpful navigational information based on the user's query and the provided visual data. Focus on clear, simple instructions that allow the user to understand the layout of their surroundings and move safely.

# Here are some key principles to follow:

# 1.  **Prioritize Safety:** Ensure that your instructions guide the user away from potential hazards and towards safe paths.

# 2.  **Be Specific:** Use precise language to describe distances ("a few steps," "several meters") and directions ("turn left," "move slightly to your right").

# 3.  **Use Object References:** Refer to identified objects in the scene to orient the user (e.g., "Walk towards the door," "The chair is to your left").

# 4.  **Anticipate User Needs:** Consider what information the user might need to navigate effectively, such as upcoming turns, obstacles, or points of interest.

# 5.  **Be Concise:** Keep your responses as short as possible while still conveying the necessary information. Avoid unnecessary details or explanations.

# 6.  **Consider Depth Information:** Use the depth map to accurately assess distances and spatial relationships between objects.

# 7.  **Example Scenario:** If the user asks how to navigate the area in front of them and provides an image of a hallway with a turn to the left or right, a good response would be: "Take a few steps forward and turn in the direction of the opening."

# 8. **Customizable Commands:** Understand that users may want customizable voice commands set for specific actions to create a more intuitive experience[2].

# 9. **Multi-Modal Communication:** Be prepared to handle complex interactions with the user to answer questions about their surroundings[3]. You can provide personalized, informative feedback tailored to a user’s specific goals[1].

# 10. **Accessibility Focus:** When generating code or suggesting actions, ensure they conform to WCAG 2.1 Level A and AA success criteria, using semantic HTML and keyboard operability where applicable[5]. Follow ARIA Authoring Practices Guide and related design patterns[5].

# By following these guidelines, you can provide valuable assistance to visually impaired users, helping them to navigate their environment with greater confidence and independence.
# """
# system_instruction = "Hello"

system_instruction = """
You are an AI assistant designed to help visually impaired users, referred to as 'Senior Design Smart Bears', navigate their environment safely and confidently.

You are always provided with:
1. A regular color image of the user's forward view.
2. A depth map image showing relative distances (red = close, blue = far).

Your job is to describe only what's important based on their question**for immediate awareness, visual assitance, or navigation**:
- Mention nearby obstacles or objects directly in front.
- Highlight potential hazards if necessary for the question (e.g. steps, vehicles, poles, moving objects).
- Use clear, brief, conversational language like you're a helpful guide walking next to them.
- When the users asks questions based on distance, provide distance estimates for objects in your response.

Avoid long explanations or visual details that don't affect the user's path or safety.
Keep responses concise and focused on action and awareness.
"""


# Initialize Gemini client
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name='gemini-2.0-flash', system_instruction=system_instruction)

# Load the image
right_image = Image.open("right.jpg")
map_image = Image.open("map.jpg")

original_width, original_height = right_image.size
print(original_width, original_height)
# new_width = int(original_width * 250 / original_height)
# # Resize the image
# resized_image = right_image.resize((new_width, 250), Image.ANTIALIAS)
# resized_image.save("resized_image.jpg")

# original_width, original_height = map_image.size
# new_width = int(original_width * 250 / original_height)
# # Resize the image
# resized_map_image = map_image.resize((new_width, 250), Image.ANTIALIAS)
# resized_map_image.save("resized_map.jpg")

text_prompt = "What is in front of me?"

start_time = time.perf_counter()

print("Generating Gemini response...")

response = model.generate_content([right_image, map_image, text_prompt])
# response = model.generate_content([resized_image, resized_map_image, text_prompt])

end_time_gemini = time.perf_counter()
elapsed_time_gemini = end_time_gemini - start_time

print(f"Gemini Response: {response.text}")
print(f"{elapsed_time_gemini} passed for Gemini")

usage_metadata = response.usage_metadata
print("Prompt token count:", usage_metadata.prompt_token_count)
print("Candidates token count:", usage_metadata.candidates_token_count)
print("Total token count:", usage_metadata.total_token_count)