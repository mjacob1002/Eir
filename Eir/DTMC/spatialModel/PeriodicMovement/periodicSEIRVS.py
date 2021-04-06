import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from math import cos, sin, pi

from ..randomMovement.randMoveSEIRVS import RandMoveSEIRVS
from Eir.utility import Person2 as Person
from Eir.utility import randEvent, dist
from Eir.DTMC.spatialModel.simul_details import Simul_Details

class PeriodicSEIRVS(RandMoveSEIRVS):

    def __init__(self, S0:int, E0:int, I0:int, R0:int, V0: int, rho: float, gamma: float, kappa: float, eta:float, planeSize: float, move_r: float, sigma_R: float, 
        spread_r: float, sigma_r: float, days:int, w0=1.0, alpha=2.0, timeDelay=-1, k=5, std=pi/2):
        self.floatCheck(k, std)
        self.negValCheck(k, std)

        super().__init__(S0=S0, E0=E0, I0=I0, R0=R0, V0=V0, rho=rho, gamma=gamma, kappa=kappa, eta=eta, planeSize=planeSize, move_r=move_r, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r, days=days, w0=w0, alpha=alpha, timeDelay=timeDelay)

        self.k, self.std = k, std
        # create a Simul_Details object
        self.details = Simul_Details(days=days, popsize=self.popsize)

        # reinstantiate the collect structures
        self.Scollect, self.Ecollect, self.Icollect, self.Rcollect, self.Vcollect = [], [], [], [], []

        loc_x, loc_y, spreading_r = np.random.random(self.popsize)*planeSize, np.random.random(self.popsize)*planeSize, np.random.normal(spread_r, sigma_r, self.popsize)
        mvnt_r = np.random.normal(move_r, sigma_r, self.popsize)
        for i in range(self.popsize):
            theta = np.random.normal(2*pi/k, std)
            p1 = Person(loc_x[i], loc_y[i], mvnt_r[i], spreading_r[i], theta=theta)
            p2 = Person(loc_x[i], loc_y[i], mvnt_r[i], spreading_r[i], theta=theta)
            p3 = Person(loc_x[i], loc_y[i], mvnt_r[i], spreading_r[i], theta=theta)
            p4 = Person(loc_x[i], loc_y[i], mvnt_r[i], spreading_r[i], theta=theta)
            p5 = Person(loc_x[i], loc_y[i], mvnt_r[i], spreading_r[i], theta=theta)            
            if i < S0:
                p1.isIncluded=True
                self.details.addStateChange(i, "S", 0)
            elif i< S0+E0:
                p2.isIncluded=True
                self.details.addStateChange(i, "E", 0)
            elif i< S0+E0+I0:
                p3.isIncluded=True
                self.details.addStateChange(i, "I", 0)
            elif i< S0+E0+I0+R0:
                p4.isIncluded=True
                self.details.addStateChange(i, "R", 0)
            else:
                p5.isIncluded=True
                self.details.addStateChange(i, "V", 0)
            self.Scollect.append(p1)
            self.Ecollect.append(p2)
            self.Icollect.append(p3)
            self.Rcollect.append(p4)
            self.Vcollect.append(p5)
            self.details.addLocation(0, (p1.x, p1.y))

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
        "Plots the number of susceptible, exposed, infected, and recovered individuals on the y-axis and the number of days on the x-axis."
        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("# Susceptibles")
        ax1.set_title("Periodic Movement SEIRSV Simulation")
        ax2.plot(t, self.E, label="Exposed", color='g')
        ax2.set_ylabel("# Exposed")
        ax3.plot(t, self.I, label="Active Cases", color='b')
        ax3.set_ylabel("# Active Infections")
        ax5.set_xlabel("Days")
        ax4.set_ylabel("# Recovered")
        ax4.plot(t, self.R, label="Removed")
        ax5.plot(t, self.V, label="Vaccinated", color='c')
        ax5.set_ylabel("# Vaccinated")
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        ax5.legend()
        plt.show()