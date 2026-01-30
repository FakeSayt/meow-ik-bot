from discord import app_commands, Interaction
from helpers import get_hero_build

async def setup(bot):
    @bot.tree.command(name="bestartifact", description="Get the best artifact build for any immortal")
    @app_commands.describe(immortal="Name of the immortal (e.g., Himiko, Wu, Alex)")
    async def bestartifact(interaction: Interaction, immortal: str):
        await interaction.response.defer()
        build_text = await asyncio.to_thread(get_hero_build, immortal)
        await interaction.followup.send(build_text)
