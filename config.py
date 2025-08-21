import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


class ConfigError(Exception):
    """Custom exception for configuration-related errors."""

    pass


def get_env_var(name: str) -> str:
    """
    Retrieves the value of an environment variable.

    Args:
        name: The name of the environment variable.

    Returns:
        The value of the environment variable.

    Raises:
        ConfigError: If the environment variable is not set.
    """
    value = os.getenv(name)
    if value is None:
        raise ConfigError(f"Environment variable '{name}' not set.")
    return value


# --- Bot Configuration ---
# The Discord bot token, essential for the bot to connect to Discord.
DISCORD_BOT_TOKEN = get_env_var("DISCORD_BOT_TOKEN")

# The Google Sheet ID where member data is stored.
GOOGLE_SHEET_ID = get_env_var("GOOGLE_SHEET_ID")


