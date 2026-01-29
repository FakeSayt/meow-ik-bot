import discord
from discord.ext import commands
import config
import server  # to run Flask
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# =====================================================
# Load commands
# =====================================================
async def load_commands():
    from bestartifact import setup as setup_bestartifact
    from damage import setup as setup_damage
    from helpmeow import setup as setup_helpmeow

    await setup_bestartifact(bot)
    await setup_damage(bot)
    await setup_helpmeow(bot)

@bot.event
async def on_ready():
    # Najpierw załaduj komendy
    await load_commands()
    # Teraz synchronizuj je z Discordem
    await bot.tree.sync()
    print(f"Logged in as {bot.user} | Slash commands synced")

bot.run(config.DISCORD_TOKEN)
