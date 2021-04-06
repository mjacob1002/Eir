import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

from .randMoveSIRD import RandMoveSIRD
from Eir.utility import Person1 as Person
from Eir.DTMC.spatialModel.simul_details import Simul_Details

class RandMoveSIRSD(RandMoveSIRD):
    """
    An SIRSD model that follows the Random Movement Model. When the individuals in the simulation move, 
    they move according to a randomly generated angle and a randomly generated distance.

    Parameters:
    ----------

    S0: int
        The starting number of susceptible individuals in the simulation.
    
    I0: int
        The starting number of infectious individuals in the simulation. 
    
    R0: int
        The starting number of recovered individuals in the simulation.

    gamma: float
        The recovery probability of an individual going from I -> R.
    
    kappa: float
        The probability of going from R -> S.
    
    mu: float
        The probability someone dies given that they do not recover in that same time step.
    
    planeSize : float
        The length of each side of the square plane in which the individuals are confined to. For example,
        if planeSize=50, then the region which people in the simulation are confined to is the square with
        vertices (0,0), (50,0), (50,50), and (0,50).
    
    move_r: float
        The mean of the movement radius of each person in the simulation. Will be used as mean along with 
        sigma_R as the standard deviation to pull from a normal distribution movement radii each time 
        _move(day) function is called.
    
    sigma_R: float
        The standard deviation of the movement radius of each person in the simulation. Will be used along with 
        move_R as the mean to pull from a normal distribution movement radii each time _move(day) function is 
        called.

    spread_r: float
        The mean of the spreading radius of each person in the simulation. Will be used along with sigma_r 
        as the standard deviation to pull from an normal distribution spreading radii for each individaul person
        when the RandMoveSIS object is initialized. 
    
    sigma_r: float
        The standard deviation of the spreading radius of each person in the simulation. 
        Will be used along with spread_r as the mean to pull from an normal distribution spreading radii 
        for each individaul person when the RandMoveSIS object is initialized. 
    
    days: int
        The number of days that was simulated.
    
    w0: float optional
        The probability of infection if the distance between an infectious person and susceptible person is 0. Default is 1.0.
    
    alpha: float optional
        A constant used in the _infect() method. The greater the constant, the greater the infection probability. Default is 2.0.

    Attributes
    ----------

    S: ndarray
        A numpy array that stores the number of people in the susceptible state on each given day of the simulation.
    
    I: ndarray
        A numpy array that stores the number of people in the infected state on each given day of the simulation.
    
    R: ndarray
        A numpy array that stores the number of people in the recovered state on each given day of the simulation.
    
    D: ndarray
        A numpy array that stores the number of people in the dead state on each given day of the simulation.
    
    popsize: int
        The total size of the population in the simulation. Given by S0 + I0 + R0.
        
    Scollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is SUSCEPTIBLE. Has a total of popsize Person objects,
        with numbers [0, popsize). 
    
    Icollect: list
         Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is INFECTED. Has a total of popsize Person objects,
        with numbers [0, popsize).
    
    Rcollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is RECOVERED. Has a total of popsize Person objects,
        with numbers [0, popsize).
    
    Dcollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is DEAD. Has a total of popsize Person objects,
        with numbers [0, popsize).


    details: Simul_Details 
        An object that can be returned to give a more in-depth look into the simulation. With this object,
        one can see transmission chains, state changes, the movement history of each individaul, the state
        history of each person, and more.
    
     """
    def __init__(self, S0, I0, R0, gamma, mu, kappa, planeSize, move_r:float, sigma_R:float, spread_r:float, sigma_r: float, days:int, w0=1.0, alpha=2.0):
        self.intCheck([S0, I0, R0, days])
        self.floatCheck(gamma, kappa, mu, planeSize, move_r, sigma_R, spread_r, sigma_r, w0, alpha)
        self.negValCheck(S0, I0, R0, gamma, kappa, mu, planeSize, move_r, sigma_R, spread_r, sigma_r, days, w0, alpha)
        self.probValCheck([gamma, kappa, mu, w0])
        self.kappa = kappa
        super(RandMoveSIRSD, self).__init__(S0=S0, I0=I0, R0=R0, gamma=gamma, mu=mu, planeSize=planeSize, move_r=move_r, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r,
        days=days)

    def _RtoS(self):
        return self._changeHelp(self.Rcollect, self.kappa)
    
    def run(self, getDetails=True):
        """
        Run the actual simulation. 

        Parameters
        ----------

        getDetails: bool optional
            If getDetails=True, then run will return a Simul_Details object which will allow the user to 
            examine details of the simulation that aren't immediately obvious.
        
        Returns
        -------

        Simul_Details:
            Allows the user to take a deeper look into the dynamics of the simulation by examining transmission
            chains. User can also examine transmission history and state changes of individuals in the object
            by utilizing the Simul_Details object. 
        """

        # for all the days in the simulation
        for i in range(1, self.days+1):
            #print("Day ", i)
            #print("Location: (", self.Scollect[0].x, ",", self.Scollect[0].y, ").")
            # run the state changes
            StoI = self._StoI(i)
            ItoR = self._ItoR()
            ItoD = self._ItoD()
            RtoS = self._RtoS()
            # change the indices of the transfers
            self._stateChanger(StoI, self.Icollect, "I", i)
            self._stateChanger(ItoR, self.Rcollect, "R", i)
            self._stateChanger(ItoD, self.Dcollect, "D", i)
            self._stateChanger(RtoS, self.Scollect, "S", i)
            
            # make everyone move randomly, don't move dead people
            self._move(i, [self.Scollect, self.Icollect, self.Rcollect])
            # change the values in the arrays
            self.S[i] = self.S[i-1] - len(StoI) + len(RtoS)
            self.I[i] = self.I[i-1] + len(StoI) - len(ItoR) - len(ItoD)
            self.R[i] = self.R[i-1] + len(ItoR) - len(RtoS)
            self.D[i] = self.D[i-1] + len(ItoD)
        if getDetails:
            return self.details
    
    def plot(self):
        "Plots the number of susceptible, infected, dead, and recovered individuals on the y-axis and the number of days on the x-axis."

        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("# Susceptibles")
        ax1.set_title("Random Movement SIRSD Simulation")
        ax4.plot(t, self.D, label="# Dead", color='g')
        ax4.set_ylabel("# Dead")
        ax2.plot(t, self.I, label="Active Cases", color='b')
        ax2.set_ylabel("# Active Infections")
        ax4.set_xlabel("Days")
        ax3.set_ylabel("# Recovered")
        ax3.plot(t, self.R, label="Recovered")
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        plt.show()
        