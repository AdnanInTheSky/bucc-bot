import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from cogs.gsheet import gSheet
from cogs.nickname_gen import nickname_gen
from cogs.role_gen import role_gen
from cogs.interaction_logger import log_message

from cogs.keep_alive import keep_alive
keep_alive()

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Enable the members intent

bot = commands.Bot(command_prefix='!', intents=intents)

class VerifyMeButton(discord.ui.View):
    @discord.ui.button(label="Verify Me", style=discord.ButtonStyle.primary)
    async def verify_me_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            # Acknowledge the interaction immediately
            await interaction.response.defer(ephemeral=True)

            user_data = gSheet() # Fetching data from google sheet, returning a dictionary of username and their details
            username = str(interaction.user)
            if username not in user_data:
                await interaction.followup.send("Your discord username isn't updated in our databse. Kindly fill up the form. Form Link: [Click Here](https://forms.gle/t3HiKSuEXaF3PwdF7)", ephemeral=True)
                await log_message(bot, f"User {interaction.user.mention} not found in the database.")
                return

            member = interaction.guild.get_member(interaction.user.id) or await interaction.guild.fetch_member(interaction.user.id)
            if member is None:
                await interaction.followup.send("Member not found in the guild.", ephemeral=True)
                await log_message(bot, f"Member {interaction.user.mention} not found in the guild.")
                return

            actual_nickname, department, designation = user_data[username]
            discord_nickname = nickname_gen(actual_nickname, department, designation)
            discord_role = role_gen(department, designation)

            role_to_add = []
            for role_id in discord_role:
                role = interaction.guild.get_role(int(role_id))
                if role:
                    role_to_add.append(role)

            await member.edit(roles=[])
            await member.edit(nick=discord_nickname)
            await member.add_roles(*role_to_add)

            await interaction.followup.send("You have been verified and your roles have been updated.", ephemeral=True)
            await log_message(bot, f"User {interaction.user.mention} has been verified and roles updated.")

        except Exception as e:
            print(f"An error occurred: {e}")
            await interaction.followup.send("An error occurred while processing your request.", ephemeral=True)
            await log_message(bot, f"An error occurred while processing verification for {interaction.user.mention}: {e}")

@bot.event
async def on_ready():
    try:
        print(f'Logged in as {bot.user}')
        await log_message(bot, f'Logged in as {bot.user}')

        verfication_channel_id = int(os.getenv('VERIFICATION_CHANNEL_ID'))
        channel = bot.get_channel(verfication_channel_id)
        if channel:
            view = VerifyMeButton()
            await channel.send('Click on the button to be verified.', view=view)
            await log_message(bot, "Bot is ready and verification button sent.")
        else:
            print(f"Channel with ID {verfication_channel_id} not found")
            await log_message (bot, f"Channel with ID {verfication_channel_id} not found")
    except Exception as e:
        print(f"An error occurred: {e}")
        await log_message(bot, f"An error occurred in on_ready: {e}")

# Get the bot token from the environment variable
bot_token = os.getenv('DISCORD_BOT_TOKEN')
if bot_token:
    bot.run(bot_token)
else:
    print("Bot token not found in environment variables")