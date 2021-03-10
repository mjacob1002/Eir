from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from utility import Person
import utility as u
import multiprocessing as mp


class Spatial:
    def __init__(self, popsize: int, pss: float, rstart: float, alpha: int, side: float, S0: int, I0: int, days: int, w0=1.0):
        # the total size of the closed population
        self.popsize = popsize
        # the probability that a person is a super spreader
        self.pss = pss
        # the starting spreading radius of an infectious perosn
        self.rstart = rstart
        # the normal probability constant that is used in Fujie & Odagaki paper infect function
        self.alpha = alpha
        # one side of the plane of the simulation
        self.side = side
        # initial susceptibles, initial infecteds
        self.S0, self.I0 = S0, I0
        # make the data structure that makes it easy to look up different things rather than using sets
        self.Scollect, self.Icollect = [], []
        # initialize the starting probability when 0 units from infectious person
        self.w0 = w0
        # number of days
        self.days = days
        # create the arrays storing the number of people in each state on each day
        self.S, self.I = np.zeros(days+1), np.zeros(days+1)
        # initialize for day 0
        self.S[0], self.I[0] = S0, I0
        # create an array of correspond x and y coordinates for popsize number of people
        # the infected person will be at locx[0] and locy[0]
        self.locx = np.random.rand(popsize) * side
        self.locy = np.random.rand(popsize) * side



    # will be inherited from Hub and Strong Infectious classes and implemented there
    def _infect(self, inf: Person, sus: Person):
        pass

    def _statechange(self):
        pass
