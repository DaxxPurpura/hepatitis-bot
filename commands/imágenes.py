import discord
import time
from utils.choose_random import choose_random
from utils.cooldowns import add_cooldown, get_cooldown
from utils.load_attachments import load_attachments

IMÁGENES = []
lastImagen = 0
IMAGEN_COOLDOWN = 30

# Carga imágenes del canal "museo de imágenes"
async def init_imágenes(bot, canalImágenes):
    global IMÁGENES
    IMÁGENES = await load_attachments(bot, canalImágenes)

def imágenes_commands(tree, serverList, godUserID):
    @tree.command(name="imagen", description="Invoca una imagen del museo de imágenes", guilds=serverList)
    async def imagen(interaction: discord.Interaction):
        userID = interaction.user.id
        global lastImagen

        '''
        if userID != godUserID:
            cooldown = get_cooldown(userID, "imágenes", IMAGEN_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{time.strftime('%M:%S', time.gmtime(cooldown))} segundos** para volver a usarlo.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            add_cooldown(userID, "mascota")
        '''

        if not IMÁGENES:
            embed = discord.Embed(description="### No hay imágenes cargadas")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        imagen, lastImagen = choose_random(IMÁGENES, lastImagen)
        await interaction.response.send_message(imagen.url)

# Actualiza la lista IMÁGENES con imágenes nuevas
def update_imágenes(message, canalImágenes):
    if message.channel.id == canalImágenes and message.attachments:
        for attachment in message.attachments:
            IMÁGENES.append(attachment)