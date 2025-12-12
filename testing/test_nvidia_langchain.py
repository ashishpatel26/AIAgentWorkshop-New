"""
Test NVIDIA API with LangChain
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()

# NVIDIA API configuration
NVIDIA_API_KEY = "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"

def test_nvidia_langchain():
    """Test NVIDIA with LangChain."""

    # Configure NVIDIA LLM
    llm = ChatOpenAI(
        model="meta/llama3-8b-instruct",
        api_key=NVIDIA_API_KEY,
        base_url="https://integrate.api.nvidia.com/v1",
        temperature=0.7
    )

    # Create messages
    messages = [
        SystemMessage(content="You are a helpful AI assistant."),
        HumanMessage(content="Explain what artificial intelligence is in simple terms.")
    ]

    try:
        response = llm.invoke(messages)
        print("✅ LangChain with NVIDIA successful!")
        print(f"Response: {response.content}")
        return True
    except Exception as e:
        print(f"❌ LangChain with NVIDIA failed: {e}")
        return False

if __name__ == "__main__":
    test_nvidia_langchain()