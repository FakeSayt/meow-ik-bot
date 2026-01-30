from discord import app_commands, Embed
from discord.ext import commands
from mage_stats import MAGE_STATS
from heroes import HERO_INFO

async def setup(bot):
    @bot.tree.command(
        name="damage",
        description="Compare ultimate skill DPS of two mages"
    )
    @app_commands.describe(immortal1="First mage", immortal2="Second mage")
    async def damage(interaction, immortal1: str, immortal2: str):
        immortal1 = immortal1.lower()
        immortal2 = immortal2.lower()

        data1 = MAGE_STATS.get(immortal1)
        data2 = MAGE_STATS.get(immortal2)

        if not data1 or not data2:
            await interaction.response.send_message("One or both mages not found!")
            return

        embed = Embed(
            title=f"⚡ Damage Comparison: {immortal1.title()} vs {immortal2.title()}",
            color=0x00FF00
        )

        embed.add_field(
            name=f"{immortal1.title()}",
            value=(
                f"Element: {data1['element']}\n"
                f"Single Target: {data1['single_target']}%\n"
                f"4 Targets: {data1['four_target']}%\n"
                f"Energy Regen: {data1['energy_regen']}\n"
                f"Skill/Sec: {data1['skill_per_sec']}\n"
                f"DPS: {data1['dps']}\n"
                f"Special: {data1['special']}"
            ),
            inline=True
        )

        embed.add_field(
            name=f"{immortal2.title()}",
            value=(
                f"Element: {data2['element']}\n"
                f"Single Target: {data2['single_target']}%\n"
                f"4 Targets: {data2['four_target']}%\n"
                f"Energy Regen: {data2['energy_regen']}\n"
                f"Skill/Sec: {data2['skill_per_sec']}\n"
                f"DPS: {data2['dps']}\n"
                f"Special: {data2['special']}"
            ),
            inline=True
        )

        better = immortal1 if data1['dps'] >= data2['dps'] else immortal2
        embed.set_footer(text=f"Highest DPS: {better.title()}")
        await interaction.response.send_message(embed=embed)
