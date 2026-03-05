import discord

def frase_embed(página, número_página, páginas_totales):
    texto = "\n".join(página)
    embed = discord.Embed(description=texto)
    embed.set_footer(text=f"Página {número_página + 1}/{páginas_totales}")
    return embed