import discord
import time
from utils.choose_random import choose_random
from utils.cooldowns import add_cooldown, get_cooldown
from utils.format_text import load_text
from utils.probabilistic_event import ProbabilisticEvent

chistes = load_text("/data/chistes.txt")
lastChiste = ""
CHISTES_COOLDOWN = 30
FORZAR_CHISTES_COOLDOWN = 900 # 15 mins

def chistes_commands(tree, serverList, godUserID):
    @tree.command(name="chiste", description="Invoca un chiste de Hepatitis B(ot)", guilds=serverList)
    async def chiste(interaction: discord.Interaction):
        userID = interaction.user.id
        global lastChiste
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
    
        chiste, lastChiste = choose_random(chistes, lastChiste)
        rare_event = ProbabilisticEvent(1, 100)
        if rare_event:
            chiste = "## ¡El chiste del pan que habla!\n### Era un día como cualquier otro en un pequeño pueblo llamado Aburrilandia, donde todas las personas vivían aburridas: los niños no hacían más que ir al colegio, volver a sus casas, comer e irse a dormir todos los días, y los adultos iban a trabajar, volvían a sus casas, comían, se preguntaban si siquiera valía la pena seguir viviendo una vida así de aburrida y, por último, se dormían.\n\n### En ese pueblo vivía un niño llamado Enrique. Él llegó al colegio y se encontró con su amigo Anacleto, que le dijo:\n\n### \"Hola Enrique, ¿cómo estás?\"\n\n### A lo que Enrique respondió:\n\n### \"Como siempre, ¿no tenés algo nuevo que contar?\"\n\n### \"No\", respondió Anacleto.\n\n### Todas las conversaciones eran así: monótonas, sin vida y siempre desinteresadas. Porque, aunque preguntasen si algo nuevo e interesante había pasado, todos sabían la respuesta. Nunca pasaba nada nuevo.\n\n### Terminó la clase y Enrique volvía caminando a su casa en medio del cielo gris, el sol tapado por nubes, cuando vio a una persona colocando un cartel en una pared. Pero Enrique estaba bastante cansado y aburrido como para importarle, así que siguió su camino.\n\n### Al día siguiente, Enrique hizo el mismo recorrido de todos los días hacia su colegio, pero esta vez el cartel llamó su atención: estaba lleno de colores y dibujos llamativos y anunciaba que un circo estaba por llegar a Aburrilandia… ¡y que tendría la participación especial del pan que habla!\n\n### En ese momento, Enrique sintió felicidad verdadera por primera vez en su vida. El cielo comenzó a despejarse y, por fin, pudo ver la luz del sol. Al llegar al colegio, Enrique esparció esa información por toda la escuela. Algunos le creyeron y parecían personas completamente diferentes, mientras que otros no podían creer que algo así llegara a Aburrilandia:\n\n### \"¿El pan que habla? Este pueblo es muy aburrido como para que pase algo así\", decían.\n\n### Sin embargo, al terminar la clase, todos vieron los carteles y quedaron impresionados:\n\n### \"¡No lo puedo creer! ¡El pan que habla realmente vendrá hasta aquí!\"\n\n### Todos se habían vuelto locos al escuchar tal cosa. Los adultos dejaron de pensar en la importancia de sus vidas y simplemente esperaban con anhelo ese día en que, por fin, el pan que habla llegase a Aburrilandia, al igual que los niños."
            embed = discord.Embed(description=f"{chiste}")
            await interaction.response.send_message(embed=embed)
            chiste = "### Pasó una semana, dos semanas, tres semanas, un mes… hasta que, por fin, el circo había llegado a Aburrilandia. Pero más importante aún: ¡el pan que habla!\n\n### Una cola gigante empezó a formarse en la entrada del circo. ¡Todo el pueblo estaba ahí! Poco a poco, la gente empezó a entrar hasta que no quedó nadie fuera. Por fin había comenzado el espectáculo.\n\n### Se abrió el telón y apareció un malabarista en el escenario. Hacía trucos muy difíciles e impresionantes, pero al público no le pareció la gran cosa.\n\n### Se cerró el telón y, cuando volvió a abrirse, apareció un payaso que hacía formas con globos y contaba chistes muy buenos, pero el silencio nunca fue tan ensordecedor. Nadie se reía.\n\n### Se cerró el telón y al abrirse apareció uno de los mejores magos de todos los tiempos. Como era de esperarse, hizo los trucos de magia más impresionantes e imposibles que uno se hubiese podido imaginar, pero no recibió ni una reacción del público.\n\n### El telón se cerró nuevamente, pero esta vez una voz anunció:\n\n### \"¡Damas y caballeros! ¡Niños y niñas! Tengo el honor de comunicarles… que está aquí con ustedes... ¡el pan que habla!\"\n\n### En ese momento, todos se pusieron de pie y empezaron a aplaudir. Ese era el momento que todos, literalmente todos, habían estado esperando durante un mes entero. Finalmente, el telón se abrió.\n\n### Ahí estaba, el pan que habla, sentado en una silla con un foco iluminándolo.\n\n### Las chicas empezaron a gritar, los chicos empezaron a llorar, todos estaban tan emocionados esperando a que el pan que habla diera su show.\n\n### De repente, un chico subió al escenario con un balde de agua en la mano, agarró al pan que habla y lo sumergió en el balde.\n\n### Todo el público gritó al mismo tiempo y comenzaron a decirle todo tipo de barbaridades al chico:\n\n### \"¿¡Qué estás haciendo!?\"\n\n### \"¡Lo estás matando!\"\n\n### \"¡Asesino!\"\n\n### \"¡Llévenlo a la cárcel!\"\n\n### A lo que el chico, confundido, respondió:\n\n### \"¿Eh? Pero si el pan que habla está dando su espectáculo.\"\n\n### Todo el público quedó igual de confundido que él.\n\n### \"¿Cómo que está dando su espectáculo?\"\n\n### Y el chico respondió:\n\n### \"Bueno, ahora que lo mojé… el pan está blando.\""
            embed = discord.Embed(description=f"{chiste}")
            await interaction.channel.send(embed=embed)
            return
        embed = discord.Embed(description=f"{chiste}")
        await interaction.response.send_message(embed=embed)

    @tree.command(name="forzarchiste", description="Fuerza un chiste de Hepatitis B(ot)", guilds=serverList)
    async def forzar_chiste(interaction: discord.Interaction, index: int):
        userID = interaction.user.id
        '''
        if userID != godUserID:
            cooldown = get_cooldown(userID, "forzarchiste", FORZAR_CHISTES_COOLDOWN)
            if cooldown > 0:
                embed = discord.Embed(description=f"# Este comando está en cooldown \n### Esperá **{time.strftime('%M:%S', time.gmtime(cooldown))} segundos** para volver a usarlo.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            add_cooldown(userID, "forzarchiste")
        '''
        if not chistes:
            embed = discord.Embed(description="### No hay chistes cargados")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
    
        realIndex = index - 1
        if realIndex == -1:
            embed = discord.Embed(description=f"## ¡El chiste del pan que habla!\n### Era un día como cualquier otro en un pequeño pueblo llamado Aburrilandia, donde todas las personas vivían aburridas: los niños no hacían más que ir al colegio, volver a sus casas, comer e irse a dormir todos los días, y los adultos iban a trabajar, volvían a sus casas, comían, se preguntaban si siquiera valía la pena seguir viviendo una vida así de aburrida y, por último, se dormían.\n\n### En ese pueblo vivía un niño llamado Enrique. Él llegó al colegio y se encontró con su amigo Anacleto, que le dijo:\n\n### \"Hola Enrique, ¿cómo estás?\"\n\n### A lo que Enrique respondió:\n\n### \"Como siempre, ¿no tenés algo nuevo que contar?\"\n\n### \"No\", respondió Anacleto.\n\n### Todas las conversaciones eran así: monótonas, sin vida y siempre desinteresadas. Porque, aunque preguntasen si algo nuevo e interesante había pasado, todos sabían la respuesta. Nunca pasaba nada nuevo.\n\n### Terminó la clase y Enrique volvía caminando a su casa en medio del cielo gris, el sol tapado por nubes, cuando vio a una persona colocando un cartel en una pared. Pero Enrique estaba bastante cansado y aburrido como para importarle, así que siguió su camino.\n\n### Al día siguiente, Enrique hizo el mismo recorrido de todos los días hacia su colegio, pero esta vez el cartel llamó su atención: estaba lleno de colores y dibujos llamativos y anunciaba que un circo estaba por llegar a Aburrilandia… ¡y que tendría la participación especial del pan que habla!\n\n### En ese momento, Enrique sintió felicidad verdadera por primera vez en su vida. El cielo comenzó a despejarse y, por fin, pudo ver la luz del sol. Al llegar al colegio, Enrique esparció esa información por toda la escuela. Algunos le creyeron y parecían personas completamente diferentes, mientras que otros no podían creer que algo así llegara a Aburrilandia:\n\n### \"¿El pan que habla? Este pueblo es muy aburrido como para que pase algo así\", decían.\n\n### Sin embargo, al terminar la clase, todos vieron los carteles y quedaron impresionados:\n\n### \"¡No lo puedo creer! ¡El pan que habla realmente vendrá hasta aquí!\"\n\n### Todos se habían vuelto locos al escuchar tal cosa. Los adultos dejaron de pensar en la importancia de sus vidas y simplemente esperaban con anhelo ese día en que, por fin, el pan que habla llegase a Aburrilandia, al igual que los niños.")
            await interaction.response.send_message(embed=embed)
            embed = discord.Embed(description=f"### Pasó una semana, dos semanas, tres semanas, un mes… hasta que, por fin, el circo había llegado a Aburrilandia. Pero más importante aún: ¡el pan que habla!\n\n### Una cola gigante empezó a formarse en la entrada del circo. ¡Todo el pueblo estaba ahí! Poco a poco, la gente empezó a entrar hasta que no quedó nadie fuera. Por fin había comenzado el espectáculo.\n\n### Se abrió el telón y apareció un malabarista en el escenario. Hacía trucos muy difíciles e impresionantes, pero al público no le pareció la gran cosa.\n\n### Se cerró el telón y, cuando volvió a abrirse, apareció un payaso que hacía formas con globos y contaba chistes muy buenos, pero el silencio nunca fue tan ensordecedor. Nadie se reía.\n\n### Se cerró el telón y al abrirse apareció uno de los mejores magos de todos los tiempos. Como era de esperarse, hizo los trucos de magia más impresionantes e imposibles que uno se hubiese podido imaginar, pero no recibió ni una reacción del público.\n\n### El telón se cerró nuevamente, pero esta vez una voz anunció:\n\n### \"¡Damas y caballeros! ¡Niños y niñas! Tengo el honor de comunicarles… que está aquí con ustedes... ¡el pan que habla!\"\n\n### En ese momento, todos se pusieron de pie y empezaron a aplaudir. Ese era el momento que todos, literalmente todos, habían estado esperando durante un mes entero. Finalmente, el telón se abrió.\n\n### Ahí estaba, el pan que habla, sentado en una silla con un foco iluminándolo.\n\n### Las chicas empezaron a gritar, los chicos empezaron a llorar, todos estaban tan emocionados esperando a que el pan que habla diera su show.\n\n### De repente, un chico subió al escenario con un balde de agua en la mano, agarró al pan que habla y lo sumergió en el balde.\n\n### Todo el público gritó al mismo tiempo y comenzaron a decirle todo tipo de barbaridades al chico:\n\n### \"¿¡Qué estás haciendo!?\"\n\n### \"¡Lo estás matando!\"\n\n### \"¡Asesino!\"\n\n### \"¡Llévenlo a la cárcel!\"\n\n### A lo que el chico, confundido, respondió:\n\n### \"¿Eh? Pero si el pan que habla está dando su espectáculo.\"\n\n### Todo el público quedó igual de confundido que él.\n\n### \"¿Cómo que está dando su espectáculo?\"\n\n### Y el chico respondió:\n\n### \"Bueno, ahora que lo mojé… el pan está blando.\"")
            await interaction.channel.send(embed=embed)
            return
        if realIndex < 0 or realIndex >= len(chistes):
            embed = discord.Embed(description=f"## ¡Ups! \n### Ese chiste no existe, tonoto")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
    
        chiste = chistes[realIndex]
        embed = discord.Embed(description=f"{chiste}")
        await interaction.response.send_message(embed=embed)

    @tree.command(name="cargarchistes", description="Actualiza la lista de chistes", guilds=serverList)
    async def cargar_chistes(interaction: discord.Interaction):
        global chistes
        chistes = load_text("/data/chistes.txt")
        embed = discord.Embed(description="### Se actualizó la lista de chistes")
        await interaction.response.send_message(embed=embed, ephemeral=True)