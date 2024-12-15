import os
from dotenv import load_dotenv
import google.generativeai as genai
import PIL.Image
import json
from pydantic import BaseModel
from pathlib import Path
import sys


class ImageDescriptionResponse(BaseModel):
    text: str


def setup_gemini():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    genai.configure(api_key=api_key)


def create_model():
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )


def get_image_description(image_path: str, model) -> str:
    try:
        image_file = PIL.Image.open(image_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file not found at: {image_path}")
    except PIL.UnidentifiedImageError:
        raise ValueError(f"Invalid image file at: {image_path}")

    prompt = """
    Describe the image in details for using as writing prompt.

    - Look at the image and describe what you see in detail
    - State the main elements, colors, subjects, and any text visible in the image
    - Identify the writing task requirements shown in or implied by the image
    - Summarize how this image serves as a writing prompt

    Example response format:
    "I see [detailed description of image contents]...
    The writing task requires students to [requirements]...
    This image serves as a prompt by [explanation]...
    """

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [image_file],
            },
        ]
    )

    response = chat_session.send_message(prompt)
    return response.text


def write_to_markdown(text: str, output_path: str):
    markdown_content = f"# Image Writing Prompt\n\n{text}"
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    except IOError as e:
        raise IOError(f"Error writing to markdown file: {e}")


def main():
    try:
        setup_gemini()
        model = create_model()

        image_path = "current_writing/image_prompt.png"
        # Get the directory of the image file and create the output path there
        image_dir = Path(image_path).parent
        output_path = image_dir / "prompt_from_image.md"

        # Get image description
        description = get_image_description(image_path, model)

        # Create response object and write to markdown
        response = ImageDescriptionResponse(text=description)
        write_to_markdown(response.text, str(output_path))

        print(f"Successfully wrote prompt to {output_path}")

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
