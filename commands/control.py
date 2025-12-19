import discord
import time
from utils.cooldowns import add_cooldown, get_cooldown

MENSAJE_COOLDOWN = 1200 # 20 mins
REACCION_COOLDOWN = 900 # 15 mins
NOREACCION_COOLDOWN = 900 # 15 mins

def control_commands(bot, godUserID):
    @bot.command()
    async def mensaje(context):
        ogMessage = context.message
        userID = context.author.id
        await ogMessage.delete()

        if userID != godUserID:
            cooldown = get_cooldown(userID, "mensaje", MENSAJE_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{time.strftime('%M:%S', time.gmtime(cooldown))} segundos** para volver a usarlo.")
                await context.send(embed=embed, delete_after=3)
                return
            add_cooldown(userID, "mensaje")
        actualMessage = ogMessage.content.replace("/mensaje ", "", 1)
        if ogMessage.reference is None:
            await context.send(actualMessage)
            return
        uffReferencia = ogMessage.reference
        replyMessage = await context.channel.fetch_message(uffReferencia.message_id)
        await replyMessage.reply(actualMessage)
        
    @bot.command()
    async def reaccion(context):
        ogMessage = context.message
        userID = context.author.id
        await ogMessage.delete()

        if ogMessage.reference is not None:
            if userID != godUserID:
                cooldown = get_cooldown(userID, "reaccion", REACCION_COOLDOWN)
                if cooldown > 0:
                    embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{time.strftime('%M:%S', time.gmtime(cooldown))} segundos** para volver a usarlo.")
                    await context.send(embed=embed, delete_after=3)
                    return
                add_cooldown(userID, "reaccion")
            actualMessage = ogMessage.content.replace("/reaccion ", "", 1)
            if not actualMessage:
                embed = discord.Embed(description=f"### Necesitás elegir un emoji para usar /reaccion.")
                await context.send(embed=embed, delete_after=3)
                return
            uffReferencia = ogMessage.reference
            reactMessage = await context.channel.fetch_message(uffReferencia.message_id)
            await reactMessage.add_reaction(actualMessage)
        else:
            embed = discord.Embed(description=f"### Necesitás responder a un mensaje para usar /reaccion.")
            await context.send(embed=embed, delete_after=3)

    @bot.command()
    async def noreaccion(context):
        ogMessage = context.message
        userID = context.author.id
        await ogMessage.delete()

        if ogMessage.reference is not None:
            if userID != godUserID:
                cooldown = get_cooldown(userID, "noreaccion", NOREACCION_COOLDOWN)
                if cooldown > 0:
                    embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{time.strftime('%M:%S', time.gmtime(cooldown))} segundos** para volver a usarlo.")
                    await context.send(embed=embed, delete_after=3)
                    return
                add_cooldown(userID, "noreaccion")
            actualMessage = ogMessage.content.replace("/noreaccion ", "", 1)
            if not actualMessage:
                embed = discord.Embed(description=f"### Necesitás elegir un emoji para usar /noreaccion.")
                await context.send(embed=embed, delete_after=3)
                return
            uffReferencia = ogMessage.reference
            reactMessage = await context.channel.fetch_message(uffReferencia.message_id)
            await reactMessage.remove_reaction(actualMessage, bot.user)
        else:
            embed = discord.Embed(description=f"### Necesitás responder a un mensaje para usar /noreaccion.")
            await context.send(embed=embed, delete_after=3)
        