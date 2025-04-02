import os
import discord
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

async def log_message(bot, message: str):
    # Fetch the log channel
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(message)
    else:
        print(f"Log channel with ID {LOG_CHANNEL_ID} not found.")
