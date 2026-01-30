from discord import app_commands, Embed
from discord.ext import commands

async def setup(bot):
    @bot.tree.command(
        name="helpmeow",
        description="Show all available bot commands"
    )
    async def helpmeow(interaction):
        embed = Embed(
            title="😺 Bot Command Help",
            description="Here are all available commands:",
            color=0x3498DB
        )
        embed.add_field(name="/bestartifact <immortal>", value="Get the best artifact build for any immortal.", inline=False)
        embed.add_field(name="/damage <mage1> <mage2>", value="Compare ultimate skill DPS of two mages.", inline=False)
        embed.add_field(name="/helpmeow", value="Show this help message.", inline=False)

        await interaction.response.send_message(embed=embed)
