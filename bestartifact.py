import discord
from discord import app_commands
from helpers import get_hero_build
from heroes import HERO_PRICE

class BestArtifactCommand(app_commands.Group):
    @app_commands.command(
        name="bestartifact",
        description="Get the best artifact build for any immortal"
    )
    @app_commands.describe(immortal="Name of the immortal (e.g., Himiko, Wu, Alex)")
    async def bestartifact(self, interaction: discord.Interaction, immortal: str):
        name = immortal.strip()
        await interaction.response.defer()
        build_text = await discord.utils.run_in_executor(None, get_hero_build, name)
        tier = HERO_PRICE.get(name.lower(), "Unknown Tier")

        embed = discord.Embed(
            title=f"✨ TL;DR – Best Artifact for {name.title()}",
            description=build_text,
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Tier: {tier}")
        await interaction.followup.send(embed=embed)
