import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

from .HubSIR import HubSIR
import Eir.utility as u


class HubSIRS(HubSIR):
    """
    SIRS compartmental model with the Hub model assumption. 

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
    
    days: int
        The number of days that are simulated.
    
    gamma: float
        The probability of someone from I going to R.
    
    kappa: float
        The probability of someone going from R compartment to S.
    
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
    def __init__(self, pss: float, rstart: float, side: float, S0: int, I0: int, R0: int,
                 days: int,
                 gamma: float, kappa: float, w0=1.0,
                 hubConstant=6 ** 0.5, alpha=2.0):
        # error checking
        self.intCheck([S0, I0, R0,days])
        self.floatCheck([pss, gamma, kappa, side, rstart, w0, alpha, hubConstant])
        self.negValCheck([S0, I0, R0, pss, gamma, kappa, side, rstart, days, w0, hubConstant, alpha])
        self.probValCheck([pss, gamma, kappa, w0])
        self.kappa = kappa
        self.popsize = S0 +I0 + R0
        super(HubSIRS, self).__init__(S0=S0, I0=I0, R0=R0, pss=pss, rstart=rstart, side=side, days=days, gamma=gamma, alpha=alpha, w0=w0, hubConstant=hubConstant)

    # run transfers from R to S
    def _RS(self):
        """
        Deals with running state changes for peope in R compatment to S commpartment. 

        Returns
        -------

        set
            contains the number people who should get converted from R to S. For example, if the set contains
            3, that means that Scollect[3].isIncluded=True. This step is taken care of in run method.
        """
        # set that keeps track of the indices of people that changed states
        transfers = set()
        for count, inf in enumerate(self.Rcollect):
            if not inf.isIncluded:
                continue
            event = u.randEvent(self.gamma)
            if not event:
                continue
            self.Rcollect[count].isIncluded = False
            transfers.add(count)
        return transfers

    def run(self, getDetails=True):
        """
        This method runs the simulation of the HubSIRS object. 

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
        # for the days 1 to day
        for i in range(1, self.days + 1):
            # run the transfers from different compartments
            transferSI = self._StoI(i)
            transferIr = self._ItoR()
            transferRS = self._RS()
            # go after and change the indices in the collection data structure thing
            # S to I
            for index in transferSI:
                self.Icollect[index].isIncluded = True
                self.details.addStateChange(index, "I", i)
            # I to R
            for index in transferIr:
                self.Rcollect[index].isIncluded = True
                self.details.addStateChange(index, "R", i)
            # R to S
            for index in transferRS:
                self.Scollect[index].isIncluded = True
                self.details.addStateChange(index, "S", i)
            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSI) + len(transferRS)
            self.I[i] = self.I[i - 1] + len(transferSI) - len(transferIr)
            self.R[i] = self.R[i - 1] + len(transferIr) - len(transferRS)
        if getDetails:
            return self.details
    
    def plot(self):
        """Plots the number of people in each compartment each day. """
        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("Number of Susceptible People")
        ax1.set_title("Hub Model SIRS Simulation")
        ax2.plot(t, self.I, label="Active Cases", color='b')
        ax2.set_ylabel("Active Cases")
        ax3.plot(t, self.R, label="Recovered", color='m')
        ax3.set_xlabel("Days")
        ax3.set_ylabel('Number of Recovered')
        ax1.legend()
        ax2.legend()
        ax3.legend()
        plt.show()
