import os
from cogs.interaction_logger import log_message

async def handle_message(bot, message):
    """Function to handle message forwarding functionality."""
    if message.author.bot:
        return  # Ignore messages from bots

    # Check if the message is in the specific channel (replace with your channel ID)
    specific_channel_id = int(os.getenv('FORWARDING_CHANNEL_ID'))
    if message.channel.id != specific_channel_id:
        return

    # Check if the message mentions a channel
    if message.channel_mentions:
        mentioned_channel = message.channel_mentions[0]  # Get the first mentioned channel
        content_to_forward = message.content.replace(f"<#{mentioned_channel.id}>", "").strip()

        # Prepare attachments (if any)
        files = [await attachment.to_file() for attachment in message.attachments]

        if content_to_forward or files:  # Ensure there's content or attachments to forward
            try:
                await mentioned_channel.send(content_to_forward, files=files)
                await log_message(
                    bot,
                    f"Message forwarded to {mentioned_channel.mention} by {message.author.mention}: {content_to_forward or 'No text'}"
                )
            except Exception as e:
                await log_message(bot, f"Failed to forward message: {e}")
        else:
            await message.channel.send(
                "Please provide a message or attachment to forward along with the channel mention.",
                delete_after=10
            )

    # Process other commands if any
    await bot.process_commands(message)  # Process other commands if any