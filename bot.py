import os
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread
import asyncio
import traceback
from openai import OpenAI

# Importujemy heroes info z osobnego pliku
from heroes import HERO_INFO, HERO_PRICE

# =====================================================
# WEB SERVER
# =====================================================
app = Flask(__name__)

@app.route("/")
def home():
    return "Discord bot is running!"

Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))).start()

# =====================================================
# OPENAI CLIENT
# =====================================================
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is missing!")

client = OpenAI(api_key=openai_api_key)

# =====================================================
# AI COMPLETION FOR UNKNOWN FIELDS
# =====================================================
def ai_fill_unknowns(hero_name: str, role: str, build_text: str):
    if "Unknown" not in build_text:
        return build_text

    prompt = f"""
You are an expert in Infinity Kingdom mobile game. Only use actual in-game artifact data.
Hero: {hero_name}
Role: {role}

Primary Rolls:
- Attack: Physical Attack % / Physical Attack Value / Magical Defense % / Magical Defense Value
- Tank: Physical Defense % / Physical Defense Value / Resilience % / Resilience Value
- Mage: Crit Rate % / Crit Value / Magical Attack % / Magical Attack Value
- Ranged: Physical Attack % / Physical Attack Value / Accuracy % / Accuracy Value
- Support: Physical Attack % / Physical Attack Value / Dodge % / Dodge Value

Secondary Rolls: any of the 16 possible rolls (Physical/Magical Attack %, Value, Crit %, Crit Value, Accuracy, Dodge, Defense, Resilience, etc.)

Bonus Rolls:
- Attack / Ranged: Iron Fist
- Attack / Support: Surge
- Defense: Growth / Guard
- Mage: Annihilation / Deadly
- Support: Shining Light

Current TL;DR build (fill Unknowns only):

{build_text}

Please provide ONLY valid artifact stats or passives according to official Infinity Kingdom game data. Do NOT invent artifacts. Leave 'Unknown' if not available.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=350
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
    hero_info = HERO_INFO.get(name_lower, {"full": name.title(), "short": name.title(), "role": "Attack"})
    hero_full = hero_info["full"]
    hero_short = hero_info["short"]
    hero_role = hero_info["role"]

    build_text = f"""✨ TL;DR – Best Artifact for {hero_full}
⭐ Best Artifact: Unknown
⚔️ Best Main Stat: Unknown
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown"""

    build_filled = ai_fill_unknowns(hero_full, hero_role, build_text)
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

    await interaction.response.defer()
    try:
        hero_full, hero_short, build_text = await asyncio.to_thread(get_hero_build, name)
    except Exception as e:
        print("[ERROR] Failed to get build:", repr(e))
        await interaction.followup.send("Error fetching artifact build.")
        return

    tier_text = HERO_PRICE.get(name.lower(), "Unknown Tier")
    embed = discord.Embed(
        title=f"✨ TL;DR – Best Artifact for {hero_short}",
        description=build_text,
        color=discord.Color.gold()
    )
    embed.add_field(name="💎 Immortal Tier", value=tier_text, inline=False)

    await interaction.followup.send(embed=embed)

# =====================================================
# RUN BOT
# =====================================================
bot.run(discord_token)
