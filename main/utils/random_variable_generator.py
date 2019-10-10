import random
from math import log

class RandomVariableGenerator():
    def __init__(self):
        pass
    
    # Generate "num_to_generate" number of random variables 
    @classmethod
    def generate_inputs(cls, rate, num_to_generate):
        return [cls.generate_input(rate) for _ in range(0, num_to_generate)]

    # Generate input following exponential distribution
    @classmethod
    def generate_input(cls, rate):
        while True:
            u = random.random()
            if u != 0:
                break
        x =  -(1/rate) * log(1-u)
        return x
