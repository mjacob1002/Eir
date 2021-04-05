import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from Eir.utility import dist, Person, randEvent
from ..Hub.HubSIRD import HubSIRD

class StrongInfSIRD(HubSIRD):

    def __init__(self, S0: int, I0: int, R0: int, pss: float, rstart: float, side: float, days: int, gamma: float, mu:float, alpha=2.0, w0=1.0):
        # error checking
        self.intCheck([S0, I0, R0,days])
        self.floatCheck([pss, gamma, mu, side, rstart, w0, alpha])
        self.negValCheck([S0, I0, R0, pss, gamma, mu, side, rstart, days, w0, alpha])
        self.probValCheck([pss, gamma, mu, w0])
        super().__init__(S0=S0, I0=I0, R0=R0, pss=pss, rstart=rstart, side=side, days=days, gamma=gamma, mu=mu, alpha=alpha, w0=w0, hubConstant=1)

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
        "Plots the number of susceptible, infected, dead, and recovered individuals on the y-axis and the number of days on the x-axis."

        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("# Susceptibles")
        ax1.set_title("Strong Infectious SIRD Simulation")
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