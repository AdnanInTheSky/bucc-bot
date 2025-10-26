import discord
from discord.ext import commands
import asyncio
import os
import logging

import config
from utils.messageForwarder import handle_message
from utils.keep_alive import keep_alive
from utils.interaction_logger import log_message

# Configure logging for the bot
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Set discord.py logging to INFO to see connection issues
discord.utils.setup_logging(level=logging.INFO)

# Define the roles that should exist in every server
REQUIRED_ROLES = [
    "Governing Body",
    "Executive Body",
    "Senior Executive",
    "Alumni",
    "Faculty",
    "C&M",
    "Creative",
    "Event",
    "Finance",
    "HR",
    "Press Release",
    "R&D",
]

# Define the channels that should exist in every server
REQUIRED_CHANNELS = [
    "automatic-verification",
    "notification",
    "message-forward-by-bot"
]

# Initialize keep-alive functionality to keep the bot running
keep_alive()

# Configure bot intents for necessary events and data access
intents = discord.Intents.default()
intents.message_content = True  # Required for accessing message content
intents.members = (
    True  # Required for accessing member information (e.g., roles, nicknames)
)

# Initialize the bot with a command prefix and specified intents with retry settings
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    max_messages=10000,  # Limit message cache
    heartbeat_timeout=60.0,  # Increase heartbeat timeout
    guild_ready_timeout=5.0  # Adjust guild ready timeout
)


@bot.event
async def on_ready():
    """
    Event handler that runs when the bot successfully connects to Discord.

    This function performs initial setup tasks for each guild the bot is a member of,
    including creating required roles and sending the verification button.
    """
    logger.info(f"Logged in as {bot.user}")
    for guild in bot.guilds:
        logger.info(f"Bot is ready in guild: {guild.name} (ID: {guild.id})")
        await log_message(bot, f"Logged in as {bot.user}", guild.id)

        # Ensure all required roles exist in the guild
        await _ensure_required_roles(guild)

        # Ensure all required channels exist in the guild
        await _ensure_required_channels(guild)

        # Send the verification button to the designated channel
        await _send_verification_button(guild)


