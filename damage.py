import discord
from discord import app_commands
from mage_stats import MAGE_STATS

class DamageCommand(app_commands.Group):
    @app_commands.command(
        name="damage",
        description="Compare two mage immortals ultimate damage"
    )
    @app_commands.describe(
        mage1="First mage immortal",
        mage2="Second mage immortal"
    )
    async def damage(self, interaction: discord.Interaction, mage1: str, mage2: str):
        m1 = mage1.strip().lower()
        m2 = mage2.strip().lower()

        if m1 not in MAGE_STATS or m2 not in MAGE_STATS:
            await interaction.response.send_message("One or both mages not found.", ephemeral=True)
            return

        stats1 = MAGE_STATS[m1]
        stats2 = MAGE_STATS[m2]
        better_dps = mage1 if stats1["dps"] >= stats2["dps"] else mage2

        embed = discord.Embed(
            title=f"⚡ Mage Ultimate Damage: {mage1.title()} vs {mage2.title()}",
            color=discord.Color.purple()
        )
        embed.add_field(
            name=mage1.title(),
            value=f"Element: {stats1['element']}\n"
                  f"Single Target: {stats1['single_target']}%\n"
                  f"4 Targets: {stats1['four_target']}%\n"
                  f"Energy Regen: {stats1['energy_regen']}\n"
                  f"Skill/sec: {stats1['skill_per_sec']}\n"
                  f"DPS: {stats1['dps']}\n"
                  f"Special: {stats1['special']}",
            inline=True
        )
        embed.add_field(
            name=mage2.title(),
            value=f"Element: {stats2['element']}\n"
                  f"Single Target: {stats2['single_target']}%\n"
                  f"4 Targets: {stats2['four_target']}%\n"
                  f"Energy Regen: {stats2['energy_regen']}\n"
                  f"Skill/sec: {stats2['skill_per_sec']}\n"
                  f"DPS: {stats2['dps']}\n"
                  f"Special: {stats2['special']}",
            inline=True
        )
        embed.set_footer(text=f"Better DPS: {better_dps.title()} ✅")
        await interaction.response.send_message(embed=embed)
