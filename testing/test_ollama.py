from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key="ollama",  # Ollama doesn't need a real API key
    base_url="http://localhost:11434/v1",
)

try:
    response = client.chat.completions.create(
        model="gemma3:4b",
        messages=[{"role": "user", "content": "Say hello in one word"}]
    )
    print("Ollama is working!")
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print("Ollama connection failed:", str(e))
    print("Make sure Ollama is running: ollama serve")
    print("And the model is pulled: ollama pull llama3.2:3b")