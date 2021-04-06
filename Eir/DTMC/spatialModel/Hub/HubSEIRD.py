import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from .HubSEIR import HubSEIR
from Eir.utility import Person
class HubSEIRD(HubSEIR):
    """
    Object that represents the Hub Model with compartments S, E, I, R, and D. In this model, E is assumed to not be
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
    
    mu: float
        The probability of going from I->D, given that they didn't go from I -> R.
    
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
    
    D: ndarray
        A numpy array that stores the number of people in the death state on each given day of the simulation.
    
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
    
    Dcollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is DEAD. Has a total of popsize Person objects,
        with numbers [0, popsize).


    details: Simul_Details 
        An object that can be returned to give a more in-depth look into the simulation. With this object,
        one can see transmission chains, state changes, the movement history of each individaul, the state
        history of each person, and more.
    

    """
    def __init__(self, S0: int, E0: int, I0: int, R0: int, pss: float, rho: float, 
        gamma: float, mu: float, side: float, rstart:float, days: int, w0=1.0, hubConstant=6**0.5, alpha=2.0):

        #error checking
        self.intCheck([S0, E0, I0, R0, days])
        self.floatCheck([pss, rho, gamma, mu, side, rstart, w0, alpha, hubConstant])
        self.negValCheck([S0, E0, I0, R0, pss, rho, gamma, mu, side, rstart, days, w0, hubConstant, alpha])
        self.probValCheck([pss, rho, gamma, mu, w0])

        super(HubSEIRD, self).__init__(S0=S0, E0=E0, I0=I0, R0=R0, pss=pss, rho=rho, gamma=gamma, side=side, rstart=rstart, alpha=alpha, days=days, hubConstant=hubConstant)
        self.Dcollect = []
        self.D = np.zeros(self.days+1)
        self.mu = mu

        for i in range(self.popsize):
            p = Person(self.locx[i], self.locy[i], self.Scollect[i].ss)
            self.Dcollect.append(p)
    
    def _ItoD(self):
        # if the person didn't go to R, test if they go to D
        return self._changeHelp(self.Icollect, self.mu)
    
    def run(self, getDetails=True):
        for i in range(1, self.days + 1):
            #print("Day: ", i)
            # run the transfers from different compartments
            transferSE = self._StoE(i)
            transferEI = self._EtoI()
            transferIR = self._ItoR()
            # put it after I->R state change bc conditional probability
            transferID = self._ItoD()

            # go after and change the indices in the collection data structure thing
            for index in transferSE:
                self.Ecollect[index].isIncluded = True
                self.details.addStateChange(index, "E", i)
            for index in transferEI:
                self.Icollect[index].isIncluded = True
                self.details.addStateChange(index, "I", i)
            for index in transferIR:
                self.Rcollect[index].isIncluded = True
                self.details.addStateChange(index, "R", i)
            self._stateChanger(transferID, self.Dcollect, 'D', i)

            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSE)
            self.E[i] = self.E[i-1] +len(transferSE) - len(transferEI)
            self.I[i] = self.I[i - 1] + len(transferEI) - len(transferIR) - len(transferID)
            self.R[i] = self.R[i-1] + len(transferIR)
            self.D[i] = self.D[i-1] + len(transferID)
        if getDetails:
            return self.details
    
    def toDataFrame(self):
        """
        Convert the data to a dataframe.
        
        Returns
        -------

        pd.DataFrame
            Holds the data of simulation in a DataFrame format.
        """
        t = np.linspace(0,self.days,self.days+1)
        arr = np.stack([t, self.S, self.E, self.I, self.R, self.D], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Exposed", "Infected", "Recovered", "Dead"])
        return df
    
    def plot(self):
        "Plots the number of susceptible, exposed, infected, recovered, and dead individuals on the y-axis and the number of days on the x-axis."

        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("# Susceptibles")
        ax1.set_title("Hub Model SEIRD Simulation")
        ax2.plot(t, self.E, label="Exposed", color='g')
        ax2.set_ylabel("# Exposed")
        ax3.plot(t, self.I, label="Active Cases", color='b')
        ax3.set_ylabel("# Active Infections")
        ax5.set_xlabel("Days")
        ax4.set_ylabel("# Recovered")
        ax4.plot(t, self.R, label="Recovered")
        ax5.plot(t, self.D, label="Dead")
        ax5.set_ylabel("# Dead")
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        ax5.legend()
        plt.show()