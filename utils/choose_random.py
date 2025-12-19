import random

def choose_random(list, lastChosen = None, canRepeat: bool = False):
    chosen = random.choice(list)
    if canRepeat is False:
        while chosen == lastChosen:
            chosen = random.choice(list)
        lastChosen = chosen
        
        return chosen, lastChosen
    
    return chosen