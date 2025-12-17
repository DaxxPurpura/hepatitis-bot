import discord
import random
from utils.cooldowns import add_cooldown, get_cooldown, remove_cooldown
from utils.format_text import load_txt_file, separate_authors

FRASES = load_txt_file("frases.txt")
lastFrase = ""
FRASES_COOLDOWN = 30
FORZAR_FRASES_COOLDOWN = 1800 # 30 mins

def frases_commands(tree, serverList, godUserID):
    @tree.command(name="frasefunny", description="Invoca una frase del museo de frases", guilds=serverList)
    async def frase_funny(interaction: discord.Interaction):
        userID = interaction.user.id
        global lastFrase
    
        if userID != godUserID:
            cooldown = get_cooldown(userID, "frasefunny", FRASES_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{round(cooldown)} segundos** para volver a usarlo.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            add_cooldown(userID, "frasefunny")

        if not FRASES:
            embed = discord.Embed(description="### No hay frases cargadas")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
    
        frase, authorsRaw = random.choice(FRASES)
        while frase == lastFrase:
            frase, authorsRaw = random.choice(FRASES)
        lastFrase = frase

        authors = await separate_authors(interaction, authorsRaw)
        embed = discord.Embed(description=f"{frase} \n### -ㅤ{authors}")
        await interaction.response.send_message(embed=embed)

    @tree.command(name="forzarfrase", description="Fuerza una frase del museo de frases", guilds=serverList)
    async def forzar_frase(interaction: discord.Interaction, index: int):
        userID = interaction.user.id
        if userID != godUserID:
            cooldown = get_cooldown(userID, "forzarfrase", FORZAR_FRASES_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{round(cooldown)} segundos** para volver a usarlo.")
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
    
        frase, authorsRaw = FRASES[realIndex]
        authors = await separate_authors(interaction, authorsRaw)
        embed = discord.Embed(description=f"{frase} \n### -ㅤ{authors}")
        await interaction.response.send_message(embed=embed)