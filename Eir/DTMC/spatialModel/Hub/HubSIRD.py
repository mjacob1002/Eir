import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from .HubSIR import HubSIR
from Eir.utility import randEvent, Person

class HubSIRD(HubSIR):
    """
    Hub Model with compartments S, I, R, and D.

    Parameters
    ----------
    S0: int
        The initial amount of susceptibles at the start of the simulation.
    
    I0: int
        The initial amount of infectious individuals at the start of the simulation.
    
    R0: int
        The inital amount of removed individuals at the start of the simulation.

    pss: float
        probability someone is considered a super spreader.
    
    rstart: float
        the spreading radius of every normal spreader.
    
    side: float
        size of one side of the square plane.
    
    days: int
        The number of days that are simulated.
    
    gamma: float
        The probability of someone from I going to R.
    
    mu: float
        The probability of going from I to D, given that the person isn't going from I to R. 
    
    w0: float (optional)
        The probability of infection if an infectious and susceptible individual are in the same location. Default is 1.0.
    
    hubConstant: float (optional)
        The factor k multliplied to the rstart if the person is a super spreader. Default is sqrt(6).
    
    alpha: float optional
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
    
    Dcollect: list
        contains the Person objects of everyone in simulation. If an element in Dcollect has isIncluded=True,
        that means person is currently in removed compartment.
    
    locx: ndarray
        stores the x coordinate of each person in the simulation.
    
    locy: ndarray
        stores the y coordinate of each person in the simulation.
    

    """
    def __init__(self, S0: int, I0: int, R0: int, pss: float, rstart: float, side: float, days: int, gamma: float, mu:float, alpha=2.0, w0=1.0, hubConstant=6 ** 0.5):
        # error checking
        self.intCheck([S0, I0, R0,days])
        self.floatCheck([pss, gamma, mu, side, rstart, w0, alpha, hubConstant])
        self.negValCheck([S0, I0, R0, pss, gamma, mu, side, rstart, days, w0, hubConstant, alpha])
        self.probValCheck([pss, gamma, mu, w0])
        super().__init__(S0=S0, I0=I0, R0=R0, pss=pss, rstart=rstart, side=side, days=days, gamma=gamma, alpha=alpha, w0=w0, hubConstant=hubConstant)
        self.mu = mu
        self.D = np.zeros(days+1)
        self.Dcollect = []
        for i in range(self.popsize):
            self.Dcollect.append(Person(self.Scollect[i].x, self.Scollect[i].y, self.Scollect[i].ss))
    
    def _ItoD(self):
        return self._changeHelp(self.Icollect, self.mu)
    
    def run(self, getDetails=True):
        """
        This method runs the simulation of the HubSIRD object. 

        Parameters
        ----------

        getDetails : bool, optional
            Default is True. If True, returns a Simul_Details() object that will allow user to look more closely
            into the details of the simulation, including transmission chains, state history of particular people,
            and more. 

        Return
        ------
        Simul_Details():
            This is returned if getDetails=True. It allows the user to more closely examine the particular simulation.
            This includes, transmission chains, state history of particular people, and more. 
        """
        for i in range(1, self.days + 1):
            #print("Day ",i)
            # run the transfers from different compartments
            transferSI = self._StoI(i)
            transferIr = self._ItoR()
            transferID = self._ItoD()
            # go after and change the indices in the collection data structure thing
            self._stateChanger(transferSI, self.Icollect, "I", i)
            self._stateChanger(transferIr, self.Rcollect, "R", i)
            self._stateChanger(transferID, self.Dcollect, "D", i)
            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSI)
            self.I[i] = self.I[i - 1] + len(transferSI) - len(transferIr) - len(transferID)
            self.R[i] = self.R[i-1] + len(transferIr)
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
        arr = np.stack([t, self.S, self.I, self.R, self.D], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Infected", "Recovered", "Dead"])
        return df
    
    def plot(self):
        "Plots the number of susceptible, infected, dead, and recovered individuals on the y-axis and the number of days on the x-axis."

        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("# Susceptibles")
        ax1.set_title("Hub Model SIRD Simulation")
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