import discord
from discord import app_commands
from helpers import get_hero_build

async def setup(bot):
    @bot.tree.command(
        name="bestartifact",
        description="Get the best artifact build for any immortal"
    )
    @app_commands.describe(immortal="Name of the immortal (e.g., Himiko, Wu, Alex)")
    async def bestartifact(interaction: discord.Interaction, immortal: str):
        name = immortal.strip()
        await interaction.response.defer()
        build_text = await asyncio.to_thread(get_hero_build, name)
        embed = discord.Embed(
            title=f"✨ TL;DR – Best Artifact for {name.title()}",
            description=build_text,
            color=discord.Color.gold()
        )
        await interaction.followup.send(embed=embed)
