import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from src.utility import randEvent, Person

from.HubSEIR import HubSEIR
from src.DTMC.spatialModel.simul_details import Simul_Details

class HubSEIRV(HubSEIR):

    def __init__(self, S0: int, E0: int, I0: int, R0: int, V0:int, pss: float, rho: float, 
        gamma: float, eta: float, side: float, rstart:float, alpha: int, days: int, w0=1.0, hubConstant=6**0.5, timeDelay=-1):
        # S->v, given that didn't go to S->E
        super(HubSEIRV, self).__init__(S0=S0, E0=E0, I0=I0, R0=R0, pss=pss, rho=rho, gamma=gamma, side=side, rstart=rstart, alpha=alpha, 
        days=days)
        self.popsize = self.popsize + V0
        self.V = np.zeros(self.days+1)
        self.V[0] = V0
        self.Scollect, self.Ecollect, self.Icollect, self.Rcollect = [], [], [], []
        self.Vcollect = []
        self.locx, self.locy = np.random.random(self.popsize)*side, np.random.random(self.popsize)*side
        self.eta = eta
        self.timeDelay = timeDelay
        self.details = Simul_Details(days, self.popsize)

        for i in range(self.popsize):
            event = randEvent(pss)
            p1 = Person(self.locx[i], self.locy[i], event)
            p2 = Person(self.locx[i], self.locy[i], event)
            p3 = Person(self.locx[i], self.locy[i], event)
            p4 = Person(self.locx[i], self.locy[i], event)
            p5 = Person(self.locx[i], self.locy[i], event)
            if i< S0:
                p1.isIncluded=True
                self.details.addStateChange(i, "S", 0)
            elif i < S0+E0:
                p2.isIncluded=True
                self.details.addStateChange(i, "E", 0)
            elif i < S0 + E0 + I0:
                p3.isIncluded=True
                self.details.addStateChange(i, "I", 0)
            elif i < S0 + E0 + I0 + R0:
                p4.isIncluded=True
                self.details.addStateChange(i, 'R', 0)
            else:
                self.details.addStateChange(i, "V", 0)
                p5.isIncluded=True
            self.Scollect.append(p1)
            self.Ecollect.append(p2)
            self.Icollect.append(p3)
            self.Rcollect.append(p4)
            self.Vcollect.append(p5)

    def _StoV(self):
        return self._changeHelp(self.Scollect, self.eta)
    
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

            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSE) - len(transferSV)
            self.E[i] = self.E[i-1] +len(transferSE) - len(transferEI)
            self.I[i] = self.I[i - 1] + len(transferEI) - len(transferIR)
            self.R[i] = self.R[i-1] + len(transferIR)
            self.V[i] = self.V[i-1] + len(transferSV)
        if getDetails:
            return self.details
    
    def toDataFrame(self):
        """
        Converts the arrays to a pandas DataFrame.

        Return
        ------

        pd.DataFrame:
            a dataframe containing the people in S, E, I, R, and V compartments per day.
        """
        # create the linspaced numpy array
        t = np.linspace(0, self.days, self.days + 1)
        # create a 2D array with the days and susceptible and infected arrays
        # do it over axis one so that it creates columns days, susceptible, infected
        arr = np.stack([t, self.S, self.E, self.I, self.R, self.V], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Exposed", "Infected", "Recovered", "Vaccinated"])
        return df
    
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
        ax1.set_title("Hub SEIRV Simulation")
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


    