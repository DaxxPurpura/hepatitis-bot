

# Cargar archivos , separar archivos en un mismo mensaje
async def load_attachments(bot, channelID):
    mascotas = []

    channel = await bot.fetch_channel(channelID)

    async for message in channel.history():
        if not message.attachments:
            continue

        for attachment in message.attachments:
            mascotas.append(attachment)
    
    return mascotas