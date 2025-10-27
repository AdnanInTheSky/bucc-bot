# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Discord bot for the Brac University Computer Club (BUCC) that automates member verification, role assignment, and server management. The bot validates Discord usernames against a Google Sheet containing member data, then automatically assigns roles and standardizes nicknames based on department and designation.

## Running the Bot

**Development:**
```bash
python bot.py
```

**Environment Variables Required:**
- `DISCORD_BOT_TOKEN` - Discord bot token
- `GOOGLE_SHEET_ID` - Google Sheet ID containing member data

**Installing Dependencies:**
```bash
pip install -r requirements.txt
```

**Deployment:**
The bot is configured for deployment on Railway using NIXPACKS. Configuration file: `railway.json`.

## Architecture

### Core Entry Point
- `bot.py` - Main entry point with event handlers and bot initialization. Contains retry logic for connection failures with exponential backoff (up to 5 retries). Automatically creates required roles and channels on startup.

### Configuration
- `config.py` - Centralized configuration management using environment variables via `python-dotenv`. Uses custom `ConfigError` exception for missing environment variables.

### Cogs System
The bot uses discord.py's cog system for modular functionality. Cogs are auto-loaded from the `cogs/` directory by walking the filesystem and loading files named `cog.py` or `verification.py` (see `bot.py:196-212`).

**Verification System (`cogs/verification/`):**
- `verification.py` - Main cog that registers the persistent "Verify Me" button view
- `service.py` - Core verification logic orchestrating the verification flow
- `responder.py` - UI response handlers for different verification outcomes

The verification flow:
1. User clicks "Verify Me" button → `verification.py:39-58`
2. `VerificationService.verify_user()` fetches user data from Google Sheet
3. If found, generates nickname via `generate_member_nickname()` and roles via `generate_member_roles()`
4. Updates member with new nickname and roles
5. Sends appropriate response (success/error) via responder functions

**Role Management (`cogs/role_management/`):**
- `cog.py` - Admin commands for exporting/importing role configurations
- `service.py` - Business logic for role export/import operations
- Commands restricted to `test-com` channel and require administrator permissions

### Utilities (`utils/`)

**Google Sheets Integration (`gsheet.py`):**
- Fetches member data via CSV export URL
- Returns dictionary with Discord username as key, `[name, department, designation]` as value
- Google Sheet must be published to web for CSV access

**Nickname Generation (`nickname_generator.py`):**
- Formats: `{name} || {dept} || {designation}` for regular members
- Formats: `{name} || {designation}` for GB/EB/Alumni
- Maps full names to abbreviations (e.g., "Senior Executive" → "SE")

**Role Assignment (`role_generator.py`):**
- GB/EB/Alumni: Only designation role
- Senior Executives: Department role + "Senior Executive" role
- Executives/General Members: Only department role
- Department names mapped to abbreviations (e.g., "Research and Development" → "R&D")

**Discord Helpers (`discord_helpers.py`):**
- Reusable utilities for Discord operations (get channels, fetch members, create roles/channels)

**Logging (`interaction_logger.py`):**
- Sends formatted log messages to "notification" channel in each guild

**Message Forwarding (`message_forwarder.py`):**
- Relays messages between configured channels

## Required Roles and Channels

The bot auto-creates these on startup if missing:

**Roles:** Governing Body, Executive Body, Senior Executive, Alumni, Faculty, C&M, Creative, Event, Finance, HR, Press Release, R&D

**Channels:** automatic-verification, notification, message-forward-by-bot

## Google Sheet Structure

Must have exactly these columns in order:
1. Discord Username (format: `username#1234` or new format without discriminator)
2. Actual Name
3. Department (full name: "Research and Development", "Human Resources", etc.)
4. Designation ("Executive", "Senior Executive", "Governing Body", etc.)

Sheet must be published to web for CSV export access.

## Bot Permissions Required

- Manage Roles
- Manage Nicknames
- Manage Channels
- Send Messages
- Read Message History
- Add Reactions
- Use External Emojis

## Error Handling Patterns

The verification system uses custom exceptions for flow control:
- `UserNotFoundInSheetError` - User not in Google Sheet
- `MemberNotFoundError` - Member not in guild
- `discord.Forbidden` - Permission errors
- `discord.HTTPException` - Discord API errors

All verification errors are caught in `verification.py:45-58` and routed to appropriate response handlers in `responder.py`.

## Connection Resilience

The bot implements retry logic with exponential backoff for:
- Connection closed errors (`discord.ConnectionClosed`)
- HTTP errors (`discord.HTTPException`)
- Max 5 retries with delays: 5s, 10s, 20s, 40s, 80s

See `bot.py:174-195` for implementation details.

## Development Notes

- Cog loading is automatic but restricted to files named `cog.py` or `verification.py` to avoid loading utility modules
- The verification button uses `timeout=None` for persistence across bot restarts
- All async operations use proper `await` syntax
- Logging is configured at INFO level with timestamp formatting
- The bot uses `!` as command prefix for text commands
