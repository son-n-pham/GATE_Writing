import os
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

load_dotenv()


client = Cerebras(
    api_key=os.getenv("CEREBRAS_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {"role": "user", "content": "Why is fast inference important?", }
    ],
    model="llama-3.3-70b",
)
