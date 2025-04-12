import discord
from discord.ext import commands
from discord.ui import View, Button
from dotenv import load_dotenv
import os

from cogs.gsheet import gSheet
from cogs.nickname_gen import nickname_gen
from cogs.role_gen import role_gen
from cogs.interaction_logger import log_message
from cogs.messageForwarder import handle_message

# Initialize keep-alive functionality
from cogs.keep_alive import keep_alive
keep_alive()

# Load environment variables from .env file
load_dotenv()

# Configure bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Initialize bot
bot = commands.Bot(command_prefix='!', intents=intents)


class VerifyMeButton(View):
    """A Discord UI View for the 'Verify Me' button."""

    def __init__(self):
        super().__init__(timeout=None)  # Disable timeout for the View

    @discord.ui.button(label="Verify Me", style=discord.ButtonStyle.primary)
    async def verify_me_button(self, interaction: discord.Interaction, button: Button):
        """Handles the 'Verify Me' button click."""
        await interaction.response.defer(ephemeral=True)

        try:
            user_data = gSheet()  # Fetch data from Google Sheet
            username = str(interaction.user)

            if username not in user_data:
                await self._handle_user_not_found(interaction)
                return

            member = await self._get_member(interaction)
            if not member:
                await self._handle_member_not_found(interaction)
                return

            await self._update_member_roles_and_nickname(interaction, member, user_data[username])

        except discord.errors.NotFound:
            await self._handle_generic_error(interaction, "Member or role not found.")
        except Exception as e:
            await self._handle_generic_error(interaction, str(e))

    async def _handle_user_not_found(self, interaction):
        """Handles the case where the user is not found in the database."""
        await interaction.followup.send(
            "Your Discord username isn't updated in our database. Kindly fill up the form. "
            "Form Link: [Click Here](https://forms.gle/t3HiKSuEXaF3PwdF7)",
            ephemeral=True
        )
        await log_message(bot, f"User {interaction.user.mention} not found in the database.")

    async def _get_member(self, interaction):
        """Fetches the member object from the guild."""
        return interaction.guild.get_member(interaction.user.id) or await interaction.guild.fetch_member(interaction.user.id)

    async def _handle_member_not_found(self, interaction):
        """Handles the case where the member is not found in the guild."""
        await interaction.followup.send("Member not found in the guild.", ephemeral=True)
        await log_message(bot, f"Member {interaction.user.mention} not found in the guild.")

    async def _update_member_roles_and_nickname(self, interaction, member, user_data):
        """Updates the member's roles and nickname."""
        actual_nickname, department, designation = user_data
        discord_nickname = nickname_gen(actual_nickname, department, designation)
        discord_roles = role_gen(department, designation)

        roles_to_add = [
            interaction.guild.get_role(int(role_id))
            for role_id in discord_roles
            if interaction.guild.get_role(int(role_id))
        ]

        await member.edit(roles=[])
        await member.edit(nick=discord_nickname)
        await member.add_roles(*roles_to_add)

        await interaction.followup.send("You have been verified and your roles have been updated.", ephemeral=True)
        await log_message(bot, f"User {interaction.user.mention} has been verified and roles updated.")

    async def _handle_generic_error(self, interaction, error_message):
        """Handles generic errors."""
        await interaction.followup.send(f"An error occurred: {error_message}", ephemeral=True)
        await log_message(bot, f"An error occurred for {interaction.user.mention}: {error_message}")


@bot.event
async def on_ready():
    """Event handler for when the bot is ready."""
    try:
        print(f'Logged in as {bot.user}')
        await log_message(bot, f'Logged in as {bot.user}')

        verification_channel_id = int(os.getenv('VERIFICATION_CHANNEL_ID'))
        channel = bot.get_channel(verification_channel_id)

        if channel:
            view = VerifyMeButton()
            await channel.send('Click on the button to be verified.', view=view)
            await log_message(bot, "Bot is ready and verification button sent.")
        else:
            error_message = f"Channel with ID {verification_channel_id} not found"
            print(error_message)
            await log_message(bot, error_message)

    except Exception as e:
        error_message = f"An error occurred in on_ready: {e}"
        print(error_message)
        await log_message(bot, error_message)

@bot.event
async def on_message(message):
    await handle_message(bot, message)  # Call the message handler from messageForwarder.py

# Run the bot
bot_token = os.getenv('DISCORD_BOT_TOKEN')
if bot_token:
    bot.run(bot_token)
else:
    print("Bot token not found in environment variables")