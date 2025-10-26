import discord
from utils.gsheet import gSheet
from utils.nickname_gen import nickname_gen
from utils.role_gen import role_gen

# Custom Exceptions
class VerificationError(Exception):
    """Base exception for verification errors."""
    pass

class UserNotFoundInSheetError(VerificationError):
    """Raised when the user is not found in the Google Sheet."""
    pass

class MemberNotFoundError(VerificationError):
    """Raised when the member is not found in the guild."""
    pass

class VerificationService:
    """
    Handles the core logic of the verification process.
    """
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    def _get_user_data(self, username: str) -> list | None:
        """Fetches the user's data from the Google Sheet."""
        all_user_data = gSheet()
        return all_user_data.get(username)

    async def _get_member(self, interaction: discord.Interaction) -> discord.Member:
        """Fetches the member object from the guild."""
        member = interaction.guild.get_member(interaction.user.id) or await interaction.guild.fetch_member(interaction.user.id)
        if not member:
            raise MemberNotFoundError("Could not find member in the guild.")
        return member

    async def _update_member(self, interaction: discord.Interaction, member: discord.Member, user_data: list):
        """Updates the member's roles and nickname."""
        actual_nickname, department, designation = user_data
        new_nickname = nickname_gen(actual_nickname, department, designation)
        role_names = role_gen(department, designation)

        roles_to_add = [
            discord.utils.get(interaction.guild.roles, name=role_name)
            for role_name in role_names
            if discord.utils.get(interaction.guild.roles, name=role_name)
        ]

        await member.edit(nick=new_nickname, roles=roles_to_add)

    async def verify_user(self, interaction: discord.Interaction):
        """
        Orchestrates the user verification process.

        Raises:
            UserNotFoundInSheetError: If the user is not in the Google Sheet.
            MemberNotFoundError: If the member cannot be found in the guild.
            discord.Forbidden: If the bot lacks permissions.
            discord.HTTPException: If a Discord API error occurs.
        """
        user_data = self._get_user_data(str(interaction.user))
        if not user_data:
            raise UserNotFoundInSheetError("User not found in the Google Sheet.")

        member = await self._get_member(interaction)
        await self._update_member(interaction, member, user_data)
