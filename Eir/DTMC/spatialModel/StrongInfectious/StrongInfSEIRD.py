import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from ..Hub.HubSEIRD import HubSEIRD
from Eir.utility import Person, dist

class StrongInfSEIRD(HubSEIRD):

    def __init__(self, S0: int, E0: int, I0: int, R0: int, pss: float, rho: float, 
        gamma: float, mu: float, side: float, rstart:float, days: int, w0=0.7, alpha=2.0):

        #error checking
        self.intCheck([S0, E0, I0, R0, days])
        self.floatCheck([pss, rho, gamma, mu, side, rstart, w0, alpha])
        self.negValCheck([S0, E0, I0, R0, pss, rho, gamma, mu, side, rstart, days, w0, alpha])
        self.probValCheck([pss, rho, gamma, mu, w0])

        super().__init__(S0=S0, E0=E0, I0=I0, R0=R0, pss=pss, rho=rho, gamma=gamma, mu=mu, side=side, rstart=rstart, alpha=alpha, days=days, w0=w0, hubConstant=1)
    
    def _infect(self, inf: Person, sus: Person):
        """
        Computes the probability of infection between an infectious persona and susceptible based on Strong Infectious Model assumptions
        """
        # compute the distance between two Person objects
        r = dist(inf, sus)
        # make variable that can potentially be changed if someone is a super spreader
        r0 = self.rstart
        # if the susceptible is too far away from the infectious person
        if r > r0:
            return 0
        # in range of the infected person
        if inf.ss:
            return self.w0
        # return using the normal probability function if not a super spreader
        return self.w0 * (1 - r / r0) ** self.alpha
    
    def plot(self):
        "Plots the number of susceptible, exposed, infected, recovered, and dead individuals on the y-axis and the number of days on the x-axis."

        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("# Susceptibles")
        ax1.set_title("Strong Infectious Model SEIRD Simulation")
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