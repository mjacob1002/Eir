import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from .HubSEIR import HubSEIR

class HubSEIRS(HubSEIR):
    """
    Object that represents the Hub Model SEIRS. In this model, E is assumed to not be
    able to spread the virus.

    Parameters
    ----------
    S0: int
        Initial amount of susceptibles at the start of the simulation.

    E0: int
        Initial amount of exposed at the start of the simulation.
    
    I0: int
        Initial amount of infected at the start of the simulation.
    
    R0: int
        Initial amount of recovered at the start of the simulation. 

    pss: float
        The probability that the randomly generated person at the start of the simulation is a super spreader.
    
    rho: float
        Rho is the probability of someone moving from E to I compartment. Rho is in [0, 1]. 
    
    gamma: float
        The probability of someone going from I to R.
    
    kappa: float
        The probability of someone going from R to S compartment.
    
    rstart: float
        The spreading radius of a normal spreader.
    
    days: int   
        The nubmer of days being simulated.
    
    w0: float optional
        The probability of a susceptible getting infected if the distance between the infectious person and susceptible is 0. Default is 1.0.
    
    hubConstant: float optional
        The scale by which the spreading radius of a super spreader increases. Default is sqrt(6).
    
    alpha: float optional
        Constant used in the infect probability generator. Default is 2.0.
    
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
        The total size of the population in the simulation. Given by S0 + E0 + I0 + R0.
        
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
    def __init__(self, S0: int, E0: int, I0: int, R0: int, pss: float, rho: float, 
        gamma: float, kappa: float, side: float, rstart:float, days: int, w0=1.0, hubConstant=6**0.5, alpha=2.0):
        #error checking
        self.intCheck([S0, E0, I0, R0, days])
        self.floatCheck([pss, rho, gamma, kappa, side, rstart, w0, alpha, hubConstant])
        self.negValCheck([S0, E0, I0, R0, pss, rho, gamma, kappa, side, rstart, days, w0, hubConstant, alpha])
        self.probValCheck([pss, rho, gamma, kappa, w0])
        super(HubSEIRS, self).__init__(S0, E0, I0, R0, pss, rho, gamma, side, rstart, days, w0=w0, hubConstant=hubConstant, alpha=alpha)
        self.kappa = kappa
    
    def _RtoS(self):
        return self._changeHelp(self.Rcollect, self.kappa)
    
    def run(self, getDetails=True):
        for i in range(1, self.days + 1):
            #print("Day: ", i)
            # run the transfers from different compartments
            transferSE = self._StoE(i)
            transferEI = self._EtoI()
            transferIR = self._ItoR()
            transferRS = self._RtoS()

            # go after and change the indices in the collection data structure thing
            self._stateChanger(transferSE, self.Ecollect, "E", i)
            self._stateChanger(transferEI, self.Icollect, "I", i)
            self._stateChanger(transferIR, self.Rcollect, "R", i)
            self._stateChanger(transferRS, self.Scollect, "S", i)


            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSE) + len(transferRS)
            self.E[i] = self.E[i-1] +len(transferSE) - len(transferEI)
            self.I[i] = self.I[i - 1] + len(transferEI) - len(transferIR)
            self.R[i] = self.R[i-1] + len(transferIR) - len(transferRS)
        if getDetails:
            return self.details
    
    def plot(self):
        """
        Plots all variables on subplots

        Return
        -------

        pyplot.Figure:
            return a fig object that will contian the graphs
        """
        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("Number of Susceptible People")
        ax1.set_title("Hub SEIRS Simulation")
        ax3.plot(t, self.I, label="Active Cases", color='b')
        ax3.set_ylabel("Active Cases")
        ax2.plot(t, self.E, label="Exposed", color='c')
        ax2.set_ylabel("# of Exposed")
        ax4.plot(t, self.R, label="Removed", color='m')
        ax4.set_xlabel("Days")
        ax4.set_ylabel('Number of Removed')
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        plt.show()
        return fig