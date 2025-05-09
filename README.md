# VoidNuker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/) [![discord.py](https://img.shields.io/badge/discord.py-stable-success.svg)](https://discordpy.readthedocs.io/)

VoidNuker is a powerful Discord administration bot written in Python, built on `discord.py`. It offers destructive and utility commands for server maintenance and management, all configurable via a `config.json` file.

## 🚀 Features

- **`$nuke`**: Deletes all channels, creates 150 `NUKED-XXXX` channels, spams each with an invite link, and bans all members (excluding the bot).
- **`$massdel`**: Deletes all channels in controlled batches to respect rate limits.
- **`$deletemsgs`**: Purges all messages from every text channel (requires **Manage Messages** permission).
- **`$massban`**: Bans all members except the bot in rate-limit-friendly batches.
- **`$ban @user`**: Bans the specified user.
- **`$dm <user_id> <message>`**: Sends a direct message to a user by their ID.
- **`$version`**: Displays the current bot version.
- **`$help`**: Shows this help message.

## 🛠 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/<your_username>/VoidNuker.git
cd VoidNuker

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate.bat

# Install dependencies
pip install -U discord.py
