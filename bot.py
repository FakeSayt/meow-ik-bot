import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from server import start_server
from bestartifact import BestArtifactCommand
from damage import DamageCommand
from helpmeow import HelpMeowCommand

# Start web server
start_server()

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    bot.tree.add_command(BestArtifactCommand())
    bot.tree.add_command(DamageCommand())
    bot.tree.add_command(HelpMeowCommand())
    await bot.tree.sync()
    print(f"Logged in as {bot.user} | Slash commands synced")

bot.run(DISCORD_TOKEN)
