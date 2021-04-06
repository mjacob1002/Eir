import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from Eir.utility import randEvent, Person

from.HubSEIR import HubSEIR
from Eir.DTMC.spatialModel.simul_details import Simul_Details

class HubSEIRV(HubSEIR):
    """
    Object that represents the Hub Model with compartments S, E, I, R, and V. In this model, E is assumed to not be
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
        Initial amount of vaccinated at the start of the simulation.

    pss: float
        The probability that the randomly generated person at the start of the simulation is a super spreader.
    
    rho: float
        Rho is the probability of someone moving from E to I compartment. Rho is in [0, 1]. 
    
    gamma: float
        The probability of someone going from I to R.
    
    eta: float
        The probability of someone going from S to V, given that they didn't go from S to E.
    
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
    
    popsize: int
        The total size of the population in the simulation. Given by S0 + I0 + R0 + V0.
        
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


    details: Simul_Details 
        An object that can be returned to give a more in-depth look into the simulation. With this object,
        one can see transmission chains, state changes, the movement history of each individaul, the state
        history of each person, and more.
    

    """
    def __init__(self, S0: int, E0: int, I0: int, R0: int, V0:int, pss: float, rho: float, 
        gamma: float, eta: float, side: float, rstart:float, days: int, w0=1.0, hubConstant=6**0.5, alpha=2.0, timeDelay=-1):
        # error checking
        # error checking
        self.intCheck([S0, E0, I0, R0, V0, days])
        self.floatCheck([pss, rho, gamma, eta, side, rstart, w0, alpha, hubConstant, timeDelay])
        self.negValCheck([S0, E0, I0, R0, V0, pss, rho, gamma, eta, side, rstart, days, w0, hubConstant, alpha])
        self.probValCheck([pss, rho, gamma, eta, w0])

        # S->v, given that didn't go to S->E
        super(HubSEIRV, self).__init__(S0=S0, E0=E0, I0=I0, R0=R0, pss=pss, rho=rho, gamma=gamma, side=side, rstart=rstart, alpha=alpha, 
        days=days)
        self.popsize = self.popsize + V0
        self.V = np.zeros(self.days+1)
        self.V[0] = V0
        self.Scollect, self.Ecollect, self.Icollect, self.Rcollect = [], [], [], []
        self.Vcollect = []
        self.locx, self.locy = np.random.random(self.popsize)*side, np.random.random(self.popsize)*side
        self.eta = eta
        self.timeDelay = timeDelay
        self.details = Simul_Details(days, self.popsize, static=True)

        for i in range(self.popsize):
            event = randEvent(pss)
            p1 = Person(self.locx[i], self.locy[i], event)
            p2 = Person(self.locx[i], self.locy[i], event)
            p3 = Person(self.locx[i], self.locy[i], event)
            p4 = Person(self.locx[i], self.locy[i], event)
            p5 = Person(self.locx[i], self.locy[i], event)
            if i< S0:
                p1.isIncluded=True
                self.details.addStateChange(i, "S", 0)
            elif i < S0+E0:
                p2.isIncluded=True
                self.details.addStateChange(i, "E", 0)
            elif i < S0 + E0 + I0:
                p3.isIncluded=True
                self.details.addStateChange(i, "I", 0)
            elif i < S0 + E0 + I0 + R0:
                p4.isIncluded=True
                self.details.addStateChange(i, 'R', 0)
            else:
                self.details.addStateChange(i, "V", 0)
                p5.isIncluded=True
            self.Scollect.append(p1)
            self.Ecollect.append(p2)
            self.Icollect.append(p3)
            self.Rcollect.append(p4)
            self.Vcollect.append(p5)
            # add location
            self.details.addLocation(0, (p1.x, p1.y))

    def _StoV(self):
        return self._changeHelp(self.Scollect, self.eta)
    
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

            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSE) - len(transferSV)
            self.E[i] = self.E[i-1] +len(transferSE) - len(transferEI)
            self.I[i] = self.I[i - 1] + len(transferEI) - len(transferIR)
            self.R[i] = self.R[i-1] + len(transferIR)
            self.V[i] = self.V[i-1] + len(transferSV)
        if getDetails:
            return self.details
    
    def toDataFrame(self):
        """
        Converts the arrays to a pandas DataFrame.

        Return
        ------

        pd.DataFrame:
            a dataframe containing the people in S, E, I, R, and V compartments per day.
        """
        # create the linspaced numpy array
        t = np.linspace(0, self.days, self.days + 1)
        # create a 2D array with the days and susceptible and infected arrays
        # do it over axis one so that it creates columns days, susceptible, infected
        arr = np.stack([t, self.S, self.E, self.I, self.R, self.V], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Exposed", "Infected", "Recovered", "Vaccinated"])
        return df
    
    def plot(self):
        """
        Plots all variables on subplots

        Return
        -------

        pyplot.Figure:
            return a fig object that will contian the graphs
        """
        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("Number of Susceptible People")
        ax1.set_title("Hub SEIRV Simulation")
        ax3.plot(t, self.I, label="Active Cases", color='b')
        ax3.set_ylabel("Active Cases")
        ax2.plot(t, self.E, label="Exposed", color='c')
        ax2.set_ylabel("# of Exposed")
        ax4.plot(t, self.R, label="Recovered", color='m')
        ax5.set_xlabel("Days")
        ax4.set_ylabel('Number of Recovered')
        ax5.plot(t, self.V, label="Vaccinated")
        ax5.set_ylabel("# Vaccinated")
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        plt.show()
        return fig


    