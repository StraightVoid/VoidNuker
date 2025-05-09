# VoidNuker

VoidNuker is a powerful Discord administration bot written in Python using discord.py. It provides a suite of destructive and utility commands designed for server maintenance and management, configurable via a JSON file.

Features
$nuke: Deletes all channels, creates 150 randomly numbered NUKED-XXXX channels, spams each with an invite link, and bans all members (excluding the bot).
$massdel: Deletes all channels in controlled batches to avoid rate limits.
$deletemsgs: Purges all messages from every text channel (requires Manage Messages permission).
$massban: Bans all members in the server except the bot, in rate-limit‑friendly batches.
$ban @user: Bans the specified user.
$dm <user_id> : Sends a direct message to a single user by their ID.
$version: Displays the current bot version.
$help: Lists all commands and usage.

Installation & Setup

Clone the repository:
'git clone https://github.com/yourusername/VoidNuker.git'
'cd VoidNuker'

