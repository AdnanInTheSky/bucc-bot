"""
Verification service for member verification workflow.

Handles fetching member data from Google Sheets and updating Discord
member roles and nicknames.
"""

import discord
import logging
from typing import Optional

from utils.gsheet import fetch_member_data_from_sheet, SheetFetchError
from utils.nickname_generator import generate_member_nickname
from utils.role_generator import generate_member_roles
from utils.discord_helpers import get_or_fetch_member

logger = logging.getLogger(__name__)


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
    """Handles the core logic of the verification process."""

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    def _get_user_data(self, username: str) -> Optional[list[str]]:
        """
        Fetch user data from Google Sheet.

        Args:
            username: Discord username to look up

        Returns:
            List containing [name, department, designation] or None if not found

        Raises:
            SheetFetchError: If sheet cannot be accessed
        """
        try:
            all_user_data = fetch_member_data_from_sheet()
            return all_user_data.get(username)
        except SheetFetchError:
            logger.error(f"Failed to fetch sheet data for username lookup: {username}")
            raise

    async def _get_member(self, interaction: discord.Interaction) -> discord.Member:
        """
        Get member from guild cache or fetch from API.

        Args:
            interaction: Discord interaction object

        Returns:
            Discord Member object

        Raises:
            MemberNotFoundError: If member cannot be found
        """
        member = await get_or_fetch_member(interaction.guild, interaction.user.id)
        if not member:
            raise MemberNotFoundError("Could not find member in the guild")
        return member

    async def _update_member(
        self, interaction: discord.Interaction, member: discord.Member, user_data: list[str]
    ) -> None:
        """
        Update member's nickname and roles based on verified data.

        Args:
            interaction: Discord interaction object
            member: Member to update
            user_data: List containing [name, department, designation]
        """
        from constants import REQUIRED_ROLES

        actual_name, department, designation = user_data
        new_nickname = generate_member_nickname(actual_name, department, designation)
        role_names = generate_member_roles(department, designation)

        logger.info(f"Assigning roles {role_names} to {member}")

        roles_to_add = [
            discord.utils.get(interaction.guild.roles, name=role_name)
            for role_name in role_names
            if discord.utils.get(interaction.guild.roles, name=role_name)
        ]

        logger.info(f"Found roles to add: {[role.name for role in roles_to_add]}")

        # Remove all existing BUCC roles (department and designation roles)
        roles_to_remove = [
            role for role in member.roles
            if role.name in REQUIRED_ROLES
        ]

        if roles_to_remove:
            logger.info(f"Removing old roles: {[role.name for role in roles_to_remove]}")
            await member.remove_roles(*roles_to_remove, reason="Updating verification roles")

        # Update nickname
        await member.edit(nick=new_nickname)

        # Add new roles (this preserves existing roles like @everyone)
        await member.add_roles(*roles_to_add, reason="Verified member")

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
