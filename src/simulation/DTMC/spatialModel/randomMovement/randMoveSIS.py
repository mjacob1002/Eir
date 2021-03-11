import numpy as np
import pandas as pd
import src.simulation.utility as u
# not to be confused with the person object that is used in the Hub/Strong Infectious Model
from src.simulation.utility import Person1 as Person
from .randMove import RandMove
import math

class RandMoveSIS(RandMove):

    def __init__(self, S0:int, I0:int, gamma:float, planeSize:float, move_R:float, sigma_R:float, spread_r:float, sigma_r: float,
    days : int, w0=1.0, alpha=2.0):
    # call to super constructor
        super(RandMoveSIS, self).init(planeSize, move_R, spread_r, w0=w0)
        # total population size
        self.popsize = S0 + I0
        # generate the data structure with the arrays
        self.S, self.I = np.zeros(days+1), np.zeros(days+1)
        # initialize day 0 to have the starting susceptibles and infecteds
        self.S[0], self.I[0] = S0, I0
        # generate the special collections that hold the Person objects
        self.Scollect = []
        self.Icollect = []
        spreading_r = np.random.normal(spread_r, sigma_r, S0+I0)
        # generate the random x, y locations
        loc_x = np.random.random(S0+I0) * planeSize
        loc_y = np.random.random(S0+I0) * planeSize
        # create the special objects:
        for i in range(self.popSize):
            # create the person object
            # for this model, the people will move with random radius R each timestep
            # therefore, the R component can be made 0, as that is only relevant for the 
            # periodic mobility model
            p1 = Person(loc_x[i], loc_y[i], 0, spreading_r[i])
            p2 = Person(loc_x[i], loc_y[i], 0, spreading_r[i])        
            # if the person is in the susceptible objects created
            if i < S0:
                p1.isIncluded = True
            else:
                p2.isIncluded = True
            # append them to the data structure
            self.Scollect.append(p1)
            self.Icollect.append(p2)
    # helps _move method with boundary checks
    
    # move people within the planSize x planeSize plane
    def _move(self):
        # generate the correct number of movement radii
        movement_r = np.random.normal(self.move_R, self.sigma_R, self.popsize)
        # generate the random thetas
        thetas = np.random.uniform(low=0, high=2*math.pi, size=self.popsize)
        # looping through everyone and moving them
        for index, person in enumerate(self.Scollect):
            # adjust the x,y coordinate using polar coordinates
            # conduct the boundary check at the same time
            x = self._boundaryCheck(person.x + movement_r[index] * math.cos(thetas[index]))
            y = self._boundaryCheck(person.y + movement_r[index] * math.sin(thetas[index]))
            # change the x, y coordinates
            self.Scollect[index].x, self.Icollect[index] = x, x
            self.Scollect[index].y, self.Icollect[index] = y, y
    
    # deal with transfers from S to I compartments
    def _StoI(self):
        # set containing the indices for transfers
        transfers = set()
        for inf in self.Icollect:
            # if the person isn't infected, check the next person
            if inf.isIncluded == False:
                continue
            for index, sus in enumerate(self.Scollect):
                # if the person isn't in the susceptible bin
                if sus.isIncluded == False:
                    continue
                event = self._infect(inf, sus)
                # if there is a successful infection
                if event:
                    # add the index to the transfer set to be transferred later
                    transfers.add(index)
                    # change the status to be not included in S collection
                    self.Scollect[index].isIncluded = False
        return transfers
    
    def _ItoS(self):
        # set that contains the indices for transfering from I to S
        transfers = set()
        for index, person in enumerate(self.Icollect):
            event = u.randEvent(self.gamma)
            # if the person is recovered
            if event:
                # add to transfer set
                transfers.add(index)
                self.Icollect.isIncluded = False
        return transfers
    
    # run the simulation
    def run(self):
        # for all the days in the simulation
        for i in range(1, self.days+1):
            # run the state changes
            StoI = self._StoI()
            ItoS = self._ItoS()
            # make everyone move randomly
            self._move()
            # change the values in the arrays
            self.S[i] = self.S[i-1] - len(StoI) + len(ItoS)
            self.I[i] = self.I[i-1] + len(StoI) - len(ItoS)

    # switch everything to a dataframe
    def toDataFrame(self):
        # create the linspaced numpy array
        t = np.linspace(0, self.days, self.days + 1)
        # create a 2D array with the days and susceptible and infected arrays
        # do it over axis one so that it creates columns days, susceptible, infected
        arr = np.stack([t, self.S, self.I], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Infected"])
        return df


                

                



            


    





        





