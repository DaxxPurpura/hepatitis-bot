import discord
from datetime import datetime

def info_commands(tree, serverList, botVersion, botRepo, initTime):
    @tree.command(name="verfrases", description="Muestra la lista de frases para saber el índice de cada frase", guilds=serverList)
    async def ver_frases(interaction: discord.Interaction):
        lines = []
        with open("frases.txt", "r", encoding="utf-8") as file:
            for i, line in enumerate(file, start=1):
                line = line.strip()
                frase, __ = line.split("=")
                frase = frase.replace("#", "")
                frase = frase.replace("\\n", " |")
                lines.append(f"{i}: {frase}")
            texto = "\n".join(lines)
            embed = discord.Embed(description=texto)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tree.command(name="veropiniones", description="Muestra la lista de opiniones para saber el índice de cada opinión", guilds=serverList)
    async def ver_opiniones(interaction: discord.Interaction):
        lines = []
        with open("opiniones.txt", "r", encoding="utf-8") as file:
            for i, line in enumerate(file, start=1):
                line = line.strip()
                line = line.replace("#", "")
                lines.append(f"{i}: {line}")
            texto = "\n".join(lines)
            embed = discord.Embed(description=texto)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tree.command(name="verfunfacts", description="Muestra la lista de factos jijosos para saber el índice de cada facto jijoso", guilds=serverList)
    async def ver_fun_facts(interaction: discord.Interaction):
        lines = []
        with open("fun_facts.txt", "r", encoding="utf-8") as file:
            for i, line in enumerate(file, start=1):
                line = line.strip()
                line = line.replace("#", "")
                line = line.replace("\\n", "")
                lines.append(f"{i}: {line}")
            texto = "\n".join(lines)
            embed = discord.Embed(description=texto)
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

    @tree.command(name="crouch", description="Muestra las Horas y minutos que Se llevandesde que se inició Hepatitis B(ot)", guilds=serverList)
    async def crouch(interaction: discord.Interaction):
        currentTime = int((datetime.now() - initTime).total_seconds())
        hours, left = divmod(currentTime, 3600)
        minutes, __ = divmod(left, 60)
        embed = discord.Embed(description=f"## Se llevan{hours} Horas y {minutes} minutos")
        await interaction.response.send_message(embed=embed)