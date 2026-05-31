import discord
import time
from utils.choose_random import choose_random
from utils.cooldowns import add_cooldown, get_cooldown
from utils.format_text import load_text, format_text

chistes = load_text("chistes.txt")
CHISTES_COOLDOWN = 30
FORZAR_CHISTES_COOLDOWN = 900 # 15 mins

def chistes_commands(tree, serverList, godUserID):
    @tree.command(name="chiste", description="Invoca un chiste de Hepatitis B(ot)", guilds=serverList)
    async def chiste(interaction: discord.Interaction):
        userID = interaction.user.id

        '''
        if userID != godUserID:
            cooldown = get_cooldown(userID, "chiste", CHISTES_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{time.strftime('%M:%S', time.gmtime(cooldown))} segundos** para volver a usarlo.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            add_cooldown(userID, "chiste")
        '''

        if not chistes:
            embed = discord.Embed(description="### No hay chistes cargados")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
    
        chiste = choose_random(chistes, canRepeat=True)
        # chiste = await format_text(interaction, chiste, "emoji") # QUITAR SI LOS CHISTES NO USAN EMOJIS
        embed = discord.Embed(description=f"{chiste}")
        await interaction.response.send_message(embed=embed)

    @tree.command(name="forzarchiste", description="Fuerza un chiste de Hepatitis B(ot)", guilds=serverList)
    async def forzar_chiste(interaction: discord.Interaction, index: int):
        userID = interaction.user.id
        if userID != godUserID:
            cooldown = get_cooldown(userID, "forzarchiste", FORZAR_CHISTES_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{time.strftime('%M:%S', time.gmtime(cooldown))} segundos** para volver a usarlo.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            add_cooldown(userID, "forzarchiste")

        if not chistes:
            embed = discord.Embed(description="### No hay chistes cargados")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
    
        realIndex = index - 1
        if realIndex < 0 or realIndex >= len(chistes):
            embed = discord.Embed(description=f"## ¡Ups! \n### Ese chiste no existe, tonoto")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
    
        chiste = chistes[realIndex]
        # chiste = await format_text(interaction, chiste, "emoji") # QUITAR SI LOS CHISTES NO USAN EMOJIS
        embed = discord.Embed(description=f"{chiste}")
        await interaction.response.send_message(embed=embed)

    @tree.command(name="cargarchistes", description="Actualiza la lista de chistes", guilds=serverList)
    async def cargar_chistes(interaction: discord.Interaction):
        global chistes
        chistes = load_text("chistes.txt")
        embed = discord.Embed(description="### Se actualizó la lista de chistes")
        await interaction.response.send_message(embed=embed, ephemeral=True)