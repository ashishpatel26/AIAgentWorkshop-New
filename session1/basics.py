"""
Session 1: Basic AI Agent Examples
This file shows simple examples of AI agents for beginners.
We will learn how AI can chat and use tools to solve problems.
"""

from langchain_openai import ChatOpenAI
from config import API_KEY, MODEL, API_BASE, TEMPERATURE, MAX_TOKENS, MAX_RETRIES, RETRY_DELAY, LLM_STRING, PROVIDER

def basic_chat_example():
    """Example 1: Simple chat with AI"""
    print("=== Example 1: Basic Chat with AI ===")
    print("This shows how to talk to an AI assistant.")
    print()

    # Ask user what they want to ask
    try:
        user_question = input("What would you like to ask the AI? (press Enter for default): ").strip()
        if not user_question:
            user_question = "Explain what an AI agent is in simple terms."
    except EOFError:
        # Handle non-interactive environments
        user_question = "Explain what an AI agent is in simple terms."
        print("What would you like to ask the AI? (press Enter for default): ")
        print("(Using default question in non-interactive environment)")

    # Create the AI model (like choosing which AI to talk to)
    llm = ChatOpenAI(
        temperature=TEMPERATURE,  # How creative the AI should be
        model=MODEL,              # Which AI model to use
        api_key=API_KEY,          # Our secret key to use the AI
        base_url=API_BASE         # Where to connect to the AI
    )

    # Prepare our message to the AI
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},  # Tell AI how to behave
        {"role": "user", "content": user_question}  # User's question
    ]

    print(f"Sending your question to AI: '{user_question}'")
    print("AI is thinking...")
    response = llm.invoke(messages)  # Send message and get response

    print("\nAI says:")
    print(response.content)
    print()

def simple_math_helper():
    """Example 2: AI Math Helper (simplified version)"""
    print("=== Example 2: AI Math Helper ===")
    print("This shows how AI can help with simple math.")
    print()

    # Ask user for their math question
    try:
        math_question = input("What math question would you like to ask? (press Enter for default): ").strip()
        if not math_question:
            math_question = "If you have 15 apples and buy 27 more, then give away 3, how many do you have left?"
    except EOFError:
        # Handle non-interactive environments
        math_question = "If you have 15 apples and buy 27 more, then give away 3, how many do you have left?"
        print("What math question would you like to ask? (press Enter for default): ")
        print("(Using default question in non-interactive environment)")

    # Create the AI brain
    llm = ChatOpenAI(
        temperature=TEMPERATURE,
        model=MODEL,
        api_key=API_KEY,
        base_url=API_BASE
    )

    # Create a helpful message for the AI
    messages = [
        {"role": "system", "content": "You are a helpful math tutor. Explain your answers clearly step by step."},
        {"role": "user", "content": math_question}
    ]

    print(f"Asking AI: {math_question}")
    print("AI is thinking...")
    response = llm.invoke(messages)

    print("\nAI Math Helper says:")
    print(response.content)
    print()

def main():
    """Run all the basic examples."""
    print("AI Agent Workshop - Session 1: Learning the Basics")
    print("=" * 60)
    print("Welcome! Today we'll learn about AI agents.")
    print("An AI agent is like a smart helper that can think and use tools.")
    print()

    try:
        # Run the first example
        basic_chat_example()

        # Run the second example
        simple_math_helper()

        print("Great job! You completed all the basic examples!")
        print("You now know how AI agents can chat and use tools.")

    except Exception as e:
        print(f"Oops! Something went wrong: {e}")
        if PROVIDER == 'sambanova':
            print("Make sure your SAMBA_API_KEY is set correctly in the .env file.")
        elif PROVIDER == 'ollama':
            print("Make sure Ollama is running locally on http://localhost:11434")
            print("Install Ollama from https://ollama.ai and run: ollama serve")
        print("Check the README.md for setup instructions.")

if __name__ == "__main__":
    main()