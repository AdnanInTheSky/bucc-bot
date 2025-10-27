"""
Message forwarding utilities.

Handles forwarding messages from designated channels to mentioned channels.
"""

import discord
import logging

from constants import ChannelNames
from utils.interaction_logger import log_message
from utils.discord_helpers import get_text_channel

logger = logging.getLogger(__name__)


async def handle_message(bot: discord.Client, message: discord.Message) -> None:
    """
    Forward messages from the message-forward-by-bot channel to mentioned channels.

    Messages must mention a channel and can include text content and/or attachments.

    Args:
        bot: The Discord bot instance
        message: The message object that triggered the event
    """
    forwarding_channel = get_text_channel(message.guild, ChannelNames.MESSAGE_FORWARD)

    if message.author.bot or not forwarding_channel:
        return

    if message.channel.id != forwarding_channel.id:
        return

    if not message.channel_mentions:
        return

    mentioned_channel = message.channel_mentions[0]
    content_to_forward = message.content.replace(f"<#{mentioned_channel.id}>", "").strip()
    files = [await attachment.to_file() for attachment in message.attachments]

    if not (content_to_forward or files):
        await message.channel.send(
            "Please provide a message or attachment to forward along with the channel mention.",
            delete_after=10,
        )
        return

    try:
        await mentioned_channel.send(content_to_forward, files=files)
        logger.info(f"Message forwarded to {mentioned_channel.name} by {message.author.name}")

        await log_message(
            bot,
            f"Message forwarded to {mentioned_channel.mention} by {message.author.mention}: {content_to_forward or 'No text'}",
            message.guild.id,
        )

    except discord.Forbidden:
        logger.warning(
            f"Bot lacks permissions to send messages to {mentioned_channel.name} in {message.guild.name}"
        )
        await message.channel.send(
            "I don't have permission to send messages to that channel.",
            delete_after=10,
        )

    except discord.HTTPException as e:
        logger.error(f"HTTP error forwarding message: {e}")
        await message.channel.send(
            "An error occurred while forwarding the message.",
            delete_after=10,
        )

    except Exception as e:
        logger.exception(f"Failed to forward message: {e}")
        await log_message(bot, f"Failed to forward message: {e}", message.guild.id)
