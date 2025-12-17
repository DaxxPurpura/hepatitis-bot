import discord

def info_commands(tree, serverList, botVersion, botRepo):
    @tree.command(name="frases", description="Muestra la lista de frases para saber el índice de cada frase", guilds=serverList)
    async def frases(interaction: discord.Interaction):
        with open("frases.txt", "r", encoding="utf-8") as file:
            embed = discord.Embed(description=f"```{file.read()}```")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tree.command(name="opiniones", description="Muestra la lista de opiniones para saber el índice de cada opinión", guilds=serverList)
    async def opiniones(interaction: discord.Interaction):
        with open("opiniones.txt", "r", encoding="utf-8") as file:
            embed = discord.Embed(description=f"```{file.read()}```")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tree.command(name="funfacts", description="Muestra la lista de factos jijosos para saber el índice de cada facto jijoso", guilds=serverList)
    async def funfacts(interaction: discord.Interaction):
        with open("fun_facts.txt", "r", encoding="utf-8") as file:
            embed = discord.Embed(description=f"```{file.read()}```")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tree.command(name="version", description="Muestra la versión de Hepatitis B(ot)", guilds=serverList)
    async def version(interaction: discord.Interaction):
        embed = discord.Embed(description=f"## {botVersion}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tree.command(name="repo", description="Muestra el repositorio de GitHub de Hepatitis B(ot)", guilds=serverList)
    async def repo(interaction: discord.Interaction):
        await interaction.response.send_message(botRepo, ephemeral=True)

    @tree.command(name="changelog", description="Muestra el changelog de Hepatitis B(ot)", guilds=serverList)
    async def changelog(interaction: discord.Interaction):
        with open("CHANGELOG.md", "r", encoding="utf-8") as file:
            embed = discord.Embed(description=f"{file.read()}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tree.command(name="ayuda", description="Muestra todos los comandos de Hepatitis B(ot), sus funciones y cooldowns", guilds=serverList)
    async def ayuda(interaction: discord.Interaction):
        with open("ayuda.txt", "r", encoding="utf-8") as file:
            embed = discord.Embed(description=f"{file.read()}")
        await interaction.response.send_message(embed=embed, ephemeral=True)