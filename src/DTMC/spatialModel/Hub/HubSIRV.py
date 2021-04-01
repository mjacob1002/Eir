import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from .HubSIR import HubSIR
from src.utility import Person, randEvent

class HubSIRV(HubSIR):

    def __init__(self, S0: int, I0: int, R0:int, V0: int, pss: float, gamma: float, eta:float, rstart: float, side: float, days:int, alpha=2, w0=1.0, hubConstant=6**0.5, timeDelay=-1):
        super().__init__(S0=S0, I0=I0, R0=R0, pss=pss, rstart=rstart, alpha=alpha, side=side, days=days, gamma=gamma, w0=w0, hubConstant=hubConstant)
        self.V0 = V0
        self.V = np.zeros(days+1)
        self.eta = eta
        self.V[0] = V0
        self.popsize += V0
        self.timeDelay = timeDelay
        self.Scollect, self.Icollect, self.Rcollect, self.Vcollect = [], [], [], []
        if V0 != 0:
            self.locx = np.random.random(self.popsize)*side
            self.locy = np.random.random(self.popsize)*side
        for i in range(self.popsize):
            p = []
            event = randEvent(self.pss)
            for j in range(4):
                p.append(Person(self.locx[i], self.locy[i], event))
            if i < S0:
                self.details.addStateChange(i, "S", 0)
                p[0].isIncluded=True
            elif i< S0 + I0:
                self.details.addStateChange(i, "I", 0)
                p[1].isIncluded=True
            elif i<S0+I0+R0:
                self.details.addStateChange(i, "R", 0)
                p[2].isIncluded=True
            else:
                self.details.addStateChange(i, "V", 0)
                p[3].isIncluded=True
            self.Scollect.append(p[0])
            self.Icollect.append(p[1])
            self.Rcollect.append(p[2])
            self.Vcollect.append(p[3])

    def _StoV(self):
        return self._changeHelp(self.Scollect, self.eta)
    
    def run(self, getDetails=True):
        for i in range(1, self.days + 1):
            print("Day ",i)
            # run the transfers from different compartments
            transferSI = self._StoI(i)
            transferIr = self._ItoR()
            transferSV = set()
            if i > self.timeDelay:
                transferSV = self._StoV()
            # go after and change the indices in the collection data structure thing
            self._stateChanger(transferSI, self.Icollect, "I", i)
            self._stateChanger(transferIr, self.Rcollect, "R", i)
            self._stateChanger(transferSV, self.Vcollect, "V", i)
            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSI) - len(transferSV)
            self.I[i] = self.I[i - 1] + len(transferSI) - len(transferIr)
            self.R[i] = self.R[i-1] + len(transferIr)
            self.V[i] = self.V[i-1] + len(transferSV)
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
        arr = np.stack([t, self.S, self.I, self.R, self.V], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Infected", "Removed", "Vaccinated"])
        return df
    
    def plot(self):
        "Plots the number of susceptible, exposed, infected, and recovered individuals on the y-axis and the number of days on the x-axis."

        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("# Susceptibles")
        ax1.set_title("Hub Model SIRV Simulation")
        ax3.plot(t, self.V, label="Vaccinated", color='g')
        ax3.set_ylabel("# Vaccinated")
        ax2.plot(t, self.I, label="Active Cases", color='b')
        ax2.set_ylabel("# Active Infections")
        ax4.set_xlabel("Days")
        ax4.set_ylabel("# Recovered")
        ax4.plot(t, self.R, label="Removed")
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        plt.show()


