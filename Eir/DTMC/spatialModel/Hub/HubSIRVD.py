import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from .HubSIRV import HubSIRV
from Eir.utility import Person, randEvent

class HubSIRVD(HubSIRV):
    """
    SIRVD compartmental model with the Hub model assumption. 

    Parameters
    ----------

    popsize: int
        size of the population.
    
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
    
    V0: int
        The initial amount of vaccinated individuals at the start of the simulation.
    
    days: int
        The number of days that are simulated.
    
    gamma: float
        The probability of someone from I going to R.
    
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
    
    D: ndarray
        stores the number of people in the D compartment on each day.
    
    Scollect: list
        contains the Person objects of everyone in simulation. If an element in Scollect has isIncluded=True,
        that means person is currently in susceptible compartment.
    
    Icollect: list
        contains the Person objects of everyone in simulation. If an element in Icollect has isIncluded=True,
        that means person is currently in infected compartment.
    
    Rcollect: list
        contains the Person objects of everyone in simulation. If an element in Rcollect has isIncluded=True,
        that means person is currently in removed compartment.
    
    Vcollect: list
        contains the Person objects of everyone in simulation. If an element in Rcollect has isIncluded=True,
        that means person is currently in vaccinated compartment.
    
    Dcollect: list
        contains the Person objects of everyone in simulation. If an element in Rcollect has isIncluded=True,
        that means person is currently in dead compartment.
    
    locx: ndarray
        stores the x coordinate of each person in the simulation.
    
    locy: ndarray
        stores the y coordinate of each person in the simulation.
    

    """
    def __init__(self, S0: int, I0: int, R0:int, V0: int, pss: float, gamma: float, eta:float, mu:float, rstart: float, side: float, days:int, alpha=2, w0=1.0, hubConstant=6**0.5, timeDelay=-1):
        # error checking
        self.intCheck([S0, I0, R0, V0, days])
        self.floatCheck([pss, gamma, eta, mu, side, rstart, w0, alpha, hubConstant, timeDelay])
        self.negValCheck([S0, I0, R0, V0, pss, gamma, eta, mu, side, rstart, days, w0, hubConstant, alpha])
        self.probValCheck([pss, gamma, eta, mu, w0])
        super().__init__(S0=S0, I0=I0, R0=R0, V0=V0, pss=pss, gamma=gamma, eta=eta, side=side, rstart=rstart, alpha=alpha, days=days, timeDelay=timeDelay)
        self.mu = mu
        self.D = np.zeros(days+1)
        self.D[0] = 0
        self.Dcollect = []
        for i in range(self.popsize):
            self.Dcollect.append(Person(self.Scollect[i].x, self.Icollect[i].y, self.Scollect[i].ss))
        
    def _ItoD(self):
        return self._changeHelp(self.Icollect, self.mu)
    
    def run(self, getDetails=True):
        for i in range(1, self.days + 1):
            #print("Day ",i)
            # run the transfers from different compartments
            transferSI = self._StoI(i)
            transferIr = self._ItoR()
            transferSV = set()
            if i > self.timeDelay:
                transferSV = self._StoV()
            transferID = self._ItoD()
            #print(type(transferID))
            # go after and change the indices in the collection data structure thing
            self._stateChanger(transferSI, self.Icollect, "I", i)
            self._stateChanger(transferIr, self.Rcollect, "R", i)
            self._stateChanger(transferSV, self.Vcollect, "V", i)
            self._stateChanger(transferID, self.Dcollect, "D", i)
            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSI) - len(transferSV)
            self.I[i] = self.I[i - 1] + len(transferSI) - len(transferIr) - len(transferID)
            self.R[i] = self.R[i-1] + len(transferIr)
            self.V[i] = self.V[i-1] + len(transferSV)
            self.D[i] = self.D[i-1] + len(transferID)
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
        arr = np.stack([t, self.S, self.I, self.R, self.V, self.D], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Infected", "Recovered", "Vaccinated", "Dead"])
        return df
    
    def plot(self):
        t = np.linspace(0, self.days, self.days+1)
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_title("Hub Model SIRVD")
        ax1.set_ylabel("# Susceptibles")
        ax2.plot(t, self.I, label="Infected", color='g')
        ax2.set_ylabel("# Active Cases")
        ax3.plot(t, self.R, label="Recovered", color='c')
        ax3.set_ylabel("# Recovered")
        ax4.plot(t, self.V, label="Vaccinated", color='b')
        ax4.set_ylabel("# Vaccinated")
        ax5.set_xlabel("Days")
        ax5.set_ylabel("# Dead")
        ax5.plot(t, self.D, label="Dead")
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        ax5.legend()
        plt.show()
        
        
