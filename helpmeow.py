from discord import app_commands, Interaction

async def setup(bot):
    @bot.tree.command(name="helpmeow", description="Show available commands")
    async def helpmeow(interaction: Interaction):
        embed = {
            "title": "Available Commands",
            "description": (
                "/bestartifact – Get best artifact build for any immortal\n"
                "/damage – Compare two mage immortal damage\n"
                "/helpmeow – Show this help menu"
            ),
        }
        await interaction.response.send_message(embed=embed)
