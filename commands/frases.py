import discord
import time
from discord import ui
from utils.choose_random import choose_random
from utils.cooldowns import add_cooldown, get_cooldown
from utils.format_text import load_text, format_text, format_frase

frases = load_text("/data/frases.txt")
lastFrase = ""
FRASES_COOLDOWN = 30
FORZAR_FRASES_COOLDOWN = 900 # 15 mins
CANALMUSEODEFRASES = 1429287959303164085

def frases_commands(tree, serverList, godUserID):
    @tree.command(name="frasefunny", description="Invoca una frase del museo de frases", guilds=serverList)
    async def frase_funny(interaction: discord.Interaction):
        userID = interaction.user.id
        global lastFrase
        '''
        if userID != godUserID:
            cooldown = get_cooldown(userID, "frasefunny", FRASES_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{time.strftime('%M:%S', time.gmtime(cooldown))} segundos** para volver a usarlo.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            add_cooldown(userID, "frasefunny")
        '''
        if not frases:
            embed = discord.Embed(description="### No hay frases cargadas")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        [frase, authors], lastFrase = choose_random(frases, lastFrase)
        authors = await format_text(interaction, authors, "user")
        embed = discord.Embed(description=f"{frase} \n### -ㅤ{authors}")
        await interaction.response.send_message(embed=embed)

    @tree.command(name="forzarfrase", description="Fuerza una frase del museo de frases", guilds=serverList)
    async def forzar_frase(interaction: discord.Interaction, index: int):
        userID = interaction.user.id
        '''
        if userID != godUserID:
            cooldown = get_cooldown(userID, "forzarfrase", FORZAR_FRASES_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{time.strftime('%M:%S', time.gmtime(cooldown))} segundos** para volver a usarlo.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            add_cooldown(userID, "forzarfrase")
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
        authors = await format_text(interaction, authors, "user")
        embed = discord.Embed(description=f"{frase} \n### -ㅤ{authors}")
        await interaction.response.send_message(embed=embed)

    @tree.command(name="cargarfrases", description="Actualiza la lista de frases", guilds=serverList)
    async def cargar_frases(interaction: discord.Interaction):
        global frases
        frases = load_text("/data/frases.txt")
        embed = discord.Embed(description="### Se actualizó la lista de frases")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    class FrasePreView(discord.ui.View):
        def __init__(self, oldFrase, oldAuthor, frase, authorsID, authorsDisplay):
            super().__init__(timeout=120)
            self.oldFrase = oldFrase
            self.oldAuthor = oldAuthor
            self.frase = frase
            self.authorsID = authorsID
            self.authorsDisplay = authorsDisplay

        async def on_timeout(self):
            try:
                await self.message.delete()
            except discord.NotFound:
                pass

        @discord.ui.button(label="Editar la frase", style=discord.ButtonStyle.primary)
        async def editar_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_modal(MyModal(self.oldFrase, self.oldAuthor))
            try:
                await self.message.delete()
            except discord.NotFound:
                pass

        @discord.ui.button(label="Enviar al museo", style=discord.ButtonStyle.success)
        async def enviar_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            line_count = 0
            with open("/data/frases.txt", "a+", encoding="utf-8") as file:
                file.write(f"\n{self.frase.replace('\n', '\\n')}={self.authorsID}")
                file.seek(0)
                line_count = sum(1 for line in file)
            
            global frases
            frases = load_text("/data/frases.txt")
            
            canal = interaction.client.get_channel(CANALMUSEODEFRASES)
            embed = discord.Embed(description=f"{self.frase} \n### -ㅤ{self.authorsDisplay}\n\n-# Frase N°{line_count} enviada por {interaction.user.name}")
            await canal.send(embed=embed)
            await interaction.response.send_message("### Frase enviada al museo de frases", ephemeral=True)

            try:
                await self.message.delete()
            except discord.NotFound:
                pass

    class MyModal(ui.Modal):
        def __init__(self, oldFrase : str, oldAuthor : str):
            super().__init__(title="Crear frase")
            self.oldFrase = oldFrase
            self.oldAuthor = oldAuthor

            self.frase = ui.TextInput(
            label="Frase",
            style=discord.TextStyle.paragraph,
            default=self.oldFrase,
            placeholder="\"Esta es una frase\"\n\"Y continúa abajo\"\nEsto no tiene comillas")

            self.fraseExplicación = ui.TextDisplay(content="-# Asegurate de escribir la frase colocando mayúsculas y tildes correctamente.")

            self.authors = ui.TextInput(
            label="Autor",
            style=discord.TextStyle.paragraph,
            default=self.oldAuthor,
            placeholder="{Paulo el frases}{Geoxz_}\n{mhofrio} hablando de yaoi\n{haziel} hablándole a {pande}")

            self.authorExplicación = ui.TextDisplay(content="-# Si querés que la frase muestre automáticamente el apodo actualizado de un usuario, escribí su nombre de Discord o su apodo entre llaves \"{}\".")

            self.add_item(self.frase)
            self.add_item(self.fraseExplicación)
            self.add_item(self.authors)
            self.add_item(self.authorExplicación)

        async def on_submit(self, interaction: discord.Interaction):
            frase, authors, authorsDisplay = await format_frase(interaction, self.frase.value, self.authors.value)
            embed = discord.Embed(title="Preview de la frase", description=f"{frase} \n### -ㅤ{authorsDisplay}\n\n-# Si está bien escrita y no tiene ningún error (POR FAVOR ASEGURATE DE ESO), podés enviarla.")
            view = FrasePreView(self.frase.value, self.authors.value, frase, authors, authorsDisplay)
            await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
            view.message = await interaction.original_response()
    
    @tree.command(name="crearfrase", description="Crea una frase y la envía a museo de frases", guilds=serverList)
    async def crear_frase(interaction: discord.Interaction):
        await interaction.response.send_modal(MyModal("", ""))