import discord
import logging
from utils.interaction_logger import log_message

logger = logging.getLogger(__name__)

async def handle_user_not_found(bot: discord.ext.commands.Bot, interaction: discord.Interaction):
    """Handles the case where the user is not found in the database."""
    embed = discord.Embed(
        title="❌ Verification Failed",
        description=(
            "We couldn't find your Discord username in our database.\n\n"
            "**What should you do?**\n"
            "Please fill out the BUCC membership form to register your Discord username.\n\n"
            "Once submitted, wait for the database to update (usually within 24 hours), then try verifying again."
        ),
        color=discord.Color.red()
    )
    embed.add_field(
        name="📝 Registration Form",
        value="[Click here to fill the form](https://forms.gle/t3HiKSuEXaF3PwdF7)",
        inline=False
    )
    embed.add_field(
        name="💡 Tip",
        value="Make sure your Discord username matches exactly what you entered in the form!",
        inline=False
    )
    embed.set_footer(text="Need help? Contact a BUCC admin")

    await interaction.followup.send(embed=embed, ephemeral=True)
    await log_message(
        bot,
        f"❗ {interaction.user.mention} not found in the database.",
        interaction.guild.id,
    )
    logger.warning(f"User not found in database: {interaction.user}")

async def handle_member_not_found(bot: discord.ext.commands.Bot, interaction: discord.Interaction):
    """Handles the case where the member is not found in the guild."""
    embed = discord.Embed(
        title="⚠️ Member Not Found",
        description=(
            "We encountered an error finding you in this server.\n\n"
            "This is unusual - please contact a server administrator for assistance."
        ),
        color=discord.Color.orange()
    )
    embed.set_footer(text="Error Code: MEMBER_NOT_FOUND")

    await interaction.followup.send(embed=embed, ephemeral=True)
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

    embed = discord.Embed(
        title="❌ Unexpected Error",
        description=(
            "Something went wrong during the verification process.\n\n"
            "**What you can do:**\n"
            "• Wait a few minutes and try clicking **Verify Me** again\n"
            "• If the problem persists, please contact a BUCC admin\n\n"
            "The error has been logged and our team will look into it."
        ),
        color=discord.Color.red()
    )
    embed.set_footer(text="We apologize for the inconvenience")

    await interaction.followup.send(embed=embed, ephemeral=True)
    await log_message(
        bot,
        f"An unexpected error occurred for {interaction.user.mention}.",
        interaction.guild.id,
    )

async def handle_success(bot: discord.ext.commands.Bot, interaction: discord.Interaction):
    """Handles the successful verification case."""
    # Get the member to show their new nickname and roles
    member = interaction.guild.get_member(interaction.user.id)

    embed = discord.Embed(
        title="✅ Verification Successful!",
        description=(
            f"Welcome to BUCC, {member.mention}!\n\n"
            "Your verification is complete. You now have access to all member channels."
        ),
        color=discord.Color.green()
    )

    # Show their new nickname
    if member.nick:
        embed.add_field(
            name="📝 Your Nickname",
            value=f"`{member.nick}`",
            inline=False
        )

    # Show assigned roles (excluding @everyone)
    role_names = [role.mention for role in member.roles if role.name != "@everyone"]
    if role_names:
        embed.add_field(
            name="🎭 Assigned Roles",
            value=" ".join(role_names),
            inline=False
        )

    embed.add_field(
        name="🎉 What's Next?",
        value="Explore the server, introduce yourself, and connect with fellow BUCC members!",
        inline=False
    )
    embed.set_footer(text="Brac University Computer Club")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)

    await interaction.followup.send(embed=embed, ephemeral=True)
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

    embed = discord.Embed(
        title="🔒 Permission Error",
        description=(
            "The bot doesn't have the necessary permissions to update your roles or nickname.\n\n"
            "**This is a server configuration issue.**\n"
            "Please contact a server administrator to fix the bot's permissions."
        ),
        color=discord.Color.orange()
    )
    embed.add_field(
        name="🛠️ Required Permissions",
        value="• Manage Roles\n• Manage Nicknames",
        inline=False
    )
    embed.set_footer(text="Error Code: INSUFFICIENT_PERMISSIONS")

    await interaction.followup.send(embed=embed, ephemeral=True)

async def handle_http_error(bot: discord.ext.commands.Bot, interaction: discord.Interaction, error: discord.HTTPException):
    """Handles Discord HTTP exceptions."""
    logger.exception(
        f"An HTTP error occurred while updating {interaction.user.mention}: {error}"
    )

    embed = discord.Embed(
        title="⚠️ Communication Error",
        description=(
            "An error occurred while communicating with Discord.\n\n"
            "This is usually a temporary issue. Please try again in a few moments."
        ),
        color=discord.Color.orange()
    )
    embed.set_footer(text=f"Error Code: HTTP_{error.status if hasattr(error, 'status') else 'UNKNOWN'}")

    await interaction.followup.send(embed=embed, ephemeral=True)
