import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from Eir.utility import randEvent
from Eir.utility import Person1 as Person
from .randMoveSIR import RandMoveSIR
from Eir.DTMC.spatialModel.simul_details import Simul_Details


class RandMoveSEIR(RandMoveSIR):
    """
    Class that simulates the random movement model with an SEIR model. People in the Exposed compartment are presumed to not be able to propogate infection.

    Parameters:
    ----------

    S0: int
        The starting number of susceptible individuals in the simulation.
    
    E0: int
        The starting number of exposed individuals in the simulation.
    
    I0: int
        The starting number of infectious individuals in the simulation. 
    
    R0: int
        The starting number of recovered individuals in the simulation.
    
    rho: float
        The probability of someone going from the E compartment to the I compartment.

    gamma: float
        The recovery probability of an individual going from I -> R.
    
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
    
    E: ndarray
        A numpy array that stores the number of people in the exposed state on each given day of the simulation.
    
    I: ndarray
        A numpy array that stores the number of people in the infected state on each given day of the simulation.
    
    R: ndarray
        A numpy array that stores the number of people in the recovered state on each given day of the simulation.
    
    popsize: int
        The total size of the population in the simulation. Given by S0 + I0
        
    Scollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is SUSCEPTIBLE. Has a total of popsize Person objects,
        with numbers [0, popsize). 
    
    Ecollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is EXPOSED. Has a total of popsize Person objects,
        with numbers [0, popsize). 
    
    Icollect: list
         Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is INFECTED. Has a total of popsize Person objects,
        with numbers [0, popsize).
    
    Rcollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is RECOVERED. Has a total of popsize Person objects,
        with numbers [0, popsize).


    details: Simul_Details 
        An object that can be returned to give a more in-depth look into the simulation. With this object,
        one can see transmission chains, state changes, the movement history of each individaul, the state
        history of each person, and more.
    


    """
    def __init__(self, S0:int, E0:int, I0:int, R0:int, rho: float, gamma: float, planeSize: float, move_r: float, sigma_R: float, 
    spread_r: float, sigma_r: float, days:int, w0=1.0, alpha=2.0):
        # error checks
        self.intCheck([S0, E0, I0, R0, days])
        self.floatCheck(rho, gamma, planeSize, move_r, sigma_R, spread_r, sigma_r, w0, alpha)
        self.negValCheck(S0, E0, I0, R0, rho, gamma, planeSize, move_r, sigma_R, spread_r, sigma_r, days, w0, alpha)
        self.probValCheck([rho, gamma, w0])
        
        super(RandMoveSEIR, self).__init__(S0=S0, I0=I0, R0=R0, gamma=gamma, planeSize=planeSize, move_r=move_r, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r, days=days, w0=w0,alpha=alpha)
        # rho is the E->I
        self.rho=rho
        # create the numpy array for exposed
        self.E = np.zeros(days+1)
        self.E[0] = E0
        self.popsize = S0 + E0 + I0 + R0
        #print("Population: ", self.popsize)
        # reinstantiate the Simul_Details object
        self.details = Simul_Details(days=days, popsize=self.popsize)
        # create the collection data structures
        self.Scollect, self.Ecollect, self.Icollect, self.Rcollect = [], [], [], []
        # random x,y locations for the start of the simulation
        loc_x, loc_y = np.random.random(self.popsize) * self.planeSize, np.random.random(self.popsize) * self.planeSize
        spreading_r = np.random.normal(spread_r, sigma_r, self.popsize)

        for i in range(self.popsize):
            p1 = Person(loc_x[i], loc_y[i], 0, spreading_r[i])
            p2 = Person(loc_x[i], loc_y[i], 0, spreading_r[i])
            p3 = Person(loc_x[i], loc_y[i], 0, spreading_r[i])
            p4 = Person(loc_x[i], loc_y[i], 0, spreading_r[i])
            if i < S0:
                p1.isIncluded = True
                self.details.addStateChange(i, "S", 0)
            elif S0 <= i < S0 + E0:
                p2.isIncluded=True
                self.details.addStateChange(i, "E", 0)
            elif S0 + E0 <= i < S0 + E0 + I0:
                p3.isIncluded=True
                self.details.addStateChange(i, "I", 0)
            else:
                p4.isIncluded=True
                self.details.addStateChange(i, "R", 0)
            self.Scollect.append(p1)
            self.Ecollect.append(p2)
            self.Icollect.append(p3)
            self.Rcollect.append(p4)
            self.details.addLocation(0, (p1.x, p1.y))
    
    # essentially the same function, except those who are infected will go to E not I. Simply return set of all infected people.
    # _StoI() also adds the transmission data as to who infected who, so that doesn't need to be written again.
    def _StoE(self, day:int):
        return self._StoI(day)
    
    # runs state changes from E to I
    def _EtoI(self):
        return self._changeHelp(self.Ecollect, self.rho)
    
    def run(self, getDetails=True):
        for i in range(1, self.days+1):
            StoE = self._StoE(i)
            EtoI = self._EtoI()
            ItoR = self._ItoR()
            self._stateChanger(StoE, self.Ecollect, "E", i)
            self._stateChanger(EtoI, self.Icollect, "I", i)
            self._stateChanger(ItoR, self.Rcollect, "R", i)
            self._move(i, [self.Scollect, self.Ecollect, self.Icollect, self.Rcollect])
            self.S[i] = self.S[i-1] - len(StoE)
            self.E[i] = self.E[i-1] + len(StoE) - len(EtoI)
            self.I[i] = self.I[i-1] + len(EtoI) - len(ItoR)
            self.R[i] = self.R[i-1] + len(ItoR)
            

        if getDetails:
            return self.details

    def toDataFrame(self):
        """
        Gives user access to pandas dataframe with amount of people in each state on each day.

        Returns
        -------

        pd.DataFrame
            DataFrame object containing the number of susceptibles and number of infecteds on each day. 

        """
        # create the linspaced numpy array
        t = np.linspace(0, self.days, self.days + 1)
        # create a 2D array with the days and susceptible and infected arrays
        # do it over axis one so that it creates columns days, susceptible, infected
        arr = np.stack([t, self.S, self.E, self.I, self.R], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Exposed", "Infected", "Removed"])
        return df
    
    def plot(self):
        "Plots the number of susceptible, exposed, infected, and recovered individuals on the y-axis and the number of days on the x-axis."

        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("# Susceptibles")
        ax1.set_title("Random Movement SEIR Simulation")
        ax2.plot(t, self.E, label="Exposed", color='g')
        ax2.set_ylabel("# Exposed")
        ax3.plot(t, self.I, label="Active Cases", color='b')
        ax3.set_ylabel("# Active Infections")
        ax4.set_xlabel("Days")
        ax4.set_ylabel("# Recovered")
        ax4.plot(t, self.R, label="Removed")
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        plt.show()
