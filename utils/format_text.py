import discord
import re

# Cargar texto, separarlo en texto y autores
def load_txt_file(txtFile: str):
    frases = []
    with open(txtFile, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            texto, authorsRaw = line.split("=")
            texto = texto.replace("\\n", "\n")
            frases.append((texto, authorsRaw))
    return frases

# Separar autores , obtener apodo de autores
async def separate_authors(interaction, authorsRaw):
    guild = interaction.guild

    authorsAsIDs = re.findall(r'\d+', authorsRaw)
    IDsAsInt = [int(ids) for ids in authorsAsIDs]

    for id in IDsAsInt:
        member = None
        if guild:
            member = guild.get_member(id)
        if member:
            authorsRaw = authorsRaw.replace(f"{id}", f"{member.display_name}", 1)
            continue

        userAuthor = interaction.client.get_user(id)
        if userAuthor is None:
            try:
                userAuthor = await interaction.client.fetch_user(id)
            except discord.NotFound:
                userAuthor = None
        if userAuthor:
            authorsRaw = authorsRaw.replace(f"{id}", f"{userAuthor.name}", 1)
        else:
            authorsRaw = authorsRaw.replace(f"{id}", "Usuario Desconocido", 1)
    return authorsRaw