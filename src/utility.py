import numpy as np

# generates a random event given a probability p
def randEvent(p: float):
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
# used in Spatial models Strong Infectious and Hub
class Person:
    def __init__(self, x, y, ss, isIncluded = False):
        # x coordinate
        self.x = x
        # y coordinate
        self.y = y
        # super spreader boolean
        self.ss = ss
        # special boolean for the data structure in the Hub/Strong Infectious classes
        self.isIncluded = isIncluded

#Person object that holds current(x,y) position,  spreading radius, movement radius, 
# and whether they're included in the data structure
class Person1:
    # x, y are the randomly generated starting coordinates, 
    # R is the movement distance
    # r is the spreading radius used when calculating infection
    def __init__(self, x, y, R, r0):
        # starting x coordinate
        self.x = x
        # starting y coordinate
        self.y = y
        # movement radius/ distance
        self.R = R
        # spreading radius/ distance
        self.r0 = r0
        # isIncluded
        self.isIncluded = False

def static_prob_help(collect: list, prob: float):
    """
    Used in order to determine who goes from collect state to another using probability prob. 

    Parameters
    ----------

    collect:list
        collect is a list of Person objects. Edits in place because passes a reference.
    
    prob: float
        The probability of a Person object going from one state to another
    """
    transfers = set()
    for i, person in enumerate(collect):
        if not person.isIncluded: 
            continue
        event = randEvent(prob)
        if not event:
            continue
        collect[i].isIncluded=False
        transfers.add(i)
    return transfers

# computes the distance between two different Person objects
def dist(p1: Person, p2: Person) -> float:
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


