import discord
import random
from utils.cooldowns import add_cooldown, get_cooldown
from utils.format_text import load_txt_file

OPINIONES = load_txt_file("opiniones.txt")
OPINIONES_COOLDOWN = 30
FORZAR_OPINIONES_COOLDOWN = 1800 # 30 mins

def opiniones_commands(tree, serverList, godUserID):
    @tree.command(name="queopinas", description="Preguntale a Hepatitis B(ot) que opina acerca de lo que se está hablando", guilds=serverList)
    async def que_opinas(interaction: discord.Interaction):
        userID = interaction.user.id
        if userID != godUserID:
            cooldown = get_cooldown(userID, "queopinas", OPINIONES_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{round(cooldown)} segundos** para volver a usarlo.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            add_cooldown(userID, "queopinas")

        if not OPINIONES:
            embed = discord.Embed(description="### No hay opiniones cargadas")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
    
        opinión = random.choice(OPINIONES)
        embed = discord.Embed(description=f"{opinión}")
        await interaction.response.send_message(embed=embed)

    @tree.command(name="forzarqueopinas", description="Fuerza una opinión de Hepatitis B(ot)", guilds=serverList)
    async def forzar_que_opinas(interaction: discord.Interaction, index: int):
        userID = interaction.user.id
        if userID != godUserID:
            cooldown = get_cooldown(userID, "forzarqueopinas", FORZAR_OPINIONES_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{round(cooldown)} segundos** para volver a usarlo.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            add_cooldown(userID, "forzarqueopinas")

        if not OPINIONES:
            embed = discord.Embed(description="### No hay opiniones cargadas")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
    
        realIndex = index - 1
        if realIndex < 0 or realIndex >= len(OPINIONES):
            embed = discord.Embed(description=f"## ¡Ups! \n### Esa opinión no existe, tonoto")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
    
        opinión = OPINIONES[realIndex]
        embed = discord.Embed(description=f"{opinión}")
        await interaction.response.send_message(embed=embed)