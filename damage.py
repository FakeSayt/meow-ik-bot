import discord
from discord import app_commands
from mage_stats import MAGE_STATS

async def setup(bot):
    @bot.tree.command(
        name="damage",
        description="Compare ultimate damage of two mage immortals"
    )
    @app_commands.describe(immortal1="First mage", immortal2="Second mage")
    async def damage(interaction: discord.Interaction, immortal1: str, immortal2: str):
        i1 = MAGE_STATS.get(immortal1.lower())
        i2 = MAGE_STATS.get(immortal2.lower())

        if not i1 or not i2:
            await interaction.response.send_message("Invalid immortal name(s).")
            return

        embed = discord.Embed(
            title=f"Damage Comparison: {immortal1.title()} vs {immortal2.title()}",
            color=discord.Color.orange()
        )

        for key in ["single_target", "four_target", "energy_regen", "dps", "special"]:
            embed.add_field(
                name=key.replace("_", " ").title(),
                value=f"{i1.get(key)} vs {i2.get(key)}",
                inline=False
            )
        await interaction.response.send_message(embed=embed)
