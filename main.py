import discord
from discord.ext import commands
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
bot = commands.Bot(command_prefix='/', intents=intents)
tree = bot.tree

ELMASCAPITO = 528940084142014484
BOT_VERSION = "1.1.0"

# Servers autorizados
# Agregá tu server para poder testear los comandos allá
HEPATITIS = discord.Object(id=1018626508853629149)
TEST = discord.Object(id=1449941097299050649)

# Sincronizar servers
@bot.event
async def on_ready():
    await tree.sync(guild=HEPATITIS)
    await tree.sync(guild=TEST)

    global MASCOTAS
    MASCOTAS = await load_mascotas()

# No le den importancia, funciona solo con ELMASCAPITO B)
@bot.event
async def on_message(message):
    if message.author.id != ELMASCAPITO:
        return
    
    if "/mensaje" in message.content:
        actualMessage = message.content.replace("/mensaje", "")
        await message.delete()
        if message.reference is None:
            await message.channel.send(actualMessage)
            return
        uffReferencia = message.reference
        channel = bot.get_channel(uffReferencia.channel_id)
        replyMessage = await channel.fetch_message(uffReferencia.message_id)
        await replyMessage.reply(actualMessage)

    elif "/reaccion" in message.content:
        actualMessage = message.content.replace("/reaccion ", "")
        await message.delete()
        if message.reference is not None:
            uffReferencia = message.reference
            channel = bot.get_channel(uffReferencia.channel_id)
            reactMessage = await channel.fetch_message(uffReferencia.message_id)
            await reactMessage.add_reaction(actualMessage)

    elif "/noreaccion" in message.content:
        actualMessage = message.content.replace("/noreaccion ", "")
        await message.delete()
        if message.reference is not None:
            uffReferencia = message.reference
            channel = bot.get_channel(uffReferencia.channel_id)
            reactMessage = await channel.fetch_message(uffReferencia.message_id)
            await reactMessage.remove_reaction(actualMessage, bot.user)
    
    await bot.process_commands(message)

# Agregá tu server a `guilds` para que el comando aparezca en tu server
@tree.command(name="versionhepatitis", description="Muestra la versión del Hepatitis B(ot)", guilds=[HEPATITIS, TEST])
async def version(interaction: discord.Interaction):
    await interaction.response.send_message(BOT_VERSION, ephemeral=True)

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
lastFrase = ""
FRASES_COOLDOWN = 60
fraseCooldowns = {}

# Obtener el tiempo restante de cooldown de UserID
def get_time_left(userID, command: str):
    if command == "frasefunny":
        if userID not in fraseCooldowns:
            return 0
        timeLeft = FRASES_COOLDOWN - (time.time() - fraseCooldowns[userID])
        return timeLeft
    elif command == "mascota":
        if userID not in mascotaCooldowns:
            return 0
        timeLeft = MASCOTA_COOLDOWN - (time.time() - mascotaCooldowns[userID])
        return timeLeft

# Obtener apodo de autores. Separar autores
async def separate_authors(interaction, authorsID):
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
async def frase_funny(interaction: discord.Interaction):
    userID = interaction.user.id
    global lastFrase
    
    if userID != ELMASCAPITO:
        TimeLeft = get_time_left(userID, "frasefunny")
        if TimeLeft > 0:
            embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{round(TimeLeft)} segundos** para volver a usarlo.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        fraseCooldowns[userID] = time.time()
    
    frase, userAuthors = random.choice(FRASES)
    while frase == lastFrase:
        frase, userAuthors = random.choice(FRASES)
    lastFrase = frase

    fraseAuthor = await separate_authors(interaction, userAuthors)
    text = "ㅤ|ㅤ".join(fraseAuthor)
    embed = discord.Embed(description=f"{frase} \n### -ㅤ{text}")
    await interaction.response.send_message(embed=embed)

# Agregá tu server a `guilds` para que el comando aparezca en tu server
@tree.command(name="forzarfrase", description="Fuerza una frase del museo de frases", guilds=[HEPATITIS, TEST])
async def forzar_frase(interaction: discord.Interaction, index: int):
    realIndex = index - 1
    if realIndex < 0 or realIndex >= len(FRASES):
        embed = discord.Embed(description=f"# Ups! Esa frase no existe, tonoto")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    frase, userAuthors = FRASES[realIndex]
    fraseAuthor = await separate_authors(interaction, userAuthors)
    text = "ㅤ|ㅤ".join(fraseAuthor)
    embed = discord.Embed(description=f"{frase} \n### -ㅤ{text}")
    await interaction.response.send_message(embed=embed)

CANALMASCOTAS = 1442192026962759795

async def load_mascotas():
    mascotas = []

    async for message in bot.get_channel(CANALMASCOTAS).history():
        if message.attachments == []:
            continue

        for attachment in message.attachments:
            mascotas.append(attachment)
    
    return mascotas

MASCOTAS = []
lastMascota = 0
MASCOTA_COOLDOWN = 60
mascotaCooldowns = {}

# Agregá tu server a `guilds` para que el comando aparezca en tu server
@tree.command(name="mascota", description="Invoca una mascota de mascotas", guilds=[HEPATITIS, TEST])
async def mascota(interaction: discord.Interaction):
    userID = interaction.user.id
    global lastMascota
    
    if userID != ELMASCAPITO:
        TimeLeft = get_time_left(userID, "mascota")
        if TimeLeft > 0:
            embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{round(TimeLeft)} segundos** para volver a usarlo.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        mascotaCooldowns[userID] = time.time()
    
    mascota = random.choice(MASCOTAS)
    while mascota == lastMascota:
        mascota = random.choice(MASCOTAS)
    lastMascota = mascota

    await interaction.response.send_message(mascota)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)