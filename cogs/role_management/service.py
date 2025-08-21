# -*- coding: utf-8 -*-
"""
Role Management Service

This module provides the core business logic for exporting and importing Discord server roles.
It is designed to be decoupled from the Discord.py command interface, allowing for easier
testing and maintenance.
"""

import discord
import logging

# Configure a logger for this module
logger = logging.getLogger(__name__)

def export_server_roles(guild: discord.Guild) -> list[dict]:
    """
    Serializes all non-default roles in a guild to a list of dictionaries.

    The roles are sorted by their position in descending order to preserve the
    visual hierarchy of the server's role list.

    Args:
        guild: The discord.Guild object from which to export roles.

    Returns:
        A list of dictionaries, where each dictionary represents a role
        and contains its name, color, permissions, and other attributes.
    """
    roles_data = []
    # Sort roles by position to maintain the hierarchy in the exported file
    for role in sorted(guild.roles, key=lambda r: r.position, reverse=True):
        if role.is_default():  # Skip the @everyone role
            continue
        
        roles_data.append({
            'name': role.name,
            'color': role.color.value,
            'permissions': role.permissions.value,
            'hoist': role.hoist,
            'mentionable': role.mentionable,
            'position': role.position
        })
    logger.info(f"Exported {len(roles_data)} roles from guild '{guild.name}'.")
    return roles_data

async def import_server_roles(guild: discord.Guild, roles_data: list[dict]) -> tuple[int, int, int]:
    """
    Imports and updates roles in a guild from a list of role data dictionaries.

    This function iterates through the provided role data. If a role with the
    same name (case-insensitive) already exists, it updates the role's properties.
    Otherwise, it creates a new role.

    Args:
        guild: The discord.Guild object to import roles into.
        roles_data: A list of dictionaries, each representing a role.

    Returns:
        A tuple containing the number of created, updated, and skipped roles.
    """
    created_count = 0
    updated_count = 0
    skipped_count = 0
    # Map lowercased role names to the actual discord.Role object for easy lookup
    existing_roles = {role.name.lower(): role for role in guild.roles}

    # Sort by position to create roles in a sensible order
    roles_data.sort(key=lambda r: r.get('position', 0))

    for role_data in roles_data:
        role_name = role_data.get('name')
        if not role_name:
            skipped_count += 1
            continue

        role_name_lower = role_name.lower()
        
        try:
            # Prepare role properties from the JSON data
            permissions = discord.Permissions(role_data.get('permissions', 0))
            color = discord.Color(role_data.get('color', 0))
            hoist = role_data.get('hoist', False)
            mentionable = role_data.get('mentionable', False)

            # Check if the role exists to either update it or create it
            if role_name_lower in existing_roles:
                # --- UPDATE EXISTING ROLE ---
                role_to_update = existing_roles[role_name_lower]
                await role_to_update.edit(
                    name=role_name,  # Use original name in case of case changes
                    permissions=permissions,
                    color=color,
                    hoist=hoist,
                    mentionable=mentionable
                )
                updated_count += 1
                logger.info(f"Successfully updated role '{role_name}' in guild '{guild.name}'.")
            else:
                # --- CREATE NEW ROLE ---
                new_role = await guild.create_role(
                    name=role_name,
                    permissions=permissions,
                    color=color,
                    hoist=hoist,
                    mentionable=mentionable
                )
                created_count += 1
                # Add the new role to our lookup to avoid duplicates from the file
                existing_roles[role_name_lower] = new_role
                logger.info(f"Successfully created role '{role_name}' in guild '{guild.name}'.")

        except discord.Forbidden:
            logger.error(f"Permission denied during import of role '{role_name}' in guild '{guild.name}'.")
            skipped_count += 1
        except Exception as e:
            logger.error(f"An unexpected error occurred for role '{role_name}': {e}")
            skipped_count += 1
            
    return created_count, updated_count, skipped_count