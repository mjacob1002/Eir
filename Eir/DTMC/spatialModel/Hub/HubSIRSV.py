import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from .HubSIRV import HubSIRV

class HubSIRSV(HubSIRV):
    """
    SIRSV compartmental model with the Hub model assumption. 

    Parameters
    ----------
    
    pss: float
        probability someone is considered a super spreader.
    
    rstart: float
        the spreading radius of every normal spreader.
    
    side: float
        size of one side of the square plane.
    
    S0: int
        The initial amount of susceptibles at the start of the simulation.
    
    I0: int
        The initial amount of infectious individuals at the start of the simulation.
    
    R0: int
        The inital amount of removed individuals at the start of the simulation.
    
    days: int
        The number of days that are simulated.
    
    gamma: float
        The probability of someone from I going to R.
    
    kappa: float
        The probability of someone going from R compartment to S.
    
    eta: float
        The probability of someone goign from S to V, given they don't go from S to I.
    
    w0: float (optional)
        The probability of infection if an infectious and susceptible individual are in the same location. Default is 1.0.
    
    hubConstant: float (optional)
        The factor k multliplied to the rstart if the person is a super spreader. Default is sqrt(6).
    
    alpha: int
        constant used in the P(infection) formula. Default is 2.0.

    
    Attributes
    ----------

    popsize: int
        size of the population.

    details: Simul_Details
        an object that can be returned using run(getDetails=True) that provides more insight about simulation
        by showing transmissions chains, personal history with states, and more. 
    S : ndarray
        stores the number of people S compartmet on each day.
    
    I : ndarray
        stores the number of people I compartmet on each day.
    
    R : ndarray
        stores the number of people R compartmet on each day.
    
    V: ndarray
        stores the number of people in the V compartment on each day.
    
    Scollect: list
        contains the Person objects of everyone in simulation. If an element in Scollect has isIncluded=True,
        that means person is currently in susceptible compartment.
    
    Icollect: list
        contains the Person objects of everyone in simulation. If an element in Icollect has isIncluded=True,
        that means person is currently in infected compartment.
    
    Rcollect: list
        contains the Person objects of everyone in simulation. If an element in Rcollect has isIncluded=True,
        that means person is currently in removed compartment.
    
    locx: ndarray
        stores the x coordinate of each person in the simulation.
    
    locy: ndarray
        stores the y coordinate of each person in the simulation.
    

    """
    def __init__(self, S0: int, I0: int, R0:int, V0: int, pss: float, gamma: float, kappa: float, eta:float, rstart: float, side: float, days:int, alpha=2, w0=1.0, hubConstant=6**0.5, timeDelay=-1):
        # error checking
        self.intCheck([S0, I0, R0,V0, days])
        self.floatCheck([pss, gamma, kappa, eta, side, rstart, w0, alpha, hubConstant, timeDelay])
        self.negValCheck([S0, I0, R0, V0, pss, gamma, kappa, eta, side, rstart, days, w0, hubConstant, alpha])
        self.probValCheck([pss, gamma, kappa, eta, w0])
        super().__init__(S0=S0, I0=I0, R0=R0, V0=V0, pss=pss, gamma=gamma, eta=eta, rstart=rstart, side=side, days=days, alpha=alpha, w0=w0, hubConstant=hubConstant, timeDelay=timeDelay)
        self.kappa = kappa
    
    def _RtoS(self):
        return self._changeHelp(self.Rcollect, self.kappa)
    
    def run(self, getDetails=True):
        for i in range(1, self.days + 1):
            #print("Day ",i)
            # run the transfers from different compartments
            transferSI = self._StoI(i)
            transferIr = self._ItoR()
            transferSV = set()
            if i > self.timeDelay:
                transferSV = self._StoV()
            transferRS = self._RtoS()
            # go after and change the indices in the collection data structure thing
            self._stateChanger(transferSI, self.Icollect, "I", i)
            self._stateChanger(transferIr, self.Rcollect, "R", i)
            self._stateChanger(transferSV, self.Vcollect, "V", i)
            self._stateChanger(transferRS, self.Scollect, "S", i)
            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSI) - len(transferSV) + len(transferRS)
            self.I[i] = self.I[i - 1] + len(transferSI) - len(transferIr)
            self.R[i] = self.R[i-1] + len(transferIr) - len(transferRS)
            self.V[i] = self.V[i-1] + len(transferSV)
        if getDetails:
            return self.details
    
    def plot(self):
        "Plots the number of susceptible, exposed, infected, and recovered individuals on the y-axis and the number of days on the x-axis."

        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("# Susceptibles")
        ax1.set_title("Hub Model SIRSV Simulation")
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
