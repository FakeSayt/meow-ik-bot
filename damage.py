from discord import app_commands, Interaction
from mage_stats import MAGE_STATS
from heroes import HERO_INFO

async def setup(bot):
    @bot.tree.command(name="damage", description="Compare two mage immortals damage")
    @app_commands.describe(immortal1="First mage immortal", immortal2="Second mage immortal")
    async def damage(interaction: Interaction, immortal1: str, immortal2: str):
        imm1 = immortal1.lower()
        imm2 = immortal2.lower()

        if imm1 not in MAGE_STATS or imm2 not in MAGE_STATS:
            return await interaction.response.send_message("One or both immortals not found or not mages!")

        stats1 = MAGE_STATS[imm1]
        stats2 = MAGE_STATS[imm2]

        msg = (
            f"**{HERO_INFO[imm1]['full']} vs {HERO_INFO[imm2]['full']}**\n"
            f"{stats1['dps']} DPS vs {stats2['dps']} DPS\n"
            f"Single-target: {stats1['single_target']} vs {stats2['single_target']}\n"
            f"Four-target: {stats1['four_target']} vs {stats2['four_target']}\n"
            f"Special: {stats1['special']} vs {stats2['special']}"
        )
        await interaction.response.send_message(msg)
