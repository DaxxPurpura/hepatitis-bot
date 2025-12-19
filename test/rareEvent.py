from utils.probabilistic_event import ProbabilisticEvent

rare_event = ProbabilisticEvent(1, 5)

for _ in range(10):
    if not rare_event:
        print("no fue un evento raro")
        continue
    print("fue un evento raro")

print("thats all folks")

"""
Ejemplo de uso de utils.probabilistic_event

ProbabilisticEvent(1, 5) genera numeros de 0 a 4 

Cuando se llama a la variable "rare_event" evalua ProbabilisticEvent.occurs
(revisar utils/probabilistic_event.py para más información)
En dado caso que el numero generado sea menor que cero retornará true

Como acepta numeros:
10**6   -> 1 millón
1_000   -> 1 millón
1000000 -> 1 millón
"""