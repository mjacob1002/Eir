import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from Eir.utility import dist, Person, randEvent
from ..Hub.HubSIRSVD import HubSIRSVD


class StrongInfSIRSVD(HubSIRSVD):

    def __init__(self, S0: int, I0: int, R0:int, V0: int, pss: float, gamma: float, kappa: float, eta:float, mu:float, rstart: float, side: float, days:int, alpha=2.0, w0=0.7, timeDelay=-1):
        # error checking
        self.intCheck([S0, I0, R0, V0, days])
        self.floatCheck([pss, gamma, kappa, eta, mu, side, rstart, w0, alpha, timeDelay])
        self.negValCheck([S0, I0, R0, V0, pss, gamma, kappa, eta, mu, side, rstart, days, w0, alpha])
        self.probValCheck([pss, gamma, kappa, eta, mu, w0])
        super().__init__(S0=S0, I0=I0, R0=R0, V0=V0, pss=pss, gamma=gamma, kappa=kappa, eta=eta, mu=mu, rstart=rstart, side=side, days=days, alpha=alpha, w0=w0, hubConstant=1, timeDelay=timeDelay)

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
        t = np.linspace(0, self.days, self.days+1)
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_title("Strong Infectious Model SIRSVD")
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