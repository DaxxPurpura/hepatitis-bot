import discord
import random
import time
from utils.choose_random import choose_random
from utils.cooldowns import add_cooldown, get_cooldown
from utils.format_text import load_text
from utils.probabilistic_event import ProbabilisticEvent

FUN_FACTS = load_text("fun_facts.txt")
lastFunFact = ""
FUN_FACTS_COOLDOWN = 30
FORZAR_FUN_FACTS_COOLDOWN = 900 # 15 mins

def fun_facts_commands(tree, serverList, godUserID):
    @tree.command(name="funfact", description="Invoca un facto jijoso de Hepatitis B(ot)", guilds=serverList)
    async def fun_fact(interaction: discord.Interaction):
        userID = interaction.user.id
        global lastFunFact

        '''
        if userID != godUserID:
            cooldown = get_cooldown(userID, "funfact", FUN_FACTS_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{time.strftime('%M:%S', time.gmtime(cooldown))} segundos** para volver a usarlo.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            add_cooldown(userID, "funfact")
        '''

        if not FUN_FACTS:
            embed = discord.Embed(description="### No hay fun facts cargados")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        funFact, lastFunFact = choose_random(FUN_FACTS, lastFunFact)
        rare_event = ProbabilisticEvent(1, 10**6)
        if rare_event:
            funFact = "## Sabías que... \n### este mensaje tiene solo un 0.000001% de probabilidad de aparecer."
        embed = discord.Embed(description=f"{funFact}")
        await interaction.response.send_message(embed=embed)

    @tree.command(name="forzarfunfact", description="Fuerza un facto jijoso de Hepatitis B(ot)", guilds=serverList)
    async def forzar_fun_fact(interaction: discord.Interaction, index: int):
        userID = interaction.user.id
        if userID != godUserID:
            cooldown = get_cooldown(userID, "forzarfunfact", FORZAR_FUN_FACTS_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{time.strftime('%M:%S', time.gmtime(cooldown))} segundos** para volver a usarlo.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            add_cooldown(userID, "forzarfunfact")

        if not FUN_FACTS:
            embed = discord.Embed(description="### No hay fun facts cargados")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
    
        realIndex = index - 1
        if realIndex == -1:
            embed = discord.Embed(description=f"## Sabías que... \n### este mensaje tiene solo un 0.000001% de probabilidad de aparecer.")
            await interaction.response.send_message(embed=embed)
            return
        elif realIndex < 0 or realIndex >= len(FUN_FACTS):
            embed = discord.Embed(description=f"## ¡Ups! \n### Ese fun fact no existe, tonoto")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
    
        funFact = FUN_FACTS[realIndex]
        embed = discord.Embed(description=f"{funFact}")
        await interaction.response.send_message(embed=embed)