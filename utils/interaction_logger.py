import discord
import logging

logger = logging.getLogger(__name__)


async def log_message(bot: discord.Client, message: str, guild_id: int):
    """
    Logs a message to a designated log channel in a specific guild.

    The log channel is identified by its name 'notification'.

    Args:
        bot: The Discord bot instance.
        message: The string message to be logged.
        guild_id: The ID of the guild where the message should be logged.
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
            await log_channel.send(message)
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
