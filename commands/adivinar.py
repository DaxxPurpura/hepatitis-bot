import discord
import time
from utils.choose_random import choose_random
from utils.cooldowns import add_cooldown, get_cooldown
from utils.format_text import load_text, format_text

frases = load_text("/data/frases.txt")
lastFrase = ""
ADIVINAR_COOLDOWN = 30
FORZAR_ADIVINAR_COOLDOWN = 900 # 15 mins

def adivinar_commands(tree, serverList, godUserID):
    @tree.command(name="adivinar", description="Intentá adivinar quién dijo la frase", guilds=serverList)
    async def adivinar(interaction: discord.Interaction):
        userID = interaction.user.id
        global lastFrase
        '''
        if userID != godUserID:
            cooldown = get_cooldown(userID, "adivinar", ADIVINAR_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{time.strftime('%M:%S', time.gmtime(cooldown))} segundos** para volver a usarlo.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            add_cooldown(userID, "adivinar")
        '''
        if not frases:
            embed = discord.Embed(description="### No hay frases cargadas")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        [frase, authors], lastFrase = choose_random(frases, lastFrase)
        embed = discord.Embed(description=f"# ¿Quién dijo esta frase? \n{frase}")
        await interaction.response.send_message(embed=embed)

    @tree.command(name="forzaradivinar", description="Fuerza una frase del museo de frases para adivinar", guilds=serverList)
    async def forzar_adivinar(interaction: discord.Interaction, index: int):
        userID = interaction.user.id
        '''
        if userID != godUserID:
            cooldown = get_cooldown(userID, "forzaradivinar", FORZAR_ADIVINAR_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{time.strftime('%M:%S', time.gmtime(cooldown))} segundos** para volver a usarlo.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            add_cooldown(userID, "forzaradivinar")
        '''
        if not frases:
            embed = discord.Embed(description="### No hay frases cargadas")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
    
        realIndex = index - 1
        if realIndex < 0 or realIndex >= len(frases):
            embed = discord.Embed(description=f"## ¡Ups! \n### Esa frase no existe, tonoto")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
    
        frase, authors = frases[realIndex]
        embed = discord.Embed(description=f"# ¿Quién dijo esta frase? \n{frase}")
        await interaction.response.send_message(embed=embed)