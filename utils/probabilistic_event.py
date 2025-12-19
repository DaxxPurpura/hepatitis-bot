import random

class ProbabilisticEvent:
    def __init__(self, numerator: int, denominator: int):
        if numerator < 0 or denominator <= 0 or numerator > denominator:
            raise ValueError("Invalid probability")
        self.numerator = numerator
        self.denominator = denominator

    def occurs(self) -> bool:
        return random.randrange(self.denominator) < self.numerator

    def __bool__(self):
        return self.occurs()
    

"""
Define la probabilidad de un evento en particular
Por ejemplo, digamos que queremos la probabilidad de 1/4
random.randrange(denominator) genera 0,1,2,3
solo 0 < 1, por lo tanto devuelve TRUE unica 
y exclusivamente en ese caso
"""