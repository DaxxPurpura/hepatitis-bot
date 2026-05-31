import re

# Cargar texto, separarlo en texto y autores si hay
def load_text(txtFile: str):
    frases = []
    with open(txtFile, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            
            if "=" in line:
                texto, authorsRaw = line.split("=")
                texto = texto.replace("\\n", "\n")
                frases.append((texto, authorsRaw))
            else:
                line = line.replace("\\n", "\n")
                frases.append(line)
    return frases

# Separar texto , obtener usuarios/emojis
async def format_text(interaction, textRaw: str, type: str):
    textAsIDs = re.findall(r'\d+', textRaw)
    IDsAsInt = [int(ids) for ids in textAsIDs]

    for id in IDsAsInt:
        if type == "user":
            guild = interaction.guild
            if guild:
                member = guild.get_member(id)
                if member:
                    textRaw = textRaw.replace(f"{id}", f"{member.display_name}", 1)
                    continue

            userAuthor = interaction.client.get_user(id)
            if userAuthor:
                textRaw = textRaw.replace(f"{id}", f"{userAuthor.name}", 1)
            else:
                textRaw = textRaw.replace(f"{id}", "Usuario Desconocido", 1)
        elif type == "emoji":
            guild = interaction.guild
            if guild:
                emoji = guild.get_emoji(id)
                if emoji:
                    textRaw = textRaw.replace(f"{id}", f"{emoji}")
                    continue
            
            textRaw = textRaw.replace(f"{id}", "")
    return textRaw

async def format_frase(interaction, fraseRaw: str, authorsRaw: str):
    authorsRaw = authorsRaw.replace("+", "ㅤ|ㅤ")
    authorsRawNew = authorsRaw
    authorsDisplay = authorsRaw
    guild = interaction.guild
    if guild:
        authors = re.findall(r"\{(.*?)\}", authorsRaw)
        for author in authors:
            member = guild.get_member_named(author)
            if not member:
                continue

            authorsDisplay = authorsDisplay.replace(f"{{{author}}}", str(f"{member.display_name} ({member.name})"))
            authorsRawNew = authorsRawNew.replace(f"{{{author}}}", str(member.id))
    
    frase = fraseRaw.replace("{", "❝").replace("}", "❞").replace("+", "\n## ")
    frase = "## " + frase
    authorsDisplay = authorsDisplay.replace("{", "").replace("}", "")
    authorsRawNew = authorsRawNew.replace("{", "").replace("}", "")
    return frase, authorsRawNew, authorsDisplay