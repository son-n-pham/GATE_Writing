import os
from dotenv import load_dotenv
import google.generativeai as genai
from config.py import LLM_MODEL

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API with key from .env file
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Add error handling for API key
def validate_api_key():
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY not found in environment variables")

try:
    validate_api_key()

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[]
    )

    response = chat_session.send_message("Hello")
    print(response.text)

except Exception as e:
    print(f"Error: {e}")
