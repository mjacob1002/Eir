import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from Eir.utility import randEvent
from Eir.utility import Person1 as Person
from .randMoveSIR import RandMoveSIR
from Eir.DTMC.spatialModel.simul_details import Simul_Details

class RandMoveSIRV(RandMoveSIR):
    """
    Class that simulates the random movement model with an SIRV model. People in the Exposed compartment are presumed to not be able to propogate infection.

    Parameters:
    ----------

    S0: int
        The starting number of susceptible individuals in the simulation.
    
    I0: int
        The starting number of infectious individuals in the simulation. 
    
    R0: int
        The starting number of recovered individuals in the simulation.
    
    V0: int
        The starting number of vaccinated individuals in the simulation.
    

    gamma: float
        The recovery probability of an individual going from I -> R.
    
    eta: float
        The probability of someone going from the S compartment to the V compartment, given that the person hasn't gone from S compartment to I compartment in that same state change.

    
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
        The probability of infection if the distance between an infectious person and susceptible person is 0.
    
    alpha: float optional
        A constant used in the _infect() method. The greater the constant, the greater the infection probability.
    
    timeDelay: int optional
        The time delay before the vaccine rollout. Default value is 0. If the day is greater than the time delay, then vaccine rollout will begin.

    Attributes
    ----------

    S: ndarray
        A numpy array that stores the number of people in the susceptible state on each given day of the simulation.
    
    I: ndarray
        A numpy array that stores the number of people in the infected state on each given day of the simulation.
    
    R: ndarray
        A numpy array that stores the number of people in the recovered state on each given day of the simulation.
    
    V: ndarray
        A numpy array that stores the number of people in the vaccinated state on each given day of the simulation.
    
    popsize: int
        The total size of the population in the simulation. Given by S0 + I0 + R0 + V0
        
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

    Vcollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is VACCINATED. Has a total of popsize Person objects,
        with numbers [0, popsize). 
    

    details: Simul_Details 
        An object that can be returned to give a more in-depth look into the simulation. With this object,
        one can see transmission chains, state changes, the movement history of each individaul, the state
        history of each person, and more.
    """
    
    def __init__(self, S0, I0, R0, V0, eta, gamma, planeSize, move_r:float, sigma_R:float, spread_r:float, sigma_r: float,
    days:int, w0=1.0, alpha=2.0, timeDelay=-1):

        self.intCheck([S0, I0, R0, V0, days])
        self.floatCheck(gamma, eta, planeSize, move_r, sigma_R, spread_r, sigma_r, w0, alpha, timeDelay)
        self.negValCheck(S0, I0, R0, V0, gamma, eta, planeSize, move_r, sigma_R, spread_r, sigma_r, days, w0, alpha)
        self.probValCheck([gamma, eta, w0])

        super(RandMoveSIRV, self).__init__(S0=S0, I0=I0, R0=R0, gamma=gamma, planeSize=planeSize, move_r=move_r, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r, days=days, w0=w0, alpha=alpha)
        # P(S->V|not S->E)
        self.eta = eta
        self.V0 = V0
        self.V = np.zeros(days+1)
        # represents the time delay for vaccine distribution
        self.timeDelay = timeDelay

        self.popsize = S0 + I0 + R0 + V0
        # reinitialize the details Simul_Details object
        self.details = Simul_Details(days=days, popsize=self.popsize)
        self.Scollect, self.Icollect, self.Rcollect, self.Vcollect = [], [], [], []
        loc_x, loc_y = np.random.random(self.popsize)*planeSize, np.random.random(self.popsize)*planeSize
        spreading_r = np.random.normal(spread_r, sigma_r, size=self.popsize)
        for i in range(self.popsize):
            p1 = Person(loc_x[i], loc_y[i], 0, spreading_r[i])
            p2 = Person(loc_x[i], loc_y[i], 0, spreading_r[i])
            p3 = Person(loc_x[i], loc_y[i], 0, spreading_r[i])
            p4 = Person(loc_x[i], loc_y[i], 0, spreading_r[i])
            if i<S0:
                p1.isIncluded=True
                self.details.addStateChange(i, "S", 0)
            elif S0 <= i < S0+I0:
                p2.isIncluded=True
                self.details.addStateChange(i, "I", 0)
            elif S0+I0 <= i < S0+I0+R0:
                p3.isIncluded=True
                self.details.addStateChange(i, "R", 0)
            else:
                p4.isIncluded=True
                self.details.addStateChange(i, "V", 0)
            self.Scollect.append(p1)
            self.Icollect.append(p2)
            self.Rcollect.append(p3)
            self.Vcollect.append(p4)
            self.details.addLocation(0, (p1.x, p1.y))
    
    def _StoV(self):
        """
        Is responsible for state changes of S to V for those that haven't gone left S already in that same state change.

        Returns
        -------

        set:
            Contains all of the indices representing people who will move from S to V.
        """
        return self._changeHelp(self.Scollect, self.eta)
    
    def run(self, getDetails=True):
        for i in range(1, self.days+1):
            StoI = self._StoI(i)
            StoV = set()
            if i > self.timeDelay:
                StoV = self._StoV()
            ItoR = self._ItoR()
            self._stateChanger(StoI, self.Icollect, "I", i)
            self._stateChanger(StoV, self.Vcollect, "V", i)
            self._stateChanger(ItoR, self.Rcollect, "R", i)
            self._move(i, [self.Scollect, self.Icollect, self.Rcollect, self.Vcollect])
            self.S[i] = self.S[i-1] - len(StoI) - len(StoV)
            self.I[i] = self.I[i-1] + len(StoI) - len(ItoR)
            self.R[i] = self.R[i-1] + len(ItoR)
            self.V[i] = self.V[i-1] + len(StoV)
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
        arr = np.stack([t, self.S, self.I, self.R, self.V], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Infected", "Removed", "Vaccinated"])
        return df
    
    def plot(self):
        "Plots the number of susceptible, exposed, infected, and recovered individuals on the y-axis and the number of days on the x-axis."

        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("# Susceptibles")
        ax1.set_title("Random Movement SIRV Simulation")
        ax3.plot(t, self.V, label="Vaccinated", color='g')
        ax3.set_ylabel("# Vaccinated")
        ax2.plot(t, self.I, label="Active Cases", color='b')
        ax2.set_ylabel("# Active Infections")
        ax4.set_xlabel("Days")
        ax4.set_ylabel("# Recovered")
        ax4.plot(t, self.R, label="Removed")
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        plt.show()
