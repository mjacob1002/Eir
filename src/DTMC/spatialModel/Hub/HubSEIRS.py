import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from .HubSEIR import HubSEIR

class HubSEIRS(HubSEIR):

    def __init__(self, S0: int, E0: int, I0: int, R0: int, pss: float, rho: float, 
        gamma: float, kappa: float, side: float, rstart:float, alpha: int, days: int, w0=1.0, hubConstant=6**0.5):
        super(HubSEIRS, self).__init__(S0, E0, I0, R0, pss, rho, gamma, side, rstart, alpha, days, w0=w0, hubConstant=hubConstant)
        self.kappa = kappa
    
    def _RtoS(self):
        return self._changeHelp(self.Rcollect, self.kappa)
    
    def run(self, getDetails=True):
        for i in range(1, self.days + 1):
            print("Day: ", i)
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