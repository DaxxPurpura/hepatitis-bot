import discord
from utils.cooldowns import add_cooldown, get_cooldown

MENSAJE_COOLDOWN = 1800 # 30 mins
MENSAJE_COOLDOWN_GLOBAL = 900 # 15 mins
REACCION_COOLDOWN = 1200 # 20 mins
REACCION_COOLDOWN_GLOBAL = 600 # 10 mins
NOREACCION_COOLDOWN = 1200 # 20 mins
NOREACCION_COOLDOWN_GLOBAL = 600 # 10 mins

async def control_commands(message, bot, godUserID):
    userID = message.author.id
    if "/mensaje" in message.content:
        await message.delete()
        if userID != godUserID:
            cooldown = get_cooldown(userID, "mensaje", MENSAJE_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{round(cooldown)} segundos** para volver a usarlo.")
                await message.channel.send(embed=embed, delete_after=3)
                return
            add_cooldown(userID, "mensaje")
        actualMessage = message.content.replace("/mensaje", "")
        if message.reference is None:
            await message.channel.send(actualMessage)
            return
        uffReferencia = message.reference
        channel = bot.get_channel(uffReferencia.channel_id)
        replyMessage = await channel.fetch_message(uffReferencia.message_id)
        await replyMessage.reply(actualMessage)

    elif "/reaccion" in message.content:
        await message.delete()
        if userID != godUserID:
            cooldown = get_cooldown(userID, "reaccion", REACCION_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{round(cooldown)} segundos** para volver a usarlo.")
                await message.channel.send(embed=embed, delete_after=3)
                return
            add_cooldown(userID, "reaccion")
        actualMessage = message.content.replace("/reaccion ", "")
        if message.reference is not None:
            uffReferencia = message.reference
            channel = bot.get_channel(uffReferencia.channel_id)
            reactMessage = await channel.fetch_message(uffReferencia.message_id)
            await reactMessage.add_reaction(actualMessage)

    elif "/noreaccion" in message.content:
        await message.delete()
        if userID != godUserID:
            cooldown = get_cooldown(userID, "noreaccion", NOREACCION_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{round(cooldown)} segundos** para volver a usarlo.")
                await message.channel.send(embed=embed, delete_after=3)
                return
            add_cooldown(userID, "noreaccion")
        actualMessage = message.content.replace("/noreaccion ", "")
        if message.reference is not None:
            uffReferencia = message.reference
            channel = bot.get_channel(uffReferencia.channel_id)
            reactMessage = await channel.fetch_message(uffReferencia.message_id)
            await reactMessage.remove_reaction(actualMessage, bot.user)