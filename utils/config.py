"""
Configuration management for the AI Agent Workshop.
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path
from .helpers import load_environment_variables, validate_api_key

class WorkshopConfig:
    """Configuration class for workshop settings."""

    def __init__(self):
        self._config = {}
        self._load_config()

    def _load_config(self):
        """Load configuration from environment and defaults."""
        try:
            env_vars = load_environment_variables()
            self._config.update(env_vars)
        except ValueError as e:
            print(f"Warning: {e}")
            # Continue with defaults

        # Set defaults
        self._config.setdefault('SAMBA_MODEL', 'gpt-oss-120b')
        self._config.setdefault('WORKSHOP_DEBUG', 'false')
        self._config.setdefault('MAX_TOKENS', '4000')
        self._config.setdefault('TEMPERATURE', '0.7')

        # Convert string values to appropriate types
        self._convert_types()

    def _convert_types(self):
        """Convert string config values to appropriate types."""
        # Boolean conversions
        bool_keys = ['WORKSHOP_DEBUG']
        for key in bool_keys:
            if key in self._config:
                self._config[key] = str(self._config[key]).lower() in ('true', '1', 'yes', 'on')

        # Integer conversions
        int_keys = ['MAX_TOKENS']
        for key in int_keys:
            if key in self._config:
                try:
                    self._config[key] = int(self._config[key])
                except ValueError:
                    print(f"Warning: Invalid integer value for {key}, using default")
                    self._config[key] = 4000

        # Float conversions
        float_keys = ['TEMPERATURE']
        for key in float_keys:
            if key in self._config:
                try:
                    self._config[key] = float(self._config[key])
                except ValueError:
                    print(f"Warning: Invalid float value for {key}, using default")
                    self._config[key] = 0.7

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        """Set configuration value."""
        self._config[key] = value

    def validate(self) -> tuple[bool, list]:
        """Validate configuration."""
        errors = []

        # Check required API key
        api_key = self.get('SAMBA_API_KEY')
        if not api_key:
            errors.append("SAMBA_API_KEY is required")
        elif not validate_api_key(api_key):
            errors.append("SAMBA_API_KEY format is invalid")

        # Check model
        model = self.get('SAMBA_MODEL')
        # SambaNova supports many models, so we'll just check it's not empty
        if not model:
            errors.append("SAMBA_MODEL is required")

        # Check temperature range
        temp = self.get('TEMPERATURE')
        if temp is not None and not (0.0 <= temp <= 2.0):
            errors.append("TEMPERATURE must be between 0.0 and 2.0")

        # Check max tokens
        max_tokens = self.get('MAX_TOKENS')
        if max_tokens is not None and max_tokens <= 0:
            errors.append("MAX_TOKENS must be greater than 0")

        is_valid = len(errors) == 0
        return is_valid, errors

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return self._config.copy()

    def save_to_env_file(self, env_file_path: str = ".env"):
        """Save configuration to .env file."""
        env_path = Path(env_file_path)

        # Read existing .env file if it exists
        existing_content = {}
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            existing_content[key.strip()] = value.strip()

        # Update with current config
        for key, value in self._config.items():
            if key.startswith(('SAMBA_', 'WORKSHOP_', 'MAX_TOKENS', 'TEMPERATURE')):  # Save relevant configs
                existing_content[key] = str(value)

        # Write back to file
        with open(env_path, 'w') as f:
            f.write("# AI Agent Workshop Configuration\n")
            f.write("# Generated automatically - do not edit manually\n\n")

            for key, value in sorted(existing_content.items()):
                f.write(f"{key}={value}\n")

    def get_agent_config(self) -> Dict[str, Any]:
        """Get configuration specifically for agents."""
        model = self.get('SAMBA_MODEL')
        # No prefix needed for SambaNova
        return {
            'model': model,
            'temperature': self.get('TEMPERATURE'),
            'max_tokens': self.get('MAX_TOKENS'),
            'api_key': self.get('SAMBA_API_KEY'),
            'api_base': 'https://api.sambanova.ai/v1',
            'max_retries': 3,  # Add retry logic
            'retry_delay': 1.0,  # Base delay in seconds
        }

    def get_workflow_config(self) -> Dict[str, Any]:
        """Get configuration for workflow execution."""
        return {
            'debug': self.get('WORKSHOP_DEBUG'),
            'max_iterations': self.get('MAX_ITERATIONS', 10),
            'timeout_seconds': self.get('TIMEOUT_SECONDS', 300),
        }

    def __str__(self) -> str:
        """String representation of config (without sensitive data)."""
        config_copy = self._config.copy()

        # Mask sensitive information
        if 'GROQ_API_KEY' in config_copy:
            key = config_copy['GROQ_API_KEY']
            if len(key) > 10:
                config_copy['GROQ_API_KEY'] = key[:6] + '*' * (len(key) - 10) + key[-4:]

        return f"WorkshopConfig({config_copy})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return self.__str__()

# Global configuration instance
_config_instance: Optional[WorkshopConfig] = None

def get_config() -> WorkshopConfig:
    """Get the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = WorkshopConfig()
    return _config_instance

def reload_config():
    """Reload the global configuration."""
    global _config_instance
    _config_instance = WorkshopConfig()

def validate_config() -> tuple[bool, list]:
    """Validate the current configuration."""
    config = get_config()
    return config.validate()

def setup_config_interactive():
    """Interactive configuration setup."""
    print("AI Agent Workshop - Configuration Setup")
    print("=" * 45)

    config = get_config()

    # Check if API key is already set
    if config.get('SAMBA_API_KEY'):
        print("✓ SambaNova API key is already configured")
    else:
        print("SambaNova API key is required")
        print("Get your API key from: https://sambanova.ai")
        api_key = input("Enter your SambaNova API key: ").strip()
        if api_key:
            config.set('SAMBA_API_KEY', api_key)
            print("✓ API key configured")
        else:
            print("❌ API key is required")
            return False

    # Optional: Configure model
    current_model = config.get('GROQ_MODEL', 'openai/gpt-oss-20b:free')
    print(f"\nCurrent model: {current_model}")
    change_model = input("Change model? (y/N): ").strip().lower()
    if change_model == 'y':
        models = [
            'gemma2-9b-it', #Free
            'llama3-8b-8192',  # Free
            'llama3-70b-8192',  # Free
            'mixtral-8x7b-32768',  # Free
            'llama-3.1-8b-instant',
            'llama-3.1-70b-versatile',
            'llama-3.1-405b-inference'
        ]
        print("Available models (some free, some paid):")
        for i, model in enumerate(models, 1):
            free_indicator = " (Free)" if i <= 3 else ""
            print(f"  {i}. {model}{free_indicator}")
        choice = input("Select model (1-7): ").strip()
        try:
            index = int(choice) - 1
            if 0 <= index < len(models):
                config.set('GROQ_MODEL', models[index])
                print(f"✓ Model set to {models[index]}")
        except ValueError:
            print("Invalid choice, keeping current model")

    # Validate configuration
    is_valid, errors = config.validate()
    if is_valid:
        print("\n✅ Configuration is valid!")
        save = input("Save configuration to .env file? (Y/n): ").strip().lower()
        if save != 'n':
            config.save_to_env_file()
            print("✓ Configuration saved to .env file")
        return True
    else:
        print("\n❌ Configuration validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False

# Initialize config on import
config = get_config()
