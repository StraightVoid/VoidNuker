import discord
import random
import asyncio
import json

# Load configuration from config.json
with open("config.json") as f:
    config = json.load(f)

# Configuration for rate-limit-friendly batching from config
delete_batch_size = config.get("delete_batch_size", 20)
create_batch_size = config.get("create_batch_size", 20)
delay_between_batches = config.get("delay_between_batches", 1)
ping_batch_size = config.get("ping_batch_size", 50)
spam_count = config.get("spam_count", 5)
invite_link = config.get("invite_link", "https://discord.gg/dywfjBVvsE")
version = config.get("version", "1.0.0")  # bot version

# Bot token will be loaded from config (ensure config.json is gitignored)
token = config.get("token")
if not token:
    raise RuntimeError("Bot token not found in config.json")

# Initialize Discord client with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.strip()
    lower = content.lower()

    # ─── NUKE COMMAND ──────────────────────────────────────────────────────────
    if lower.startswith('$nuke'):
        guild = message.guild
        # ... (unchanged nuke logic) ...
        # [Omitted for brevity]
        pass  # placeholder for nuke logic

    # ─── MASSDEL COMMAND ────────────────────────────────────────────────────────
    elif lower.startswith('$massdel'):
        guild = message.guild
        # ... (unchanged massdel logic) ...
        pass  # placeholder for massdel logic

    # ─── DELETEMSGS COMMAND ─────────────────────────────────────────────────────
    elif lower.startswith('$deletemsgs'):
        if not message.author.guild_permissions.manage_messages:
            return await message.channel.send("❌ You lack Manage Messages permission.")
        guild = message.guild
        # ... (unchanged deletemsgs logic) ...
        pass  # placeholder for deletemsgs logic

    # ─── MASSBAN COMMAND ─────────────────────────────────────────────────────────
    elif lower.startswith('$massban'):
        guild = message.guild
        # ... (unchanged massban logic) ...
        pass  # placeholder for massban logic

    # ─── BAN COMMAND ────────────────────────────────────────────────────────────
    elif lower.startswith('$ban '):
        mentions = message.mentions
        if not mentions:
            return await message.channel.send("❌ Please mention a user to ban.")
        target = mentions[0]
        if target == client.user:
            return await message.channel.send("❌ Cannot ban myself.")
        try:
            await message.guild.ban(target, reason=f"Banned by {message.author}")
            await message.channel.send(f"🔨 Banned {target.mention}.")
        except Exception as e:
            await message.channel.send(f"❌ Failed to ban {target.mention}: {e}")

    # ─── DM COMMAND ─────────────────────────────────────────────────────────────
    elif lower.startswith('$dm '):
        parts = content.split(' ', 2)
        if len(parts) < 3:
            return await message.channel.send("❌ Usage: $dm <user_id> <message>")
        user_id_str, dm_msg = parts[1], parts[2]
        try:
            user_id = int(user_id_str)
            user = await client.fetch_user(user_id)
            await user.send(dm_msg)
            await message.channel.send(f"📬 Sent DM to {user.mention}.")
        except ValueError:
            await message.channel.send("❌ Invalid user ID.")
        except Exception as e:
            await message.channel.send(f"❌ Failed to send DM: {e}")

    # ─── VERSION COMMAND ────────────────────────────────────────────────────────
    elif lower.startswith('$version'):
        await message.channel.send(f"🤖 Bot version: {version}")

    # ─── HELP COMMAND ────────────────────────────────────────────────────────────
    elif lower.startswith('$help'):
        help_text = (
            "**Available Commands:**\n"
            "`$nuke` — Deletes all channels, creates 150 spammed channels, and bans all members.\n"
            "`$massdel` — Deletes all channels in batches.\n"
            "`$deletemsgs` — Deletes all messages in every text channel (no message if none deleted).\n"
            "`$massban` — Bans all members in the server except the bot.\n"
            "`$ban @user` — Bans the mentioned user.\n"
            "`$dm <user_id> <message>` — Sends a direct message to the specified user by ID.\n"
            "`$version` — Displays the bot version.\n"
            "`$help` — Displays this help message.\n\n"
            f"Version: {version}"
        )
        await message.channel.send(help_text)

# Run with the token from config.json
client.run(token)
