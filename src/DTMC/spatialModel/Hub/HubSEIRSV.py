import numpy as np
from matplotlib import pyplot as plt

from .HubSEIRV import HubSEIRV

class HubSEIRSV(HubSEIRV):

    def __init__(self, S0: int, E0: int, I0: int, R0: int, V0:int, pss: float, rho: float, 
        gamma: float, eta: float, kappa:float, side: float, rstart:float, alpha: int, days: int, w0=1.0, hubConstant=6**0.5, timeDelay=-1):
        super(HubSEIRSV, self).__init__(S0=S0, E0=E0, I0=I0, R0=R0, V0=V0, pss=pss, rho=rho, gamma=gamma, eta=eta, side=side, rstart=rstart, alpha=alpha, 
        days=days, timeDelay=timeDelay)
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
            transfersRS = self._RtoS()
            

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
            self._stateChanger(transfersRS, self.Scollect, "S", i)

            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSE) - len(transferSV) + len(transfersRS)
            self.E[i] = self.E[i-1] +len(transferSE) - len(transferEI)
            self.I[i] = self.I[i - 1] + len(transferEI) - len(transferIR)
            self.R[i] = self.R[i-1] + len(transferIR) - len(transfersRS)
            self.V[i] = self.V[i-1] + len(transferSV)
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
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("Number of Susceptible People")
        ax1.set_title("Hub SEIRSV Simulation")
        ax3.plot(t, self.I, label="Active Cases", color='b')
        ax3.set_ylabel("Active Cases")
        ax2.plot(t, self.E, label="Exposed", color='c')
        ax2.set_ylabel("# of Exposed")
        ax4.plot(t, self.R, label="Recovered", color='m')
        ax5.set_xlabel("Days")
        ax4.set_ylabel('Number of Recovered')
        ax5.plot(t, self.V, label="Vaccinated")
        ax5.set_ylabel("# Vaccinated")
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        plt.show()
        return fig