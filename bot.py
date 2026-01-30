import os
import discord
from discord.ext import commands
from threading import Thread
from flask import Flask
import asyncio
import config
import server

# =====================================================
# DISCORD BOT SETUP
# =====================================================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# =====================================================
# LOAD COMMANDS
# =====================================================
async def load_commands():
    import bestartifact, damage, helpmeow
    await bestartifact.setup(bot)
    await damage.setup(bot)
    await helpmeow.setup(bot)

@bot.event
async def on_ready():
    await load_commands()
    await bot.tree.sync()
    print(f"Logged in as {bot.user} | Commands synced")

# =====================================================
# RUN BOT
# =====================================================
bot.run(config.DISCORD_TOKEN)
