"""
Interaction logging utilities.

Sends formatted log messages to designated notification channels.
"""

import discord
import logging
from datetime import datetime
from typing import Literal

from constants import ChannelNames
from utils.discord_helpers import get_text_channel

logger = logging.getLogger(__name__)

LogType = Literal["success", "error", "warning", "info"]


async def log_message(
    bot: discord.Client, message: str, guild_id: int, log_type: LogType = "info"
) -> None:
    """
    Log a message to the notification channel with rich embeds.

    Args:
        bot: The Discord bot instance
        message: The message to log
        guild_id: The guild ID where the message should be logged
        log_type: Type of log - "success", "error", "warning", or "info"
    """
    guild = bot.get_guild(guild_id)
    if not guild:
        logger.warning(f"Attempted to log to non-existent guild ID: {guild_id}")
        return

    log_channel = get_text_channel(guild, ChannelNames.NOTIFICATION)
    if not log_channel:
        logger.warning(f"Notification channel not found in {guild.name}")
        return

    color_map = {
        "success": discord.Color.green(),
        "error": discord.Color.red(),
        "warning": discord.Color.orange(),
        "info": discord.Color.blue(),
    }

    emoji_map = {
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
        "info": "ℹ️",
    }

    color = color_map.get(log_type, discord.Color.blue())
    emoji = emoji_map.get(log_type, "ℹ️")

    embed = discord.Embed(
        description=message, color=color, timestamp=datetime.utcnow()
    )
    embed.set_footer(text=f"{emoji} Bot Log")

    try:
        await log_channel.send(embed=embed)
    except discord.Forbidden:
        logger.warning(f"Bot lacks permissions to send log messages in {guild.name}")
    except discord.HTTPException as e:
        logger.error(f"HTTP error sending log message to {guild.name}: {e}")