@bot.event
async def on_member_join(member: discord.Member):
    """
    Event handler that runs when a new member joins the server.
    Sends a welcome message to guide them through verification.
    """
    # Find the verification channel
    verification_channel = discord.utils.get(member.guild.text_channels, name="automatic-verification")

    if verification_channel:
        embed = discord.Embed(
            title=f"👋 Welcome to BUCC, {member.name}!",
            description=(
                f"Hey {member.mention}! We're excited to have you join the **Brac University Computer Club**!\n\n"
                f"To unlock all channels and get your roles, please head over to {verification_channel.mention} "
                "and click the **Verify Me** button.\n\n"
                "See you around! 🚀"
            ),
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Brac University Computer Club", icon_url=member.guild.icon.url if member.guild.icon else None)

        # Try to send a DM to the new member
        try:
            await member.send(embed=embed)
            logger.info(f"Sent welcome DM to {member}")
        except discord.Forbidden:
            # If DM fails, send in a welcome channel or log it
            logger.warning(f"Could not send DM to {member}, they likely have DMs disabled")
            # Optionally send to a welcome channel instead
            welcome_channel = discord.utils.get(member.guild.text_channels, name="general")
            if welcome_channel:
                await welcome_channel.send(embed=embed)

    await log_message(bot, f"👋 {member.mention} joined the server.", member.guild.id)


@bot.event
async def on_message(message: discord.Message):
    """
    Event handler that runs when a message is sent in any channel the bot can access.

    This function is used for message forwarding functionality.
    """
    await handle_message(
        bot, message
    )  # Call the message handler from messageForwarder.py
    await bot.process_commands(message)


async def _ensure_required_roles(guild: discord.Guild):
    """
    Ensures that all predefined required roles exist in the given guild.
    If a role does not exist, the bot attempts to create it.

    Args:
        guild: The Discord guild (server) to check roles in.
    """
    for role_name in REQUIRED_ROLES:
        if discord.utils.get(guild.roles, name=role_name) is None:
            try:
                await guild.create_role(
                    name=role_name
                )  # Create role without specific permissions or color
                logger.info(f"Created role '{role_name}' in {guild.name}.")
                await log_message(
                    bot, f"Created role '{role_name}' in {guild.name}.", guild.id
                )
            except discord.Forbidden:
                logger.warning(
                    f"Missing permissions to create role '{role_name}' in {guild.name}."
                )
                await log_message(
                    bot,
                    f"Missing permissions to create role '{role_name}' in {guild.name}.",
                    guild.id,
                )
            except Exception as e:
                logger.error(f"Error creating role '{role_name}' in {guild.name}: {e}")
                await log_message(
                    bot,
                    f"Error creating role '{role_name}' in {guild.name}: {e}",
                    guild.id,
                )


async def _ensure_required_channels(guild: discord.Guild):
    """
    Ensures that all predefined required text channels exist in the given guild.
    If a channel does not exist, the bot attempts to create it.

    Args:
        guild: The Discord guild (server) to check channels in.
    """
    for channel_name in REQUIRED_CHANNELS:
        if discord.utils.get(guild.text_channels, name=channel_name) is None:
            try:
                await guild.create_text_channel(name=channel_name)
                logger.info(f"Created channel '{channel_name}' in {guild.name}.")
                await log_message(
                    bot, f"Created channel '{channel_name}' in {guild.name}.", guild.id
                )
            except discord.Forbidden:
                logger.warning(
                    f"Missing permissions to create channel '{channel_name}' in {guild.name}."
                )
                await log_message(
                    bot,
                    f"Missing permissions to create channel '{channel_name}' in {guild.name}.",
                    guild.id,
                )
            except Exception as e:
                logger.error(f"Error creating channel '{channel_name}' in {guild.name}: {e}")
                await log_message(
                    bot,
                    f"Error creating channel '{channel_name}' in {guild.name}: {e}",
                    guild.id,
                )


async def _send_verification_button(guild: discord.Guild):
    """
    Sends the verification button to the 'automatic-verification' channel in the given guild.

    Args:
        guild: The Discord guild (server) to send the button to.
    """
    channel = discord.utils.get(guild.text_channels, name="automatic-verification")

    if channel:
        from cogs.verification.verification import VerifyMeButton

        # Create a beautiful embed for the verification message
        embed = discord.Embed(
            title="🎓 Welcome to BUCC!",
            description=(
                "Welcome to the **Brac University Computer Club** Discord server!\n\n"
                "To get started and access all channels, please verify yourself by clicking the button below.\n\n"
                "**What happens when you verify?**\n"
                "✅ Your roles will be assigned based on your department and designation\n"
                "✅ Your nickname will be updated to match our format\n"
                "✅ You'll gain access to member-exclusive channels\n\n"
                "Click **Verify Me** to begin!"
            ),
            color=discord.Color.blue()
        )
        embed.set_footer(text="Brac University Computer Club", icon_url=guild.icon.url if guild.icon else None)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

        view = VerifyMeButton(bot)
        await channel.send(embed=embed, view=view)
        logger.info(f"Verification button sent to {channel.name} in {guild.name}.")
        await log_message(bot, "Bot is ready and verification button sent.", guild.id)
    else:
        error_message = f"Channel with name 'automatic-verification' not found in guild {guild.name}"
        logger.warning(error_message)
        await log_message(bot, error_message, guild.id)


async def load_cogs():
    """Finds and loads all cogs in the 'cogs' directory, including subdirectories."""
    cogs_dir = "cogs"
    for root, dirs, files in os.walk(cogs_dir):
        for filename in files:
            # Load python files that are not __init__.py
            if filename == "cog.py" or filename == "verification.py": # Only load files intended as cogs
                # Construct the module path from the file path
                # e.g., cogs/role_management/cog.py -> cogs.role_management.cog
                path = os.path.join(root, filename)
                # To create the module path, remove the base 'cogs' dir, remove .py, and replace slashes with dots
                module_path = path.replace(os.sep, ".")[:-3]
                try:
                    await bot.load_extension(module_path)
                    logger.info(f"Successfully loaded cog: {module_path}")
                except Exception as e:
                    logger.error(f"Failed to load cog {module_path}: {e}", exc_info=True)

async def main():
    """
    The main asynchronous function that initializes and starts the bot.

    This function loads all cogs and then starts the Discord bot using the token
    from the configuration.
    """
    max_retries = 5
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            async with bot:
                await load_cogs()
                # Start the bot with the Discord token from config
                await bot.start(config.DISCORD_BOT_TOKEN)
                break  # If successful, exit retry loop
        except discord.ConnectionClosed as e:
            logger.error(f"Connection closed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logger.critical("Max retries reached. Bot failed to start.")
                raise
        except discord.HTTPException as e:
            if e.status == 1015 or "cloudflare" in str(e).lower():
                logger.error(f"Cloudflare rate limit hit (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    logger.info(f"Waiting {retry_delay} seconds before retry...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.critical("Persistent Cloudflare blocking. Check your IP or contact Render support.")
                    raise
            else:
                raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except config.ConfigError as e:
        logger.critical(f"Configuration error: {e}")
    except Exception as e:
        logger.critical(f"An unhandled error occurred: {e}")
