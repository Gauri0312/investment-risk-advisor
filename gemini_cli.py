import os
import google.generativeai as genai

# Configure the API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model with generation config and safety settings 
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# Start a chat session
chat = model.start_chat(history=[])

# Function to get response from the model
def get_gemini_response(question):
    response = chat.send_message(question)
    return response.text

# Main loop for CLI interaction
if __name__ == "__main__":
    print("Gemini CLI Chatbot. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        response = get_gemini_response(user_input)
        print(f"Gemini: {response}")
