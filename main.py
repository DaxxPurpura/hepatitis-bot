import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import os
import random
import re
import time

load_dotenv()
token = os.getenv('DISCORD_TOKEN') # Agregá el token de tu bot al .env
serverID = os.getenv('TEST_SERVER') # Agregá el ID de tu server al .env
godUserID = int(os.getenv('GOD_USER')) # Agregá tu ID de usuario al .env

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents)
tree = bot.tree

BOT_VERSION = "1.1.2"
BOT_REPO = "https://github.com/DaxxPurpura/hepatitis-bot"

# Servers autorizados
HEPATITIS = discord.Object(id=1018626508853629149)
TEST = discord.Object(id=serverID)

# Sincronizar servers
@bot.event
async def on_ready():
    await tree.sync(guild=HEPATITIS)
    await tree.sync(guild=TEST)

    global MASCOTAS
    MASCOTAS = await load_mascotas()


@bot.event
async def on_message(message):
    # Actualiza la lista MASCOTAS con nuevas imagenes
    if message.channel.id == CANALMASCOTAS and message.attachments:
        for attachment in message.attachments:
            MASCOTAS.append(attachment)

    # No le den importancia, funciona solo con godUserID B)
    if message.author.id != godUserID:
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

# Agregá tu server a `guilds` para que el comando aparezca en tu server
@tree.command(name="repohepatitis", description="Muestra la versión del Hepatitis B(ot)", guilds=[HEPATITIS, TEST])
async def repo(interaction: discord.Interaction):
    await interaction.response.send_message(BOT_REPO, ephemeral=True)

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

# Cargar frases , separarlas en frase y autores
def load_frases():
    frases = []
    with open("frases.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            texto, authorsRaw = line.split("=")
            texto = texto.replace("\\n", "\n")
            frases.append((texto, authorsRaw))
    return frases

FRASES = load_frases()
lastFrase = ""
FRASES_COOLDOWN = 60
fraseCooldowns = {}

# Obtener apodo de autores , separar autores
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

# Agregá tu server a `guilds` para que el comando aparezca en tu server
@tree.command(name="frasefunny", description="Invoca una frase del museo de frases", guilds=[HEPATITIS, TEST])
async def frase_funny(interaction: discord.Interaction):
    userID = interaction.user.id
    global lastFrase
    
    if userID != godUserID:
        TimeLeft = get_time_left(userID, "frasefunny")
        if TimeLeft > 0:
            embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{round(TimeLeft)} segundos** para volver a usarlo.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        fraseCooldowns[userID] = time.time()
    
    frase, authorsRaw = random.choice(FRASES)
    while frase == lastFrase:
        frase, authorsRaw = random.choice(FRASES)
    lastFrase = frase

    authors = await separate_authors(interaction, authorsRaw)
    embed = discord.Embed(description=f"{frase} \n### -ㅤ{authors}")
    await interaction.response.send_message(embed=embed)

# Agregá tu server a `guilds` para que el comando aparezca en tu server
@tree.command(name="forzarfrase", description="Fuerza una frase del museo de frases", guilds=[HEPATITIS, TEST])
async def forzar_frase(interaction: discord.Interaction, index: int):
    realIndex = index - 1
    if realIndex < 0 or realIndex >= len(FRASES):
        embed = discord.Embed(description=f"## ¡Ups! \n### Esa frase no existe, tonoto")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    frase, authorsRaw = FRASES[realIndex]
    authors = await separate_authors(interaction, authorsRaw)
    embed = discord.Embed(description=f"{frase} \n### -ㅤ{authors}")
    await interaction.response.send_message(embed=embed)

CANALMASCOTAS = 1442192026962759795

# Cargar mascotas , separar archivos en un mismo mensaje
async def load_mascotas():
    mascotas = []

    channel = await bot.fetch_channel(CANALMASCOTAS)

    async for message in channel.history():
        if not message.attachments:
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
    
    if userID != godUserID:
        TimeLeft = get_time_left(userID, "mascota")
        if TimeLeft > 0:
            embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{round(TimeLeft)} segundos** para volver a usarlo.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        mascotaCooldowns[userID] = time.time()

    if not MASCOTAS:
        await interaction.response.send_message("No hay mascotas cargadas", ephemeral=True)
        return
    
    mascota = random.choice(MASCOTAS)
    while mascota == lastMascota:
        mascota = random.choice(MASCOTAS)
    lastMascota = mascota

    await interaction.response.send_message(mascota.url)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)