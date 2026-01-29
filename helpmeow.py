import discord
from discord import app_commands

class HelpMeowCommand(app_commands.Group):
    @app_commands.command(
        name="helpmeow",
        description="Show all available bot commands and how to use them"
    )
    async def helpmeow(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📜 IK Bot Commands Help",
            color=discord.Color.blue(),
            description="Here are the available commands and how to use them:"
        )

        embed.add_field(
            name="/bestartifact <immortal>",
            value="Get the best artifact build for any immortal.\nExample: `/bestartifact Himiko`",
            inline=False
        )
        embed.add_field(
            name="/damage <mage1> <mage2>",
            value="Compare two mage immortals ultimate damage.\nExample: `/damage Merlin Himiko`",
            inline=False
        )
        embed.add_field(
            name="/helpmeow",
            value="Show this help message.",
            inline=False
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)
