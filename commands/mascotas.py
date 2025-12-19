import discord
import time
from utils.choose_random import choose_random
from utils.cooldowns import add_cooldown, get_cooldown
from utils.load_attachments import load_attachments

MASCOTAS = []
lastMascota = 0
MASCOTA_COOLDOWN = 30

# Carga imagenes del canal "mascotas"
async def init_mascotas(bot, canalMascotas):
    global MASCOTAS
    MASCOTAS = await load_attachments(bot, canalMascotas)

def mascotas_commands(tree, serverList, godUserID):
    @tree.command(name="mascota", description="Invoca una mascota de mascotas", guilds=serverList)
    async def mascota(interaction: discord.Interaction):
        userID = interaction.user.id
        global lastMascota

        '''
        if userID != godUserID:
            cooldown = get_cooldown(userID, "mascota", MASCOTA_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{time.strftime('%M:%S', time.gmtime(cooldown))} segundos** para volver a usarlo.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            add_cooldown(userID, "mascota")
        '''

        if not MASCOTAS:
            embed = discord.Embed(description="### No hay mascotas cargadas")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        mascota, lastMascota = choose_random(MASCOTAS, lastMascota)
        await interaction.response.send_message(mascota.url)

# Actualiza la lista MASCOTAS con imagenes nuevas
def update_mascotas(message, canalMascotas):
    if message.channel.id == canalMascotas and message.attachments:
        for attachment in message.attachments:
            MASCOTAS.append(attachment)