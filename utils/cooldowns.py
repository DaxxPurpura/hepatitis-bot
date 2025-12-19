import time

cooldowns = {
    "frasefunny": {},
    "forzarfrase": {},
    "mascota": {},
    "queopinas": {},
    "forzarqueopinas": {},
    "funfact": {},
    "forzarfunfact": {},
    "mensaje": {},
    "reaccion": {},
    "noreaccion": {},
    "oye": {}
}

# Añadir cooldown a userID
def add_cooldown(userID, command: str):
    cooldowns[command][userID] = time.time()

# Obtener el tiempo restante del cooldown de UserID
def get_cooldown(userID, command: str, amount: int):
    if userID not in cooldowns[command]:
        return 0
    return amount - (time.time() - cooldowns[command][userID])

# Quitar cooldown a userID
def remove_cooldown(userID, command: str):
    cooldowns[command].pop(userID, None)