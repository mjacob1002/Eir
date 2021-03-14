import numpy as np
import pandas as pd
import math
import src.utility as u

# not to be confused with the person object that is used in the Hub/Strong Infectious Model
from src.utility import Person1 as Person

class RandMove():
    def __init__(self, planeSize, move_r, spread_r, w0, alpha=2.0):
        # size of the plane
        self.planeSize = planeSize
        # mean movement radius
        self.move_r = move_r
        # mean spreading radius
        self.spread_r = spread_r
        # initial probability of infection
        self.w0 = w0
        # constant for the infected equation
        self.alpha = alpha
        # pop size. This will typically be intialized for the subclasses, but make it a number for now
        self.popsize = 100

    # determine whether an infection event has occured
    def _infect(self, inf: Person, sus: Person):
        # get the distance between two points
        r = u.dist(inf, sus)
        # if the distance between two people is greater than the infected person's spreading radius
        if r > inf.R:
            return False
        # compute the probability given that r is within range
        w = self.w0 * (1.0 - (r/inf.r0)**self.alpha)
        # generate a random infection event based on the probability of infection
        inf_event = u.randEvent(w)
        # return the event
        return inf_event

    # eventually do it for every person in each collection array; will be implemented in the sublcasses
    def _move(self):
        # generate the correct number of movement radii
        movement_r = np.random.normal(self.move_R, self.sigma_R, self.popsize)
        # generate the random thetas
        thetas = np.random.uniform(low=0, high=2*math.pi, size=self.popsize)

    # apply this check to every x and y coordinate to make sure they're always within the plane
    def _boundaryCheck(self, coordinate):
        # if the coordinate is too low( below/ to the left of the square plane)
        if coordinate < 0:
            coordinate = 0
        # if the coordinate is too high(above/to the right of the square plane)
        elif coordinate > self.planeSize:
            coordinate = self.planeSize
        return coordinate