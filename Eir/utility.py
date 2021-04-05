import numpy as np
import math

# generates a random event given a probability p
def randEvent(p: float):
    """
    Function to generate random events.
    
    Parameters
    ----------

    p: float
        The probability of a random event occuring.
    
    Returns
    -------

    bool:
        represents whether the event tested happened. True if it, False if it didn't.
    """
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
    """
    Person object used for static spatial models.
    
    Parameters
    ----------

    x: float
        x-coordinate of the Person object
    
    y: float
        y-coordinate of the Person object
    
    ss: bool
        Boolean value determining if the Person is a super spreader.
    
    isIncluded: bool optional
        Determines if the Person object is in the data structure representing a compartment. Default is False.
    """
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
class Person1(Person):
    """
    Person object used for randMovement spatial models.
    
    Parameters
    ----------

    x: float
        x-coordinate of the Person object
    
    y: float
        y-coordinate of the Person object
    
    R: float
        Defaulted to 0 for the randMove models. Usually picked from a distribution.
    
    r0: float
        The spreading radius of the individual Person object. Picked from a normal distribution in the initalization of Model objects.
    
    isIncluded: bool optional
        Determines if the Person object is in the data structure representing a compartment. Default is False.
    """
    # x, y are the randomly generated starting coordinates, 
    # R is the movement distance
    # r is the spreading radius used when calculating infection
    def __init__(self, x, y, R, r0):
        super().__init__(x, y, False)
        # movement radius/ distance
        self.R = R
        # spreading radius/ distance
        self.r0 = r0

#Person object that holds current(x,y) position,  spreading radius, movement radius, 
# and whether they're included in the data structure
class Person2(Person1):
    """
    Person object used for randMovement spatial models.
    
    Parameters
    ----------

    x: float
        x-coordinate of the Person object
    
    y: float
        y-coordinate of the Person object
    
    R: float
        The radius of the circle of the movement of the Person object.
    
    r0: float
        The spreading radius of the individual Person object. Picked from a normal distribution in the initalization of Model objects.
    
    theta: float
        The angle, in radians, that the person is on the circle. Used for calculating the x, y position. 
    
    isIncluded: bool optional
        Determines if the Person object is in the data structure representing a compartment. Default is False.
    
    Attributes
    ----------

    h: float
        x-coordiante of the center of the object's periodic motion.
    
    k: float
        y-coordiante of the center of the object's periodic motion.

    
    """
    # x, y are the randomly generated starting coordinates, 
    # R is the movement distance
    # r is the spreading radius used when calculating infection
    def __init__(self, x, y, R, r0, theta):
        super().__init__(x, y, R, r0)
        # the current theta value
        self.theta =theta
        # h,k is the center of the periodic motion
        self.h = x - self.R * math.cos(self.theta)
        self.k = y - self.R * math.sin(self.theta)

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
def dist(p1: Person, p2: Person):
    """
    Computes the distance between two person objects. 
    
    Parameters
    ----------
    p1: Person
        A person that involved in distance. 
    p2: Person
        A person that involved in distance
    
    Returns
    -------

    float:
        Represents the distance between the two people.
    """
    
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


