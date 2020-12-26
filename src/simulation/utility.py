import numpy as np


# generates a random event given a probability p
def randEvent(p: float) -> bool:
    # there is no chance of an event occuring
    if p == 0:
        return False
    else:
        # generate a random number
        x = np.random.rand(1).mean()
        # if the random number falls within a range that represents the probability of an event occuring
        # return True
        if 0 <= x < p:
            return True
        else:
            return False


# Person object that holds whether they are a super spreader or not
# used in Spatial models
class Person:
    def __init__(self, x, y, ss):
        self.x = x
        self.y = y
        self.ss = ss


# computes the distance between two different Person objects
def dist(p1: Person, p2: Person) -> float:
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
