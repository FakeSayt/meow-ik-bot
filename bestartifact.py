from discord import app_commands, Embed
from discord.ext import commands
from helpers import get_hero_build

async def setup(bot):
    @bot.tree.command(
        name="bestartifact",
        description="Get the best artifact build for any immortal"
    )
    @app_commands.describe(immortal="Name of the immortal (e.g., Himiko, Wu, Alex)")
    async def bestartifact(interaction, immortal: str):
        await interaction.response.defer()
        build_text = await commands.bot._get_loop().run_in_executor(None, get_hero_build, immortal)
        embed = Embed(
            title=f"✨ TL;DR – Best Artifact for {immortal.title()}",
            description=build_text,
            color=0xFFD700
        )
        await interaction.followup.send(embed=embed)
