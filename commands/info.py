import discord

def info_commands(tree, serverList, botVersion, botRepo):
    @tree.command(name="versionhepatitis", description="Muestra la versión de Hepatitis B(ot)", guilds=serverList)
    async def version(interaction: discord.Interaction):
        await interaction.response.send_message(botVersion, ephemeral=True)

    @tree.command(name="repohepatitis", description="Muestra el repositorio de GitHub de Hepatitis B(ot)", guilds=serverList)
    async def repo(interaction: discord.Interaction):
        await interaction.response.send_message(botRepo, ephemeral=True)