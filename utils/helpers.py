"""
Utility functions and helpers for the AI Agent Workshop.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

def load_environment_variables() -> Dict[str, str]:
    """Load and validate environment variables."""
    load_dotenv()

    required_vars = ['OPENROUTER_API_KEY']
    optional_vars = ['OPENROUTER_MODEL', 'WORKSHOP_DEBUG', 'MAX_TOKENS', 'TEMPERATURE']

    env_vars = {}

    # Check required variables
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            raise ValueError(f"Required environment variable {var} is not set")
        env_vars[var] = value

    # Load optional variables
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            env_vars[var] = value

    return env_vars

def validate_api_key(api_key: str) -> bool:
    """Validate OpenRouter API key format."""
    if not api_key or not isinstance(api_key, str):
        return False

    # Basic validation - OpenRouter keys start with 'sk-or-v1-'
    return api_key.startswith('sk-or-v1-') and len(api_key) > 20

def format_agent_response(response: Any) -> str:
    """Format agent response for consistent output."""
    if isinstance(response, str):
        return response.strip()
    elif hasattr(response, '__str__'):
        return str(response).strip()
    else:
        return f"Response: {response}"

def create_progress_indicator(current: int, total: int, prefix: str = "Progress") -> str:
    """Create a simple progress indicator string."""
    percentage = int((current / total) * 100) if total > 0 else 0
    bar_length = 20
    filled_length = int(bar_length * current / total) if total > 0 else 0

    bar = '█' * filled_length + '░' * (bar_length - filled_length)

    return f"{prefix}: [{bar}] {percentage}% ({current}/{total})"

def safe_get_nested_value(data: Dict, keys: list, default: Any = None) -> Any:
    """Safely get nested dictionary value."""
    try:
        for key in keys:
            data = data[key]
        return data
    except (KeyError, TypeError, IndexError):
        return default

def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """Truncate text to maximum length with suffix."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def calculate_token_estimate(text: str) -> int:
    """Rough estimate of token count for text (approximation)."""
    # Rough approximation: 1 token ≈ 4 characters for English text
    return len(text) // 4

def format_workflow_summary(state: Dict[str, Any]) -> str:
    """Format a workflow state summary for display."""
    summary_lines = []

    # Basic info
    if 'status' in state:
        summary_lines.append(f"Status: {state['status']}")

    if 'timestamp' in state:
        summary_lines.append(f"Timestamp: {state['timestamp']}")

    # Task information
    crew_tasks = safe_get_nested_value(state, ['crew_tasks'], [])
    if crew_tasks:
        summary_lines.append(f"Tasks Completed: {len(crew_tasks)}")

    crew_results = safe_get_nested_value(state, ['crew_results'], [])
    if crew_results:
        summary_lines.append(f"Results Generated: {len(crew_results)}")

    # Content summaries
    for key in ['user_request', 'analysis_result', 'final_synthesis']:
        value = safe_get_nested_value(state, [key])
        if value:
            truncated = truncate_text(str(value), 100)
            summary_lines.append(f"{key.replace('_', ' ').title()}: {truncated}")

    return "\n".join(summary_lines)

def create_error_message(error: Exception, context: str = "") -> str:
    """Create a formatted error message."""
    error_type = type(error).__name__
    error_msg = str(error)

    message = f"Error in {context}: {error_type}"
    if error_msg:
        message += f" - {error_msg}"

    return message

def validate_workflow_state(state: Dict[str, Any], required_keys: list) -> tuple[bool, list]:
    """Validate that workflow state contains required keys."""
    missing_keys = []

    for key in required_keys:
        if key not in state:
            missing_keys.append(key)

    is_valid = len(missing_keys) == 0
    return is_valid, missing_keys

def merge_agent_contexts(*contexts) -> Dict[str, Any]:
    """Merge multiple agent contexts into one."""
    merged = {}

    for context in contexts:
        if isinstance(context, dict):
            merged.update(context)

    return merged

def log_workflow_step(step_name: str, data: Optional[Dict] = None):
    """Log a workflow step with optional data."""
    import datetime

    timestamp = datetime.datetime.now().isoformat()
    print(f"[{timestamp}] {step_name}")

    if data:
        for key, value in data.items():
            if isinstance(value, str) and len(value) > 100:
                value = value[:100] + "..."
            print(f"  {key}: {value}")

def get_available_models() -> list:
    """Get list of available OpenRouter models for agents."""
    return [
        "z-ai/glm-4.5-air:free",  # Free
        "anthropic/claude-3-haiku",  # Free
        "microsoft/wizardlm-2-8x22b",  # Free
        "anthropic/claude-3-sonnet",
        "openai/gpt-4",
        "openai/gpt-3.5-turbo",
        "google/gemini-pro",
        "meta-llama/llama-2-70b-chat"
    ]

def estimate_cost(tokens_used: int, model: str = "z-ai/glm-4.5-air:free") -> float:
    """Estimate API cost based on tokens used via OpenRouter (rough approximation)."""
    # Approximate costs per 1K tokens via OpenRouter (as of 2024)
    # Note: Many models have free tiers or very low costs
    costs = {
        "z-ai/glm-4.5-air:free": 0.0,  # Free
        "anthropic/claude-3-haiku": 0.0,  # Often free
        "microsoft/wizardlm-2-8x22b": 0.0,  # Free
        "anthropic/claude-3-sonnet": 0.015,  # $0.015 per 1K tokens
        "openai/gpt-4": 0.03,  # $0.03 per 1K tokens
        "openai/gpt-3.5-turbo": 0.002,  # $0.002 per 1K tokens
        "google/gemini-pro": 0.0,  # Often free
        "meta-llama/llama-2-70b-chat": 0.001,  # $0.001 per 1K tokens
    }

    cost_per_1k = costs.get(model, 0.01)  # Default fallback
    return (tokens_used / 1000) * cost_per_1k
