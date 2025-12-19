import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import os
from commands.control import control_commands
from commands.frases import frases_commands
from commands.fun_fact import fun_facts_commands
from commands.info import info_commands
from commands.mascotas import init_mascotas, mascotas_commands, update_mascotas
from commands.oye import oye_commands, detect_victims
from commands.que_opinas import opiniones_commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN') # Agregá la token de tu bot al .env
serverID = os.getenv('TEST_SERVER') # Agregá la ID de tu server al .env
godUserID = int(os.getenv('GOD_USER')) # Agregá tu ID de usuario al .env

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents)
tree = bot.tree

BOT_VERSION = "1.4.0"
BOT_REPO = "https://github.com/DaxxPurpura/hepatitis-bot"
botVoiceChat = None

# Servers autorizados
HEPATITIS = discord.Object(id=1018626508853629149)
TEST = discord.Object(id=serverID)

CANALMASCOTAS = 1442192026962759795

# Sincronizar servers
@bot.event
async def on_ready():
    await tree.sync(guild=HEPATITIS)
    await tree.sync(guild=TEST)

    await init_mascotas(bot, CANALMASCOTAS)

@bot.event
async def on_message(message):
    update_mascotas(message, CANALMASCOTAS)

    await detect_victims(message, bot)
    
    await bot.process_commands(message)

# código inútil al parecer
@bot.event
async def on_voice_state_update(member, before, current):
    currentChannel = current.channel
    global botVoiceChat
    if currentChannel != None and botVoiceChat == None:
        botVoiceChat = await currentChannel.connect(self_deaf=True)
    elif len(currentChannel.members) <= 1:
        await botVoiceChat.disconect()
        botVoiceChat = None

control_commands(bot, godUserID)

frases_commands(tree, [HEPATITIS, TEST], godUserID)

fun_facts_commands(tree, [HEPATITIS, TEST], godUserID)

info_commands(tree, [HEPATITIS, TEST], BOT_VERSION, BOT_REPO)

mascotas_commands(tree, [HEPATITIS, TEST], godUserID)

oye_commands(bot, godUserID)

opiniones_commands(tree, [HEPATITIS, TEST], godUserID)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)