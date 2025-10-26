import discord
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


async def log_message(bot: discord.Client, message: str, guild_id: int, log_type: str = "info"):
    """
    Logs a message to a designated log channel in a specific guild with rich embeds.

    The log channel is identified by its name 'notification'.

    Args:
        bot: The Discord bot instance.
        message: The string message to be logged.
        guild_id: The ID of the guild where the message should be logged.
        log_type: Type of log - "success", "error", "warning", "info" (default: "info")
    """
    guild = bot.get_guild(guild_id)
    if not guild:
        logger.warning(
            f"Attempted to log message to non-existent guild with ID: {guild_id}"
        )
        return

    log_channel = discord.utils.get(guild.text_channels, name="notification")
    if log_channel:
        try:
            # Determine embed color and emoji based on log type
            color_map = {
                "success": discord.Color.green(),
                "error": discord.Color.red(),
                "warning": discord.Color.orange(),
                "info": discord.Color.blue()
            }

            emoji_map = {
                "success": "✅",
                "error": "❌",
                "warning": "⚠️",
                "info": "ℹ️"
            }

            # Auto-detect log type from message if not specified
            if log_type == "info":
                if "✅" in message or "verified" in message.lower():
                    log_type = "success"
                elif "❌" in message or "error" in message.lower() or "failed" in message.lower():
                    log_type = "error"
                elif "⚠️" in message or "warning" in message.lower() or "❗" in message:
                    log_type = "warning"

            color = color_map.get(log_type, discord.Color.blue())
            emoji = emoji_map.get(log_type, "ℹ️")

            # Create embed
            embed = discord.Embed(
                description=message,
                color=color,
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text=f"{emoji} Bot Log")

            await log_channel.send(embed=embed)
        except discord.Forbidden:
            logger.warning(
                f"Bot lacks permissions to send messages to log channel in {guild.name}."
            )
        except discord.HTTPException as e:
            logger.error(f"HTTP error sending log message to {guild.name}: {e}")
    else:
        logger.warning(
            f"Log channel with name 'notification' not found in guild {guild.name} (ID: {guild.id})."
        )
