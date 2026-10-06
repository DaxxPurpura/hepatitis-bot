import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import os

from commands.adivinar import adivinar_commands
from commands.chistes import chistes_commands
from commands.control import control_commands
from commands.frases import frases_commands
from commands.fun_fact import fun_facts_commands
from commands.info import info_commands
from commands.mascotas import init_mascotas, mascotas_commands, update_mascotas
from commands.oye import oye_commands, detect_victims
from commands.que_opinas import opiniones_commands
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # Agregá el token de tu bot al .env
serverID = os.getenv('TEST_SERVER') # Agregá la ID de tu server al .env

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)
tree = bot.tree

GOD_USER_ID = 528940084142014484
botVersion = "1.6.3"
BOT_REPO = "https://github.com/DaxxPurpura/hepatitis-bot"
botVoiceClient = None
initTime = datetime.now()

# Servers autorizados
HEPATITIS = discord.Object(id=1018626508853629149)
PLANETA = discord.Object(id=1450568433467916533)
TEST = discord.Object(id=serverID)
SERVERS = [HEPATITIS, PLANETA, TEST]

CANALMASCOTAS = 1442192026962759795

# Sincronizar servers
@bot.event
async def on_ready():
    await tree.sync(guild=HEPATITIS)
    await tree.sync(guild=PLANETA)
    await tree.sync(guild=TEST)

    await init_mascotas(bot, CANALMASCOTAS)

@bot.event
async def on_message(message):
    update_mascotas(message, CANALMASCOTAS)

    await detect_victims(message, bot)

    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, current):
    if member.bot:
        return
    global botVoiceClient
    currentChannel = current.channel
    if currentChannel is not None and botVoiceClient is None:
        try:
            botVoiceClient = await currentChannel.connect(self_deaf=True)
        except Exception as e:
            print(e)
    elif botVoiceClient is not None:
        if len(botVoiceClient.channel.members) == 1:
            await botVoiceClient.disconnect()
            botVoiceClient = None

# adivinar_commands(tree, SERVERS, GOD_USER_ID)

chistes_commands(tree, SERVERS, GOD_USER_ID)

control_commands(bot, GOD_USER_ID)

frases_commands(tree, SERVERS, GOD_USER_ID)

fun_facts_commands(tree, SERVERS, GOD_USER_ID)

info_commands(tree, SERVERS, botVersion, BOT_REPO, initTime)

mascotas_commands(tree, SERVERS, GOD_USER_ID)

oye_commands(bot, GOD_USER_ID)

opiniones_commands(tree, SERVERS, GOD_USER_ID)

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)