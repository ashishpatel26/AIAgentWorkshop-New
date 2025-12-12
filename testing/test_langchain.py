from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-oss-120b",
    api_key="e601d1fe-2b94-489d-b6d8-2b6f853e4bfe",
    base_url="https://api.sambanova.ai/v1"
)

messages = [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "Explain the importance of fast language models."}
]

response = llm.invoke(messages)

print(response.content)