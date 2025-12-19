import discord
import time
from utils.cooldowns import add_cooldown, get_cooldown

OYE_COOLDOWN = 900 # 15 mins
channelOye = {}

def oye_commands(bot, godUserID):
    @bot.command()
    async def oye(context):
        ogMessage = context.message
        userID = context.author.id
        await ogMessage.delete()

        if channelOye.get(context.channel) is not None:
            embed = discord.Embed(description=f"### Alguien ya usó ese comando en este canal.")
            await context.send(embed=embed, delete_after=2)
            return

        if userID != godUserID:
            cooldown = get_cooldown(userID, "oye", OYE_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{time.strftime('%M:%S', time.gmtime(cooldown))} segundos** para volver a usarlo.")
                await context.send(embed=embed, delete_after=3)
                return
            add_cooldown(userID, "oye")
        if ogMessage.reference is None:
            channelOye[context.channel] = "all"
            await ogMessage.channel.send("Oye")
            return
        uffReferencia = ogMessage.reference
        replyMessage = await context.channel.fetch_message(uffReferencia.message_id)
        channelOye[context.channel] = replyMessage.author
        await replyMessage.reply("Oye")

async def detect_victims(message, bot):
    if channelOye.get(message.channel) is None:
        return
    
    if message.author == bot.user:
        return
    
    if channelOye[message.channel] == "all":
        await message.reply("No nada.")
        channelOye[message.channel] = None
    elif channelOye[message.channel] == message.author:
        await message.reply("No nada.")
        channelOye[message.channel] = None