"""
Simple configuration for AI Agent Workshop.
Automatically loads environment variables and provides easy imports.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration - Choose provider
PROVIDER = os.getenv('AI_PROVIDER', 'ollama')  # 'sambanova' or 'ollama'

if PROVIDER == 'sambanova':
    API_KEY = os.getenv('SAMBA_API_KEY', '1f2ecb79-46bf-4b57-938a-b26db06ed941')
    MODEL = os.getenv('SAMBA_MODEL', 'gpt-oss-120b')
    API_BASE = 'https://api.sambanova.ai/v1'
elif PROVIDER == 'ollama':
    API_KEY = 'ollama'  # Ollama doesn't need a real API key
    MODEL = os.getenv('OLLAMA_MODEL', 'gemma3:4b')
    API_BASE = 'http://localhost:11434/v1'
else:
    # Default to SambaNova
    API_KEY = os.getenv('SAMBA_API_KEY', '1f2ecb79-46bf-4b57-938a-b26db06ed941')
    MODEL = os.getenv('SAMBA_MODEL', 'gpt-oss-120b')
    API_BASE = 'https://api.sambanova.ai/v1'

# Workshop Configuration
DEBUG = os.getenv('WORKSHOP_DEBUG', 'false').lower() == 'true'
MAX_TOKENS = int(os.getenv('MAX_TOKENS', '4000'))
TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))

# Agent Configuration
MAX_RETRIES = 3
RETRY_DELAY = 1.0

# LLM Configuration based on provider
if PROVIDER == 'ollama':
    LLM_STRING = f"ollama/{MODEL}"  # Ollama uses ollama/model format
else:
    LLM_STRING = f"{PROVIDER}/{MODEL}"  # SambaNova uses provider/model format