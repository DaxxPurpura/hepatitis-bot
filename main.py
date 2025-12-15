import discord
from discord import app_commands
from dotenv import load_dotenv
import logging
import os
import random
import time

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

BOT_VERSION = "1.0.0"

# Servers autorizados
# Agregá tu server para poder testear los comandos allá
HEPATITIS = discord.Object(id=1018626508853629149)
TEST = discord.Object(id=1449941097299050649)

# Sincronizar servers
@client.event
async def on_ready():
    await tree.sync(guild=HEPATITIS)
    await tree.sync(guild=TEST)

# Cargar frases. Separarlas en frase y autores.
def load_frases():
    frases = []
    with open("frases.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            texto, authorRaw = line.split("=", 1)
            texto = texto.replace("\\n", "\n")

            authorsID = [int(uid.strip()) for uid in authorRaw.split("|") if uid.strip().isdigit()]
            frases.append((texto, authorsID))
    return frases

FRASES = load_frases()
last_frase = ""
FRASES_COOLDOWN = 60
NO_COOLDOWN = 528940084142014484
cooldowns = {}

# Obtener el tiempo restante de cooldown de UserID
def get_time_left(userID):
    if userID not in cooldowns:
        return 0
    timeLeft = FRASES_COOLDOWN - (time.time() - cooldowns[userID])
    return timeLeft

# Obtener apodo de autores. Separar autores
async def SeparateAuthors(interaction, authorsID):
    authors = []
    guild = interaction.guild

    for userAuthor in authorsID:
        member = None
        if guild:
            member = guild.get_member(userAuthor)
        if member:
            authors.append(member.display_name)
            continue

        fraseAuthor = interaction.client.get_user(userAuthor)
        if fraseAuthor is None:
            try:
                fraseAuthor = await interaction.client.fetch_user(userAuthor)
            except discord.NotFound:
                fraseAuthor = None
        if fraseAuthor:
            authors.append(fraseAuthor.name)
        else:
            authors.append("Usuario Desconocido")
    
    return authors

# Agregá tu server a `guilds` para que el comando aparezca en tu server
@tree.command(name="frasefunny", description="Invoca una frase del museo de frases", guilds=[HEPATITIS, TEST])
async def frasefunny(interaction: discord.Interaction):
    userID = interaction.user.id
    global last_frase
    
    if userID != NO_COOLDOWN:
        TimeLeft = get_time_left(userID)
        if TimeLeft > 0:
            embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{round(TimeLeft)} segundos** para volver a usarlo.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        cooldowns[userID] = time.time()
    
    frase, userAuthors = random.choice(FRASES)
    while frase == last_frase:
        frase, userAuthors = random.choice(FRASES)
    last_frase = frase

    fraseAuthor = await SeparateAuthors(interaction, userAuthors)
    text = "ㅤ|ㅤ".join(fraseAuthor)
    embed = discord.Embed(description=f"{frase} \n### -ㅤ{text}")
    await interaction.response.send_message(embed=embed)

# Agregá tu server a `guilds` para que el comando aparezca en tu server
@tree.command(name="forzarfrase", description="Fuerza una frase del museo de frases", guilds=[HEPATITIS, TEST])
async def forzarfrase(interaction: discord.Interaction, index: int):
    realIndex = index - 1
    if realIndex < 0 or realIndex >= len(FRASES):
        embed = discord.Embed(description=f"# Ups! Esa frase no existe, tonoto")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    frase, userAuthors = FRASES[realIndex]
    fraseAuthor = await SeparateAuthors(interaction, userAuthors)
    text = "ㅤ|ㅤ".join(fraseAuthor)
    embed = discord.Embed(description=f"{frase} \n### -ㅤ{text}")
    await interaction.response.send_message(embed=embed)

# Agregá tu server a `guilds` para que el comando aparezca en tu server
@tree.command(name="versionhepatitis", description="Muestra la versión del Hepatitis B(ot)", guilds=[HEPATITIS, TEST])
async def forzarfrase(interaction: discord.Interaction):
    await interaction.response.send_message(BOT_VERSION, ephemeral=True)

client.run(token, log_handler=handler, log_level=logging.DEBUG)