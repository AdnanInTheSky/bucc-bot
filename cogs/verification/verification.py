import discord
from discord.ext import commands
from discord.ui import View, Button
import logging

from constants import ButtonIDs
from .service import VerificationService, UserNotFoundInSheetError, MemberNotFoundError
from .responder import (
    handle_user_not_found,
    handle_member_not_found,
    handle_generic_error,
    handle_success,
    handle_permission_error,
    handle_http_error,
)

logger = logging.getLogger(__name__)


class VerifyMeButton(View):
    """
    A Discord UI View that presents a "Verify Me" button to the user.
    When clicked, it initiates the verification process.
    """

    def __init__(self, bot: commands.Bot):
        """
        Initializes the VerifyMeButton view.
        """
        super().__init__(timeout=None)
        self.bot = bot
        self.verification_service = VerificationService(self.bot)

    @discord.ui.button(
        label="Verify Me",
        style=discord.ButtonStyle.primary,
        custom_id=ButtonIDs.VERIFY_ME,
    )
    async def verify_me_button(self, interaction: discord.Interaction, button: Button):
        """
        Handles the 'Verify Me' button click event by delegating to the VerificationService.
        """
        await interaction.response.defer(ephemeral=True)
        logger.info(f"Verification process started for user: {interaction.user}")

        try:
            await self.verification_service.verify_user(interaction)
            await handle_success(self.bot, interaction)

        except UserNotFoundInSheetError:
            await handle_user_not_found(self.bot, interaction)
        except MemberNotFoundError:
            await handle_member_not_found(self.bot, interaction)
        except discord.Forbidden:
            await handle_permission_error(self.bot, interaction)
        except discord.HTTPException as e:
            await handle_http_error(self.bot, interaction, e)
        except Exception as e:
            await handle_generic_error(self.bot, interaction, e)


class Verification(commands.Cog):
    """
    Cog for handling user verification.
    This cog is responsible for adding the verification view to the bot,
    making the "Verify Me" button persistent across bot restarts.
    """

    def __init__(self, bot: commands.Bot):
        """
        Initializes the Verification cog.
        """
        self.bot = bot
        self.bot.add_view(VerifyMeButton(self.bot))


async def setup(bot: commands.Bot):
    """
    Sets up the Verification cog by adding it to the bot.
    """
    await bot.add_cog(Verification(bot))