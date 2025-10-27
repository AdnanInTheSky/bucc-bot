"""
Discord utility functions for common operations.

This module provides helper functions for frequently used Discord operations
to reduce code duplication and improve maintainability.
"""

import discord
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def get_text_channel(
    guild: discord.Guild, channel_name: str
) -> Optional[discord.TextChannel]:
    """
    Safely retrieve a text channel by name from a guild.

    Args:
        guild: The Discord guild to search in
        channel_name: Name of the channel to find

    Returns:
        The TextChannel if found, None otherwise
    """
    return discord.utils.get(guild.text_channels, name=channel_name)


async def get_or_fetch_member(
    guild: discord.Guild, user_id: int
) -> Optional[discord.Member]:
    """
    Get a member from cache or fetch from API if not cached.

    Args:
        guild: The Discord guild
        user_id: ID of the user to retrieve

    Returns:
        The Member if found, None otherwise
    """
    member = guild.get_member(user_id)
    if member:
        return member

    try:
        return await guild.fetch_member(user_id)
    except discord.NotFound:
        logger.warning(f"Member {user_id} not found in guild {guild.name}")
        return None
    except discord.HTTPException as e:
        logger.error(f"HTTP error fetching member {user_id}: {e}")
        return None


async def ensure_role_exists(
    guild: discord.Guild, role_name: str
) -> Optional[discord.Role]:
    """
    Ensure a role exists in the guild, creating it if necessary.

    Args:
        guild: The Discord guild
        role_name: Name of the role to ensure exists

    Returns:
        The Role object if successful, None if creation failed
    """
    existing_role = discord.utils.get(guild.roles, name=role_name)
    if existing_role:
        return existing_role

    try:
        new_role = await guild.create_role(name=role_name)
        logger.info(f"Created role '{role_name}' in {guild.name}")
        return new_role
    except discord.Forbidden:
        logger.warning(f"Missing permissions to create role '{role_name}' in {guild.name}")
        return None
    except Exception as e:
        logger.error(f"Error creating role '{role_name}' in {guild.name}: {e}")
        return None


async def ensure_text_channel_exists(
    guild: discord.Guild, channel_name: str
) -> Optional[discord.TextChannel]:
    """
    Ensure a text channel exists in the guild, creating it if necessary.

    Args:
        guild: The Discord guild
        channel_name: Name of the channel to ensure exists

    Returns:
        The TextChannel object if successful, None if creation failed
    """
    existing_channel = get_text_channel(guild, channel_name)
    if existing_channel:
        return existing_channel

    try:
        new_channel = await guild.create_text_channel(name=channel_name)
        logger.info(f"Created channel '{channel_name}' in {guild.name}")
        return new_channel
    except discord.Forbidden:
        logger.warning(
            f"Missing permissions to create channel '{channel_name}' in {guild.name}"
        )
        return None
    except Exception as e:
        logger.error(f"Error creating channel '{channel_name}' in {guild.name}: {e}")
        return None
