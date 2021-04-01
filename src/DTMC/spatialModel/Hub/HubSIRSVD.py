import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

from .HubSIRVD import HubSIRVD

class HubSIRSVD(HubSIRVD):
    
    def __init__(self, S0: int, I0: int, R0:int, V0: int, pss: float, gamma: float, kappa:float, eta:float, mu:float, rstart: float, side: float, days:int, alpha=2, w0=1.0, hubConstant=6**0.5, timeDelay=-1):
        super().__init__(S0=S0, I0=I0, R0=R0, V0=V0, pss=pss, gamma=gamma, eta=eta, mu=mu, side=side, rstart=rstart, alpha=alpha, days=days, timeDelay=timeDelay)
        self.kappa = kappa
    
    def _RtoS(self):
        return self._changeHelp(self.Rcollect, self.kappa) 
    
    def run(self, getDetails=True):
        for i in range(1, self.days + 1):
            print("Day ",i)
            # run the transfers from different compartments
            transferSI = self._StoI(i)
            transferIr = self._ItoR()
            transferSV = set()
            if i > self.timeDelay:
                transferSV = self._StoV()
            transferID = self._ItoD()
            transferRS = self._RtoS()
            # go after and change the indices in the collection data structure thing
            self._stateChanger(transferSI, self.Icollect, "I", i)
            self._stateChanger(transferIr, self.Rcollect, "R", i)
            self._stateChanger(transferSV, self.Vcollect, "V", i)
            self._stateChanger(transferID, self.Dcollect, "D", i)
            self._stateChanger(transferRS, self.Scollect, "S", i)
            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSI) - len(transferSV) + len(transferRS)
            self.I[i] = self.I[i - 1] + len(transferSI) - len(transferIr) - len(transferID)
            self.R[i] = self.R[i-1] + len(transferIr) - len(transferRS)
            self.V[i] = self.V[i-1] + len(transferSV)
            self.D[i] = self.D[i-1] + len(transferID)
        if getDetails:
            return self.details
    
    def plot(self):
        t = np.linspace(0, self.days, self.days+1)
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_title("Hub Model SIRSVD")
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