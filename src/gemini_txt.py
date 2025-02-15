import os
from dotenv import load_dotenv
import google.generativeai as genai
from src.config import LLM_MODEL

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


def list_available_models():
    """List all available Gemini models"""
    try:
        models = genai.list_models()
        print("\nAvailable Gemini Models:")
        print("-" * 50)
        for model in models:
            if "gemini" in model.name:
                print(f"Name: {model.name}")
                print(f"Display Name: {model.display_name}")
                print(f"Description: {model.description}")
                print("-" * 50)
    except Exception as e:
        print(f"Error listing models: {e}")


try:
    validate_api_key()

    list_available_models()

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
