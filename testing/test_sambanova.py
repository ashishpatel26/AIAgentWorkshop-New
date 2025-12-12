from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key="e601d1fe-2b94-489d-b6d8-2b6f853e4bfe",
    base_url="https://api.sambanova.ai/v1",
)

response = client.chat.completions.create(
    model="gpt-oss-120b",
    messages=[{"role": "user", "content": "Explain the importance of fast language models"}]
)

print(response.choices[0].message.content)