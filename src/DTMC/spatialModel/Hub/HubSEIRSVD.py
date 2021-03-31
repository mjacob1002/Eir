import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from .HubSEIRVD import HubSEIRVD

class HubSEIRSVD(HubSEIRVD):

    def __init__(self, S0: int, E0: int, I0: int, R0: int, V0:int, pss: float, rho: float, 
        gamma: float, kappa: float, eta:float, mu: float, side: float, rstart:float, alpha: int, days: int, w0=1.0, hubConstant=6**0.5, timeDelay=-1):
        super().__init__(S0=S0, E0=E0, I0=I0, R0=R0, V0=V0, pss=pss, rho=rho, gamma=gamma, eta=eta, mu=mu, side=side, rstart=rstart, alpha=alpha, days=days, hubConstant=hubConstant, timeDelay=timeDelay)
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
            transferSV = set()
            if i > self.timeDelay:
                transferSV = self._StoV()
            transferRS = self._RtoS()
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
            self._stateChanger(transferRS, self.Scollect, "S", i)

            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSE) - len(transferSV) + len(transferRS)
            self.E[i] = self.E[i-1] +len(transferSE) - len(transferEI)
            self.I[i] = self.I[i - 1] + len(transferEI) - len(transferIR) - len(transferID)
            self.R[i] = self.R[i-1] + len(transferIR) - len(transferRS)
            self.V[i] = self.V[i-1] + len(transferSV)
            self.D[i] = self.D[i-1] + len(transferID)
        if getDetails:
            return self.details
        
    def plot(self):
        t = np.linspace(0,self.days, self.days+1)
        fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(nrows=6, sharex="all")
        ax1.set_title("Hub Model SEIRSDV")
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