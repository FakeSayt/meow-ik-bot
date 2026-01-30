import os
import discord
from discord.ext import commands
from threading import Thread
import config
import server
import asyncio

# =====================================================
# DISCORD BOT SETUP
# =====================================================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# =====================================================
# IMPORT COMMANDS
# =====================================================
from bestartifact import setup as bestartifact_setup
from damage import setup as damage_setup
from helpmeow import setup as helpmeow_setup

@bot.event
async def on_ready():
    # Rejestracja wszystkich komend
    await bestartifact_setup(bot)
    await damage_setup(bot)
    await helpmeow_setup(bot)

    # Synchronizacja komend z Discordem
    await bot.tree.sync()
    print(f"Bot is ready! Logged in as {bot.user}")

# =====================================================
# RUN BOT
# =====================================================
bot.run(config.DISCORD_TOKEN)
