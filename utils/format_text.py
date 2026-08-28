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
    authorsRawNew = authorsRaw
    authorsDisplay = authorsRaw
    guild = interaction.guild
    if guild:
        authors = re.findall(r"\{(.*?)\}", authorsRaw)
        for author in authors:
            member = guild.get_member_named(author)
            if not member:
                member = check_manual_nicknames(author, guild)
            if not member:
                continue
                
            authorsRawNew = authorsRawNew.replace(f"{author}", str(member.id))
            authorsDisplay = authorsDisplay.replace(f"{author}", str(f"{member.display_name} ({member.name})"))
    
    isOpeningQuote = True
    for character in fraseRaw:
        if character != "\"":
            continue
        
        if isOpeningQuote:
            fraseRaw = fraseRaw.replace("\"", "❝", 1)
        else:
            fraseRaw = fraseRaw.replace("\"", "❞", 1)
        isOpeningQuote = not isOpeningQuote

    frase = "## " + fraseRaw.replace("\n", "\n## ")
    authorsRawNew = authorsRawNew.replace("}{", "ㅤ|ㅤ").replace("} {", "ㅤ|ㅤ").replace("{", "").replace("}", "")
    authorsDisplay = authorsDisplay.replace("}{", "ㅤ|ㅤ").replace("} {", "ㅤ|ㅤ").replace("{", "").replace("}", "")
    return frase, authorsRawNew, authorsDisplay

def check_manual_nicknames(author: str, guild):
    author = author.lower()
    if author == "abby":
        return guild.get_member(539460039178715149)
    elif author == "daxx":
        return guild.get_member(528940084142014484)
    elif author == "eduardo" or author == "edu":
        return guild.get_member(923004720900104224)
    elif author == "geo":
        return guild.get_member(476341482949705759)
    elif author == "haziel" or author == "haz":
        return guild.get_member(468293832283521024)
    elif author == "juani":
        return guild.get_member(611330643976126464)
    elif author == "kris":
        return guild.get_member(468213463840456713)
    elif author == "matías" or author == "matias" or author == "mati":
        return guild.get_member(836284886393946124)
    elif author == "mho" or author == "mhofrio":
        return guild.get_member(364507206118539264)
    elif author == "pandemonic" or author == "pande" or author == "tarkus" or author == "parsons":
        return guild.get_member(985241349357961356)
    elif author == "paulo":
        return guild.get_member(1449943226973683784)
    elif author == "rash":
        return guild.get_member(359729430463119361)