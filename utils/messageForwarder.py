import config
from utils.interaction_logger import log_message
import discord
import logging

logger = logging.getLogger(__name__)


async def handle_message(bot: discord.Client, message: discord.Message):
    """
    Handles message forwarding functionality.

    Messages from a specific forwarding channel that mention another channel
    will be forwarded to the mentioned channel.

    Args:
        bot: The Discord bot instance.
        message: The message object that triggered the event.
    """
    # Find the forwarding channel by name
    forwarding_channel = discord.utils.get(message.guild.text_channels, name='message-forward-by-bot')

    # Ignore messages from bots or if forwarding channel is not found
    if message.author.bot or not forwarding_channel:
        return

    # Check if the message is in the specific forwarding channel
    if message.channel.id != forwarding_channel.id:
        return

    # Check if the message mentions a channel
    if message.channel_mentions:
        mentioned_channel = message.channel_mentions[
            0
        ]  # Get the first mentioned channel
        content_to_forward = message.content.replace(
            f"<#{mentioned_channel.id}>", ""
        ).strip()

        # Prepare attachments (if any)
        files = [await attachment.to_file() for attachment in message.attachments]

        # Ensure there's content or attachments to forward
        if content_to_forward or files:
            try:
                await mentioned_channel.send(content_to_forward, files=files)
                logger.info(
                    f"Message forwarded to {mentioned_channel.name} by {message.author.name}."
                )
                await log_message(
                    bot,
                    f"Message forwarded to {mentioned_channel.mention} by {message.author.mention}: {content_to_forward or 'No text'}",
                    message.guild.id,
                )
            except discord.Forbidden:
                logger.warning(
                    f"Bot lacks permissions to send messages to {mentioned_channel.name} in {message.guild.name}."
                )
                await message.channel.send(
                    "I don't have permission to send messages to that channel.",
                    delete_after=10,
                )
            except discord.HTTPException as e:
                logger.error(f"HTTP error forwarding message: {e}")
                await message.channel.send(
                    "An error occurred while forwarding the message.", delete_after=10
                )
            except Exception as e:
                logger.exception(f"Failed to forward message: {e}")
                await log_message(
                    bot, f"Failed to forward message: {e}", message.guild.id
                )
        else:
            await message.channel.send(
                "Please provide a message or attachment to forward along with the channel mention.",
                delete_after=10,
            )

    # Process other commands if any (e.g., if the message is also a bot command)
    await bot.process_commands(message)
