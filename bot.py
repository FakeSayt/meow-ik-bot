import os
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread
import asyncio
import traceback
from openai import OpenAI

# =====================================================
# WEB SERVER (RENDER)
# =====================================================
app = Flask(__name__)

@app.route("/")
def home():
    return "Discord bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web).start()

# =====================================================
# OPENAI CLIENT
# =====================================================
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is missing!")

client = OpenAI(api_key=openai_api_key)

# =====================================================
# HEROES DICTIONARY (full + short)
# =====================================================
HERO_INFO = {
    "wukong": {"full": "Wukong", "short": "Wuk"},
    "louis ix": {"full": "Louis IX", "short": "Louis"},
    "tutankhamun": {"full": "Tutankhamun", "short": "Tut"},
    "khubilai khan": {"full": "Khubilai Khan", "short": "Khan"},
    "manco": {"full": "Manco", "short": "Manco"},
    "alexander the great": {"full": "Alexander The Great", "short": "Alex"},
    "hippolyta": {"full": "Hippolyta", "short": "Hip"},
    "william": {"full": "William", "short": "Will"},
    "attila the hun": {"full": "Attila The Hun", "short": "Attila"},
    "saladin": {"full": "Saladin", "short": "Sal"},
    "muhammad ii": {"full": "Muhammad II", "short": "Muh"},
    "siegfried": {"full": "Siegfried", "short": "Sieg"},
    "peter the great": {"full": "Peter The Great", "short": "Peter"},
    "ramesses ii": {"full": "Ramesses II", "short": "Ram"},
    "hannibal barca": {"full": "Hannibal Barca", "short": "Hann"},
    "herald": {"full": "Herald", "short": "Herald"},
    "frederick": {"full": "Frederick", "short": "Fred"},
    "loki": {"full": "Loki", "short": "Loki"},
    "hammurabi": {"full": "Hammurabi", "short": "Ham"},
    "himiko": {"full": "Himiko", "short": "Him"},
    "empress wu": {"full": "Empress Wu", "short": "Wu"},
    "baldwin iv": {"full": "Baldwin IV", "short": "Bald"},
    "merlin": {"full": "Merlin", "short": "Mer"},
    "cleopatra": {"full": "Cleopatra", "short": "Cleo"},
    "bjorn": {"full": "Bjorn", "short": "Bjorn"},
    "king arthur": {"full": "King Arthur", "short": "Arthur"},
    "el cid": {"full": "El Cid", "short": "Cid"},
    "leonidas": {"full": "Leonidas", "short": "Leo"},
    "julius caesar": {"full": "Julius Caesar", "short": "JC"},
    "charles": {"full": "Charles", "short": "Char"},
    "ragnar": {"full": "Ragnar", "short": "Rag"},
    "trajan": {"full": "Trajan", "short": "Traj"},
    "tokugawa": {"full": "Tokugawa", "short": "Toku"},
    "gilgamesh": {"full": "Gilgamesh", "short": "Gil"},
    "elizabeth bathory": {"full": "Elizabeth Bathory", "short": "Liz"},
    "yoshitsune": {"full": "Yoshitsune", "short": "Yoshi"},
    "yi seong-gye": {"full": "Yi Seong-Gye", "short": "Yi"},
    "ashoka": {"full": "Ashoka", "short": "Ash"},
    "genghis khan": {"full": "Genghis Khan", "short": "GK"},
    "arash": {"full": "Arash", "short": "Arash"},
    "atalanta": {"full": "Atalanta", "short": "Ata"},
    "seondeok": {"full": "Seondeok", "short": "Seon"},
    "margaret i": {"full": "Margaret I", "short": "Marg"},
    "nebuchadnezzar ii": {"full": "Nebuchadnezzar II", "short": "Neb"}
}

# =====================================================
# AI COMPLETION FOR UNKNOWN FIELDS
# =====================================================
def ai_fill_unknowns(hero_name: str, build_text: str):
    if "Unknown" not in build_text:
        return build_text

    prompt = f"""
Infinity Kingdom only use actual in-game artifact data.
Hero: {hero_name}

Reference artifact stats:
Primary rolls: Physical Attack %, Magical Attack %, Crit Rate %, Crit Damage %, Defense %, Health %, etc.
Secondary rolls: Physical Attack %, Magical Attack %, Crit Rate %, Dodge Rate %, Block Rate %, Defense %, HP %, Healing %, etc.
Bonus rolls: Iron Fist, Annihilation, Deadly, Growth, Guard, Shining Light, Surge, Eternal, etc.

Current TL;DR build (fill Unknowns only):

{build_text}

Please fill only valid artifact stats or passives according to official Infinity Kingdom game data. Do NOT invent artifacts. Respond ONLY with the updated TL;DR build in the same format. Leave 'Unknown' if data is not available.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=300
        )
        content = response.choices[0].message.content.strip()
        return content if content else build_text
    except Exception as e:
        print("[ERROR] AI failed to fill unknowns:", repr(e))
        traceback.print_exc()
        return build_text

# =====================================================
# GET HERO BUILD
# =====================================================
def get_hero_build(name: str):
    name_lower = name.lower()
    hero_info = HERO_INFO.get(name_lower, {"full": name.title(), "short": name.title()})
    hero_full = hero_info["full"]
    hero_short = hero_info["short"]

    build_text = f"""✨ TL;DR – Best Artifact for {hero_full}
⭐ Best Artifact: Unknown
⚔️ Best Main Stat: Unknown
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown"""

    build_filled = ai_fill_unknowns(hero_full, build_text)
    return hero_full, hero_short, build_filled

# =====================================================
# DISCORD BOT
# =====================================================
discord_token = os.environ.get("DISCORD_TOKEN")
if not discord_token:
    raise ValueError("DISCORD_TOKEN environment variable is missing!")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user} | Slash commands synced")

# =====================================================
# SLASH COMMAND
# =====================================================
@bot.tree.command(
    name="bestartifact",
    description="Get the best artifact build for any immortal"
)
@app_commands.describe(immortal="Name of the immortal (e.g., Himiko, Wu, Alex)")
async def bestartifact(interaction: discord.Interaction, immortal: str):
    name = immortal.strip()

    try:
        await interaction.response.defer()
    except Exception as e:
        print("[WARNING] Defer failed:", repr(e))
        return

    try:
        hero_full, hero_short, build_text = await asyncio.to_thread(get_hero_build, name)
    except Exception as e:
        print("[ERROR] Failed to get build:", repr(e))
        await interaction.followup.send("Error fetching artifact build.")
        return

    embed = discord.Embed(
        title=f"✨ TL;DR – Best Artifact for {hero_short}",
        description=build_text,
        color=discord.Color.gold()
    )

    await interaction.followup.send(embed=embed)

# =====================================================
# RUN BOT
# =====================================================
bot.run(discord_token)
