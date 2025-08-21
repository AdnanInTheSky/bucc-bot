# BUCC Discord Bot

A Discord bot for the Brac University Computer Club (BUCC) to automate member verification and role management.

## Features

- **Verification System:** New members can verify themselves by clicking a "Verify Me" button. The bot then checks their Discord username against a Google Sheet of registered members.
- **Automatic Role Assignment:** Assigns roles based on the member's department and designation within the club.
- **Nickname Generation:** Automatically generates a standardized nickname for verified members.
- **Message Forwarding:** Forwards messages from a specific channel to another.
- **Interaction Logging:** Logs important events, such as verifications and errors, to a designated log channel.
- **Automatic Role and Channel Creation:** On startup, the bot automatically creates predefined roles and channels (e.g., `automatic-verification`, `notification`, `message-forward-by-bot`) if they don't already exist in a server.
- **Role Listing Command:** The `!list_roles` command now displays role names, IDs, colors, and a summary of their permissions.

## Codebase Structure

The project is organized into the following directories:

- `bot.py`: The main entry point of the bot. It handles bot initialization, loads cogs, and manages core Discord events like `on_ready` and `on_message`.
- `config.py`: Centralized configuration management. It loads environment variables and provides access to various bot settings.
- `cogs/`: Contains Discord.py cogs, which are modular extensions that add functionality to the bot.
  - `verification.py`: Handles the user verification process, including the "Verify Me" button interaction.
  - `roles.py`: Contains commands related to role management, such as `!list_roles`.
- `utils/`: Contains utility functions and helper modules that are not cogs but are used across different parts of the bot.
  - `gsheet.py`: Functions for interacting with the Google Sheet to fetch member data.
  - `nickname_gen.py`: Logic for generating standardized nicknames.
  - `role_gen.py`: Logic for generating role names based on user data.
  - `interaction_logger.py`: Functions for logging important bot interactions and errors to a designated Discord channel.
  - `messageForwarder.py`: Handles the forwarding of messages between specified channels.
  - `keep_alive.py`: Contains a simple Flask web server to keep the bot alive, especially when deployed on platforms that require a web server.

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/BUCC-Discord-BOT.git
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Create a `.env` file:**
   Create a `.env` file in the root directory and add the following environment variables:
   ```
   DISCORD_BOT_TOKEN=your_bot_token
   GOOGLE_SHEET_ID=your_google_sheet_id
   FORWARDING_CHANNEL_ID=your_forwarding_channel_id # Optional: Only if message forwarding is desired
   ```
   *Note: `VERIFICATION_CHANNEL_ID` and `LOG_CHANNEL_ID` are no longer needed as channels are now automatically created/identified by name (`automatic-verification` and `notification`).*

4. **Run the bot:**
   ```bash
   python bot.py
   ```

## Dependencies

- [discord.py](https://discordpy.readthedocs.io/en/latest/)
- [pandas](https://pandas.pydata.org/)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/)