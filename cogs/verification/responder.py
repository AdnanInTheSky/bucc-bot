import discord
import logging
from utils.interaction_logger import log_message

logger = logging.getLogger(__name__)

async def handle_user_not_found(bot: discord.ext.commands.Bot, interaction: discord.Interaction):
    """Handles the case where the user is not found in the database."""
    await interaction.followup.send(
        "Your Discord username isn't updated in our database. Kindly fill up the form. "
        "Form Link: [Click Here](https://forms.gle/t3HiKSuEXaF3PwdF7)",
        ephemeral=True,
    )
    await log_message(
        bot,
        f"❗ {interaction.user.mention} not found in the database.",
        interaction.guild.id,
    )
    logger.warning(f"User not found in database: {interaction.user}")

async def handle_member_not_found(bot: discord.ext.commands.Bot, interaction: discord.Interaction):
    """Handles the case where the member is not found in the guild."""
    await interaction.followup.send(
        "Could not find you in the server.", ephemeral=True
    )
    await log_message(
        bot,
        f"Member {interaction.user.mention} not found in the guild.",
        interaction.guild.id,
    )
    logger.error(
        f"Member not found in guild, but interaction was received: {interaction.user}"
    )

async def handle_generic_error(bot: discord.ext.commands.Bot, interaction: discord.Interaction, error: Exception):
    """Handles generic, unexpected errors."""
    logger.exception(
        f"An unexpected error occurred during verification for {interaction.user}: {error}"
    )
    await interaction.followup.send(
        "An unexpected error occurred. Please try again later.", ephemeral=True
    )
    await log_message(
        bot,
        f"An unexpected error occurred for {interaction.user.mention}.",
        interaction.guild.id,
    )

async def handle_success(bot: discord.ext.commands.Bot, interaction: discord.Interaction):
    """Handles the successful verification case."""
    await interaction.followup.send(
        "You have been verified and your roles have been updated.",
        ephemeral=True,
    )
    await log_message(
        bot,
        f"✅ {interaction.user.mention} has been verified and roles updated.",
        interaction.guild.id,
    )
    logger.info(f"Successfully verified and updated user: {interaction.user}")

async def handle_permission_error(bot: discord.ext.commands.Bot, interaction: discord.Interaction):
    """Handles the case where the bot lacks permissions."""
    logger.warning(
        f"Bot lacks permissions to modify roles/nickname for {interaction.user.mention} in {interaction.guild.name}."
    )
    await interaction.followup.send(
        "I don't have the necessary permissions to update your roles or nickname.",
        ephemeral=True,
    )

async def handle_http_error(bot: discord.ext.commands.Bot, interaction: discord.Interaction, error: discord.HTTPException):
    """Handles Discord HTTP exceptions."""
    logger.exception(
        f"An HTTP error occurred while updating {interaction.user.mention}: {error}"
    )
    await interaction.followup.send(
        "An error occurred while communicating with Discord.", ephemeral=True
    )
