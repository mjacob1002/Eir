import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from .HubSEIRV import HubSEIRV
from Eir.utility import Person, randEvent


class HubSEIRVD(HubSEIRV):
    """
    Object that represents the Hub Model SEIRVD. In this model, E is assumed to not be
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
    
    V0: int
        Initial amount of vaccianted people at the start of the simulation.

    pss: float
        The probability that the randomly generated person at the start of the simulation is a super spreader.
    
    rho: float
        Rho is the probability of someone moving from E to I compartment. Rho is in [0, 1]. 
    
    gamma: float
        The probability of someone going from I to R.
    
    eta: float
        The probability of someone going from S to V, given that they aren't going from S to E.
    
    mu: float
        The probability of someone going from I to D, given that they aren't going from I to R.
    
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
    
    V: ndarray
        A numpy array that stores the number of people in the vaccinated state on each given day of the simulation.
    
    D: ndarray
        A numpy array that stores the number of people in the dead state on each given day of the simulation.
    
    popsize: int
        The total size of the population in the simulation. Given by S0 + E0 + I0 + R0 + V0.
        
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
    
    Vcollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is VACCINATED. Has a total of popsize Person objects,
        with numbers [0, popsize).
    
    Dcollect: list
        Vcollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is DEAD. Has a total of popsize Person objects,
        with numbers [0, popsize).


    details: Simul_Details 
        An object that can be returned to give a more in-depth look into the simulation. With this object,
        one can see transmission chains, state changes, the movement history of each individaul, the state
        history of each person, and more.
    

    """
    def __init__(self, S0: int, E0: int, I0: int, R0: int, V0:int, pss: float, rho: float, 
        gamma: float, eta:float, mu: float, side: float, rstart:float, days: int, w0=1.0, hubConstant=6**0.5, alpha=2.0, timeDelay=-1):
        # error checking
        self.intCheck([S0, E0, I0, R0, V0, days])
        self.floatCheck([pss, rho, gamma, eta, mu, side, rstart, w0, alpha, hubConstant, timeDelay])
        self.negValCheck([S0, E0, I0, R0, pss, rho, gamma, eta, mu, side, rstart, days, w0, hubConstant, alpha])
        self.probValCheck([pss, rho, gamma, eta, mu, w0])
        super().__init__(S0=S0, E0=E0, I0=I0, R0=R0, V0=V0, pss=pss, rho=rho, gamma=gamma, eta=eta, side=side, rstart=rstart, alpha=alpha, days=days, hubConstant=hubConstant, timeDelay=timeDelay)
        self.mu = mu
        self.Dcollect = []
        self.D = np.zeros(self.days+1)

        for i in range(self.popsize):
            p = Person(self.locx[i], self.locy[i], self.Scollect[i].ss)
            self.Dcollect.append(p)


    def _ItoD(self):
        return self._changeHelp(self.Icollect, self.mu)
    
    def run(self, getDetails=True):
        for i in range(1, self.days + 1):
            #print("Day: ", i)
            # run the transfers from different compartments
            transferSE = self._StoE(i)
            transferEI = self._EtoI()
            transferIR = self._ItoR()
            transferSV = set()
            if i > self.timeDelay:
                transferSV = self._StoV()
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
            self._stateChanger(transferSV, self.Vcollect, "V", i)
            self._stateChanger(transferID, self.Dcollect, 'D', i)

            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSE) - len(transferSV)
            self.E[i] = self.E[i-1] +len(transferSE) - len(transferEI)
            self.I[i] = self.I[i - 1] + len(transferEI) - len(transferIR) - len(transferID)
            self.R[i] = self.R[i-1] + len(transferIR)
            self.V[i] = self.V[i-1] + len(transferSV)
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
        arr = np.stack([t, self.S, self.E, self.I, self.R, self.D, self.V], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Exposed", "Infected", "Recovered", "Dead", "Vaccinated"])
        return df
    
    def plot(self):
        t = np.linspace(0,self.days, self.days+1)
        fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(nrows=6, sharex="all")
        ax1.set_title("Hub Model SEIRDV")
        ax6.set_xlabel("Days")
        ax1.set_ylabel('# Susceptibles')
        ax1.plot(t, self.S, label="Susceptibles")
        ax2.set_ylabel("# Exposed")
        ax2.plot(t, self.E, label="Exposed")
        ax3.set_ylabel("# Infected")
        ax3.plot(t, self.I, label="Infected")
        ax4.set_ylabel("# Recovered")
        ax4.plot(t, self.R, label="Recovered")
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
