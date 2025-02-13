import requests
import json

# Server base URL
BASE_URL = "http://localhost:1234/v1"

# Function to check available models


def get_models():
    try:
        response = requests.get(f"{BASE_URL}/models")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking models: {e}")
        return None

# Function to send chat completion request


def send_chat_message(message, temperature=0.7):
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-r1-distill-qwen-7b",  # Replace with your actual model name
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ],
        "temperature": temperature
    }

    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=data
        )
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Check if server is running and get models
    models = get_models()
    if models:
        print("Available models:")
        for model in models.get("data", []):
            print(f"- {model['id']}")

    # Send a test message
    response = send_chat_message("Hello, how are you?")
    if response:
        print("\nAI Response:")
        print(response)
