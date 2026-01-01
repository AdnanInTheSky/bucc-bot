"""
BUCC Discord Bot - Main entry point.

A Discord bot for the Brac University Computer Club that automates member
verification, role assignment, and server management.
"""

import discord
from discord.ext import commands
import asyncio
import os
import logging

import config
from constants import REQUIRED_ROLES, REQUIRED_CHANNELS, ChannelNames
from utils.message_forwarder import handle_message
from utils.interaction_logger import log_message
from utils.discord_helpers import ensure_role_exists, ensure_text_channel_exists, get_text_channel
from webserver import keep_alive

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

discord.utils.setup_logging(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 5
MESSAGE_CACHE_SIZE = 10000
HEARTBEAT_TIMEOUT = 60.0
GUILD_READY_TIMEOUT = 5.0

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    max_messages=MESSAGE_CACHE_SIZE,
    heartbeat_timeout=HEARTBEAT_TIMEOUT,
    guild_ready_timeout=GUILD_READY_TIMEOUT,
)


@bot.event
async def on_ready() -> None:
    """Initialize server setup when bot connects to Discord."""
    logger.info(f"Logged in as {bot.user}")
    for guild in bot.guilds:
        logger.info(f"Bot is ready in guild: {guild.name} (ID: {guild.id})")
        await log_message(bot, f"Logged in as {bot.user}", guild.id)

        await _ensure_required_roles(guild)
        await _ensure_required_channels(guild)
        await _send_verification_button(guild)


@bot.event
async def on_member_join(member: discord.Member) -> None:
    """Send welcome message when new member joins."""
    verification_channel = get_text_channel(member.guild, ChannelNames.VERIFICATION)

    if not verification_channel:
        logger.warning(f"Verification channel not found in {member.guild.name}")
        return

    embed = discord.Embed(
        title=f"👋 Welcome to BUCC, {member.name}!",
        description=(
            f"Hey {member.mention}! We're excited to have you join the **Brac University Computer Club**!\n\n"
            "**📝 Step 1: Fill out the registration form**\n"
            f"Please complete [this form](<https://forms.gle/t3HiKSuEXaF3PwdF7>) using your **G Suite account**.\n"
            f"• Discord Username: `{member.name}` (copy this exactly)\n"
            f"• Nickname: Use your first or last name\n\n"
            "**✅ Step 2: Verify yourself**\n"
            f"After submitting the form, head over to {verification_channel.mention} and click the **Verify Me** button to get your roles!\n\n"
            "See you around! 🚀"
        ),
        color=discord.Color.blue(),
    )
    embed.set_thumbnail(url=member.display_avatar.url)

    if member.guild.icon:
        embed.set_footer(
            text="Brac University Computer Club", icon_url=member.guild.icon.url
        )

    try:
        await member.send(embed=embed)
        logger.info(f"Sent welcome DM to {member}")
    except discord.Forbidden:
        logger.warning(f"Could not send DM to {member}, they likely have DMs disabled")
        welcome_channel = get_text_channel(member.guild, ChannelNames.GENERAL)
        if welcome_channel:
            await welcome_channel.send(embed=embed)

    await log_message(bot, f"👋 {member.mention} joined the server", member.guild.id)


@bot.event
async def on_message(message: discord.Message) -> None:
    """Handle incoming messages for forwarding and commands."""
    await handle_message(bot, message)
    await bot.process_commands(message)


async def _ensure_required_roles(guild: discord.Guild) -> None:
    """Ensure all required roles exist in the guild, creating if necessary."""
    for role_name in REQUIRED_ROLES:
        await ensure_role_exists(guild, role_name)


async def _ensure_required_channels(guild: discord.Guild) -> None:
    """Ensure all required channels exist in the guild, creating if necessary."""
    for channel_name in REQUIRED_CHANNELS:
        await ensure_text_channel_exists(guild, channel_name)


async def _send_verification_button(guild: discord.Guild) -> None:
    """Send verification button to the verification channel."""
    channel = get_text_channel(guild, ChannelNames.VERIFICATION)

    if not channel:
        error_message = f"Verification channel not found in guild {guild.name}"
        logger.warning(error_message)
        await log_message(bot, error_message, guild.id)
        return

    from cogs.verification.verification import VerifyMeButton

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
        color=discord.Color.blue(),
    )

    if guild.icon:
        embed.set_footer(text="Brac University Computer Club", icon_url=guild.icon.url)
        embed.set_thumbnail(url=guild.icon.url)

    view = VerifyMeButton(bot)
    await channel.send(embed=embed, view=view)
    logger.info(f"Verification button sent to {channel.name} in {guild.name}")
    await log_message(bot, "Bot is ready and verification button sent", guild.id)


async def load_cogs() -> None:
    """Discover and load all cogs from the cogs directory."""
    from pathlib import Path

    cogs_directory = Path("cogs")
    cog_files = {"cog.py", "verification.py"}

    for python_file in cogs_directory.rglob("*.py"):
        if python_file.name in cog_files:
            module_path = str(python_file.with_suffix("")).replace(os.sep, ".")

            try:
                await bot.load_extension(module_path)
                logger.info(f"Loaded cog: {module_path}")
            except (ImportError, discord.errors.ExtensionError) as e:
                logger.error(f"Failed to load cog {module_path}: {e}", exc_info=True)
            except Exception as e:
                logger.critical(f"Unexpected error loading cog {module_path}: {e}", exc_info=True)


async def main() -> None:
    """Initialize and start the bot with retry logic for connection failures."""
    retry_delay = RETRY_DELAY_SECONDS

    for attempt in range(MAX_RETRIES):
        try:
            async with bot:
                await load_cogs()
                await bot.start(config.DISCORD_BOT_TOKEN)
                break
        except (discord.ConnectionClosed, discord.HTTPException) as e:
            error_type = "Connection closed" if isinstance(e, discord.ConnectionClosed) else "HTTP error"
            logger.error(f"{error_type} during startup (attempt {attempt + 1}/{MAX_RETRIES}): {e}")

            if attempt < MAX_RETRIES - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2
            else:
                logger.critical("Max retries reached. Check bot token and network connection")
                raise


if __name__ == "__main__":
    # Start web server for health checks (keeps bot alive on free hosting)
    keep_alive()
    logger.info("Health check web server started")

    try:
        asyncio.run(main())
    except config.ConfigError as e:
        logger.critical(f"Configuration error: {e}")
    except Exception as e:
        logger.critical(f"An unhandled error occurred: {e}")
