import discord
import time
from utils.choose_random import choose_random
from utils.cooldowns import add_cooldown, get_cooldown
from utils.format_text import load_text, format_text

FRASES = load_text("frases.txt")
lastFrase = ""
FRASES_COOLDOWN = 30
FORZAR_FRASES_COOLDOWN = 900 # 15 mins

def frases_commands(tree, serverList, godUserID):
    @tree.command(name="frasefunny", description="Invoca una frase del museo de frases", guilds=serverList)
    async def frase_funny(interaction: discord.Interaction):
        userID = interaction.user.id
        global lastFrase
    
        if userID != godUserID:
            cooldown = get_cooldown(userID, "frasefunny", FRASES_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{time.strftime('%M:%S', time.gmtime(cooldown))} segundos** para volver a usarlo.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            add_cooldown(userID, "frasefunny")

        if not FRASES:
            embed = discord.Embed(description="### No hay frases cargadas")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        [frase, authors], lastFrase = choose_random(FRASES, lastFrase)
        authors = await format_text(interaction, authors, "user")
        embed = discord.Embed(description=f"{frase} \n### -ㅤ{authors}")
        await interaction.response.send_message(embed=embed)

    @tree.command(name="forzarfrase", description="Fuerza una frase del museo de frases", guilds=serverList)
    async def forzar_frase(interaction: discord.Interaction, index: int):
        userID = interaction.user.id
        if userID != godUserID:
            cooldown = get_cooldown(userID, "forzarfrase", FORZAR_FRASES_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{time.strftime('%M:%S', time.gmtime(cooldown))} segundos** para volver a usarlo.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            add_cooldown(userID, "forzarfrase")

        if not FRASES:
            embed = discord.Embed(description="### No hay frases cargadas")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
    
        realIndex = index - 1
        if realIndex < 0 or realIndex >= len(FRASES):
            embed = discord.Embed(description=f"## ¡Ups! \n### Esa frase no existe, tonoto")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
    
        frase, authors = FRASES[realIndex]
        authors = await format_text(interaction, authors, "user")
        embed = discord.Embed(description=f"{frase} \n### -ㅤ{authors}")
        await interaction.response.send_message(embed=embed)