# -*- coding: utf-8 -*-
"""
Role Management Cog

This cog provides server administrators with commands to export the server's role
structure to a JSON file and import it into another server. This is useful for
server templating, backups, or migrations.
"""

import discord
from discord.ext import commands
import json
import os
import logging
from . import service

# Configure a logger for this cog
logger = logging.getLogger(__name__)

class RoleManagementCog(commands.Cog, name="Role Management"):
    """A cog for exporting and importing server roles."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='export_roles')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def export_roles(self, ctx: commands.Context):
        """
        Exports all server roles to a JSON file.

        This command serializes the server's roles, including their names, colors,
        permissions, and hierarchy, into a `roles.json` file. The file is then
        sent to the channel where the command was invoked.

        Usage:
            !export_roles
        """
        # Silently ignore commands not in the correct channel
        if ctx.channel.name != 'test-com':
            return

        # Defer the response to let users know the bot is working on the request.
        await ctx.typing()

        try:
            roles_data = service.export_server_roles(ctx.guild)

            if not roles_data:
                await ctx.send("This server has no roles to export (besides @everyone).")
                return

            file_path = 'roles.json'
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(roles_data, f, indent=4)

            await ctx.send("Here are the exported roles:", file=discord.File(file_path))
            logger.info(f"Successfully exported roles for guild '{ctx.guild.name}' for user '{ctx.author}'.")
            
            # Clean up the temporary file
            os.remove(file_path)

        except discord.Forbidden:
            logger.warning(f"Missing permissions to export roles in guild '{ctx.guild.name}'.")
            await ctx.send("I don't have the required permissions to read roles.")
        except Exception as e:
            logger.error(f"An error occurred during role export in '{ctx.guild.name}': {e}", exc_info=True)
            await ctx.send("An unexpected error occurred. Please check the logs.")

    @commands.command(name='import_roles')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def import_roles(self, ctx: commands.Context):
        """
        Imports roles from an uploaded JSON file.

        This command reads a `roles.json` file attached to the message, then creates
        roles in the current server with the same properties. It will skip any roles
        that already exist by name.

        Usage:
            !import_roles (with `roles.json` file attached)
        """
        # Silently ignore commands not in the correct channel
        if ctx.channel.name != 'test-com':
            return

        await ctx.typing()

        if not ctx.message.attachments:
            await ctx.send("You must upload a `roles.json` file with this command.")
            return

        attachment = ctx.message.attachments[0]
        if not attachment.filename.endswith('.json'):
            await ctx.send("Invalid file format. Please upload a file ending in `.json`.")
            return

        try:
            roles_bytes = await attachment.read()
            roles_data = json.loads(roles_bytes.decode('utf-8'))
            
            created, updated, skipped = await service.import_server_roles(ctx.guild, roles_data)

            await ctx.send(f"Role import complete. **Created:** {created}, **Updated:** {updated}, **Skipped:** {skipped}.")
            logger.info(f"Successfully imported roles in guild '{ctx.guild.name}' for user '{ctx.author}'.")

        except json.JSONDecodeError:
            logger.warning(f"Failed to decode JSON from attachment in '{ctx.guild.name}'.")
            await ctx.send("The provided file is not a valid JSON file.")
        except discord.Forbidden:
            logger.warning(f"Missing permissions to import roles in guild '{ctx.guild.name}'.")
            await ctx.send("I don't have the required permissions to create roles.")
        except Exception as e:
            logger.error(f"An error occurred during role import in '{ctx.guild.name}': {e}", exc_info=True)
            await ctx.send("An unexpected error occurred. Please check the logs.")

async def setup(bot: commands.Bot):
    """
    The setup function for the RoleManagementCog.

    This function is called by discord.py when loading the extension, and it
    registers the cog with the bot.
    """
    await bot.add_cog(RoleManagementCog(bot))