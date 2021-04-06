import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from math import cos, sin, pi

from ..randomMovement.randMoveSEIRSDV import RandMoveSEIRSDV
from Eir.utility import Person2 as Person
from Eir.utility import randEvent, dist
from Eir.DTMC.spatialModel.simul_details import Simul_Details

class PeriodicSEIRSDV(RandMoveSEIRSDV):

    def __init__(self, S0:int, E0:int, I0:int, R0:int, V0: int, rho: float, gamma: float, mu: float, eta:float, kappa: float, planeSize: float, move_r: float, sigma_R: float, 
        spread_r: float, sigma_r: float, days:int, w0=1.0, alpha=2.0, timeDelay=-1, k=5, std=pi/2):
        self.floatCheck(k, std)
        self.negValCheck(k, std)
        
        super().__init__(S0=S0, E0=E0, I0=I0, R0=R0, V0=V0, rho=rho, gamma=gamma, mu=mu, eta=eta, kappa=kappa, planeSize=planeSize, move_r=move_r, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r, days=days, w0=w0, alpha=alpha, timeDelay=timeDelay)

        self.k, self.std = k, std

        # create data structures
        self.Scollect, self.Ecollect, self.Icollect, self.Rcollect, self.Vcollect, self.Dcollect = [], [], [], [], [], []
        loc_x, loc_y, spreading_r, mvnt_r = np.random.random(self.popsize)*planeSize, np.random.random(self.popsize)*planeSize, np.random.normal(spread_r, sigma_r, self.popsize), np.random.normal(2*pi/k, std, self.popsize)
        # create the Simul_Details object
        self.details = Simul_Details(days=self.days, popsize=self.popsize)
        # generation of population
        for i in range(self.popsize):
            theta = np.random.normal(2*pi/k, std)
            persons = []
            for j in range(6):
                persons.append(Person(loc_x[i], loc_y[i], mvnt_r[i], spreading_r[i], theta=theta))
            if i < S0:
                persons[0].isIncluded=True
                self.details.addStateChange(i, "S", 0)
            elif i< S0 + E0:
                persons[1].isIncluded=True
                self.details.addStateChange(i, "E", 0)
            elif i< S0 + E0 + I0:
                persons[2].isIncluded=True
                self.details.addStateChange(i, "I", 0)
            elif i< S0 + E0 + I0 + R0:
                persons[3].isIncluded=True
                self.details.addStateChange(i, "R", 0)
            else:
                persons[4].isIncluded=True
                self.details.addStateChange(i, "V", 0)
            # add generated people to the data structure
            self.Scollect.append(persons[0])
            self.Ecollect.append(persons[1])
            self.Icollect.append(persons[2])
            self.Rcollect.append(persons[3])
            self.Vcollect.append(persons[4])
            self.Dcollect.append(persons[5])
            # add the location to day 0 of every person
            self.details.addLocation(0, (persons[0].x, persons[0].y))
    
    # eventually do it for every person in each collection array; will be implemented in the sublcasses
    def _move(self, day: int, collects: list):
        """
        Responsible for moving the locations of each Person in the simulation. Does it in place.

        Parameters
        ----------
        day: int
            The current day that the move is taking place on. Is important for the Simul_Details() object in order to keep track of the movement patterns each day.
        
        collect: list
            Contains all of the collection data structures that will be cycled through for the moves. This allows for easy object-oriented design.
        """
        # generate the random thetas from a normal distribution
        thetas = np.random.normal(2*pi/self.k, self.std, self.popsize)

        for index, person in enumerate(collects[0]):
            # adjust the theta current theta values in the object
            collects[0][index].theta += thetas[index]
            # adjust the x,y coordinate using polar coordinates
            # conduct the boundary check at the same time
            x = self._boundaryCheck(person.h + person.R * cos(collects[0][index].theta))
            y = self._boundaryCheck(person.k + person.R * sin(collects[0][index].theta))
            # add the new location to the Simul_Details object
            self.details.addLocation(day, (x,y))
            # change the x, y coordinates of every copy of person index in the other collections
            for j, collect in enumerate(collects):
                collects[j][index].x = x
                collects[j][index].y = y
                collects[j][index].theta += thetas[index]
    
    def plot(self):
        t = np.linspace(0,self.days, self.days+1)
        fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(nrows=6, sharex="all")
        ax1.set_title("Periodic Movement SEIRSDV")
        ax6.set_xlabel("Days")
        ax1.set_ylabel('# Susceptibles')
        ax1.plot(t, self.S, label="Susceptibles", color='r')
        ax2.set_ylabel("# Exposed")
        ax2.plot(t, self.E, label="Exposed", color='g')
        ax3.set_ylabel("# Infected")
        ax3.plot(t, self.I, label="Infected")
        ax4.set_ylabel("# Recovered")
        ax4.plot(t, self.R, label="Recovered", color='c')
        ax5.set_ylabel("# Dead")
        ax5.plot(t, self.D, label='Dead')
        ax6.set_ylabel("# Vaccinated")
        ax6.plot(t, self.V, label="Vaccinated")
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        ax5.legend()
        ax6.legend()
        plt.show()
