import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .HubSEIRD import HubSEIRD

class HubSEIRSD(HubSEIRD):

    def __init__(self, S0: int, E0: int, I0: int, R0: int, pss: float, rho: float, 
        gamma: float, kappa: float, mu: float, side: float, rstart:float, alpha: int, days: int, w0=1.0, hubConstant=6**0.5):
        super().__init__(S0=S0, E0=E0, I0=I0, R0=R0, pss=pss, rho=rho, gamma=gamma, mu=mu,side=side, rstart=rstart, alpha=alpha, 
        days=days, hubConstant=hubConstant)

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
            # put it after I->R state change bc conditional probability
            transferID = self._ItoD()
            transferRS = self._RtoS()

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
            self._stateChanger(transferID, self.Dcollect, 'D', i)
            self._stateChanger(transferRS, self.Scollect, "S", i)

            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSE) + len(transferRS)
            self.E[i] = self.E[i-1] +len(transferSE) - len(transferEI)
            self.I[i] = self.I[i - 1] + len(transferEI) - len(transferIR) - len(transferID)
            self.R[i] = self.R[i-1] + len(transferIR) - len(transferRS)
            self.D[i] = self.D[i-1] + len(transferID)
        if getDetails:
            return self.details
    
    def plot(self):
        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("# Susceptibles")
        ax1.set_title("Hub Model SEIRSD Simulation")
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