# 🤖 BUCC Discord Bot

<div align="center">

[![Bot Status](https://img.shields.io/badge/status-active-brightgreen)](https://github.com/AffanHossainRakib/BUCC-Discord-BOT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org/downloads/)
[![Discord.py Version](https://img.shields.io/badge/discord.py-2.5.2-7289DA)](https://discordpy.readthedocs.io/)

**A powerful Discord bot for the Brac University Computer Club (BUCC) that streamlines member verification and server management.**

</div>

## ✨ Features

<table>
  <tr>
    <td width="50%">
      <h3>🔐 Verification System</h3>
      <p>New members verify themselves with a single click. The bot validates their Discord username against the club's Google Sheet.</p>
    </td>
    <td width="50%">
      <h3>👥 Automatic Role Assignment</h3>
      <p>Intelligently assigns roles based on member's department and designation within the club hierarchy.</p>
    </td>
  </tr>
  <tr>
    <td>
      <h3>👤 Nickname Standardization</h3>
      <p>Generates consistent, formatted nicknames for all verified members.</p>
    </td>
    <td>
      <h3>📨 Message Forwarding</h3>
      <p>Seamlessly forwards messages between configured channels.</p>
    </td>
  </tr>
  <tr>
    <td>
      <h3>📝 Interaction Logging</h3>
      <p>Comprehensive logging of all important events and errors to a designated channel.</p>
    </td>
    <td>
      <h3>⚙️ Automatic Server Setup</h3>
      <p>Creates required roles and channels on startup if they don't exist.</p>
    </td>
  </tr>
</table>

## 🏗️ Architecture

The project follows a modular architecture with clear separation of concerns:

### Core Components

```
BUCC-Discord-BOT
├── 🚀 bot.py           # Main entry point & event handlers
├── ⚙️ config.py        # Configuration management
├── 📋 constants.py     # Centralized constants & mappings
├── 📋 requirements.txt # Dependencies
```

### Modules

<details>
<summary><b>📁 cogs/</b> - Discord.py extensions</summary>

```
cogs/
├── verification/             # User verification system
│   ├── __init__.py           # Module initialization
│   ├── responder.py          # UI interactions & responses
│   ├── service.py            # Verification business logic
│   └── verification.py       # Main verification cog
└── role_management/          # Role import/export system
    ├── __init__.py           # Module initialization
    ├── cog.py                # Role management commands
    └── service.py            # Role operations logic
```

</details>

<details>
<summary><b>🛠️ utils/</b> - Helper utilities</summary>

```
utils/
├── discord_helpers.py    # Reusable Discord utilities
├── gsheet.py             # Google Sheets integration
├── interaction_logger.py # Discord event logging
├── message_forwarder.py  # Channel message relay
├── nickname_generator.py # Nickname standardization
└── role_generator.py     # Role assignment logic
```

</details>

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Discord Bot Token
- Google Sheet with member data

### Installation

<details>
<summary><b>Step 1:</b> Clone the repository</summary>

```bash
git clone https://github.com/AffanHossainRakib/BUCC-Discord-BOT.git
cd BUCC-Discord-BOT
```

</details>

<details>
<summary><b>Step 2:</b> Create a virtual environment (recommended)</summary>

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

</details>

<details>
<summary><b>Step 3:</b> Install dependencies</summary>

```bash
pip install -r requirements.txt
```

</details>

<details>
<summary><b>Step 4:</b> Set up environment variables</summary>

Create a `.env` file in the project root with:

```
DISCORD_BOT_TOKEN=your_bot_token
GOOGLE_SHEET_ID=your_google_sheet_id
```

> 💡 Channels like `automatic-verification` and `notification` are now created automatically!

</details>

<details>
<summary><b>Step 5:</b> Launch the bot</summary>

```bash
python bot.py
```

</details>

## 📚 Dependencies

| Library           | Version | Description         | Documentation                                            |
| ----------------- | ------- | ------------------- | -------------------------------------------------------- |
| **discord.py**    | 2.3.2+  | Discord API wrapper | [Documentation](https://discordpy.readthedocs.io/)       |
| **pandas**        | 2.0.0+  | Data manipulation   | [Documentation](https://pandas.pydata.org/)              |
| **python-dotenv** | 1.0.0+  | Environment config  | [Documentation](https://pypi.org/project/python-dotenv/) |

## 🛠️ Configuration

### Google Sheet Structure

Your Google Sheet should have the following columns:

1. Discord Username (e.g., `username`)
2. Nick Name (e.g., `John Doe`)
3. Department (e.g., `Research and Development`, `Finance`, `Creative`, `Human Resources`)
4. Designation (e.g., `Executive`, `Senior Executive`, `General Member`)

Make sure your sheet is published to the web to be accessible via CSV export.

### Bot Permissions

The bot requires the following permissions:

- Manage Roles
- Manage Nicknames
- Send Messages
- Read Message History
- Add Reactions
- Use External Emojis
- Manage Channels

## 🔧 Usage

### Verification Process

1. Users click the "Verify Me" button in the `automatic-verification` channel
2. Bot checks their Discord username against the Google Sheet
3. If found, bot assigns appropriate roles and updates their nickname
4. Bot sends confirmation message with assigned roles

### Commands

| Command         | Description                      | Permission    | Restriction      |
| --------------- | -------------------------------- | ------------- | ---------------- |
| `!export_roles` | Export server roles to JSON file | Administrator | test-com channel |
| `!import_roles` | Import roles from JSON file      | Administrator | test-com channel |

## 💎 Code Quality

This project follows enterprise-level coding standards:

- ✅ **Modular Design** - Clear separation of concerns with small, focused files
- ✅ **Type Safety** - Comprehensive type hints throughout the codebase
- ✅ **PEP 8 Compliant** - Follows Python style guidelines
- ✅ **DRY Principle** - No code duplication, reusable utilities
- ✅ **Constants Management** - All magic strings centralized in `constants.py`
- ✅ **Error Handling** - Proper exception handling with custom error types
- ✅ **Self-Documenting** - Clear naming conventions minimize need for comments

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📃 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

BUCC - [bucc@g.bracu.ac.bd](mailto:bucc@g.bracu.ac.bd)

Project Link: [https://github.com/AffanHossainRakib/BUCC-Discord-BOT](https://github.com/AffanHossainRakib/BUCC-Discord-BOT)

---

<div align="center">
  <sub>Built with ❤️ by the Brac University Computer Club</sub>
</div>
