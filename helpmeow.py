import discord
from discord import app_commands

async def setup(bot):
    @bot.tree.command(
        name="helpmeow",
        description="Show all available commands and usage"
    )
    async def helpmeow(interaction: discord.Interaction):
        embed = discord.Embed(
            title="Bot Commands Help",
            description="""
/bestartifact <immortal> - Get TL;DR best artifact build
/damage <immortal1> <immortal2> - Compare ultimate damage of two mages
/helpmeow - Show this help
""",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)
