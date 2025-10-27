"""
Configuration management for the BUCC Discord Bot.

Loads environment variables and provides centralized access to bot configuration.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class ConfigError(Exception):
    """Raised when required environment variables are missing."""

    pass


def get_env_var(name: str) -> str:
    """
    Retrieve required environment variable.

    Args:
        name: Environment variable name

    Returns:
        Environment variable value

    Raises:
        ConfigError: If environment variable is not set
    """
    value = os.getenv(name)
    if value is None:
        raise ConfigError(f"Environment variable '{name}' not set")
    return value


DISCORD_BOT_TOKEN: str = get_env_var("DISCORD_BOT_TOKEN")
GOOGLE_SHEET_ID: str = get_env_var("GOOGLE_SHEET_ID")
