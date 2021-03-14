from .HubSIS import HubSIS
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from src.utility import Person
import src.utility as u
from multipledispatch import dispatch


class HubSIR(HubSIS):
    def __init__(self, popsize: int, pss: float, rstart: float, alpha: int, side: float, S0: int, I0: int, R0: int,
                 days: int,
                 gamma: float, w0=1.0,
                 hubConstant=6 ** 0.5):
        self.R0 = R0
        super(HubSIR, self).__init__(popsize, pss, rstart, alpha, side, S0, I0, days, gamma, w0, hubConstant)
        # create and initialize the removed array
        self.R = np.zeros(days + 1)
        self.R[0] = R0
        # create the R collection data structure
        self.Rcollect = []

        # initialize the Scollect and Icollect arrays
        # this loop will make the isIncluded = True for all the susceptible
        for i in range(0, S0):
            # create the two person objects, with everything identical except the isIncluded boolean
            p1 = Person(self.locx[i], self.locy[i], u.randEvent(pss), isIncluded=True)
            p2 = Person(self.locx[i], self.locy[i], u.randEvent(pss))
            p3 = Person(self.locx[i], self.locy[i], u.randEvent(pss))
            # push them to the data structure/ array structure
            self.Scollect.append(p1)
            self.Icollect.append(p2)
            self.Rcollect.append(p3)
        # this loop will make the isIncluded = True for all the infecteds
        for i in range(S0, S0 + I0):
            # create the two person objects, with everything identical except the isIncluded boolean
            p1 = Person(self.locx[i], self.locy[i], u.randEvent(pss))
            p2 = Person(self.locx[i], self.locy[i], u.randEvent(pss), isIncluded=True)
            p3 = Person(self.locx[i], self.locy[i], u.randEvent(pss))
            # push them to the data structure/ array structure
            self.Scollect.append(p1)
            self.Icollect.append(p2)
            self.Rcollect.append(p3)
        # initialize the Rcollect array
        for i in range(S0 + I0, S0 + I0 + R0):
            # create the two person objects, with everything identical except the isIncluded boolean
            p1 = Person(self.locx[i], self.locy[i], u.randEvent(pss))
            p2 = Person(self.locx[i], self.locy[i], u.randEvent(pss))
            p3 = Person(self.locx[i], self.locy[i], u.randEvent(pss), isIncluded=True)
            # push them to the data structure/ array structure
            self.Scollect.append(p1)
            self.Icollect.append(p2)
            self.Rcollect.append(p3)

    # run state changes from I to R
    def _ItoR(self):
        # call the super method __ItoS, as it is effectively the same thing.
        # only difference will be that the transfers set will go from I to R
        transfers = self.__ItoS()
        return transfers

    # run the simulation using
    def run(self):
        for i in range(1, self.days + 1):
            # run the transfers from different compartments
            transferSI = self._StoI()
            transferIr = self._ItoR()
            # go after and change the indices in the collection data structure thing
            for index in transferSI:
                self.Icollect[index].isIncluded = True
            for index in transferIr:
                self.Scollect[index].isIncluded = True
            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSI)
            self.I[i] = self.I[i - 1] + len(transferSI) - len(transferIr)
            self.R[i] = self.R[i-1] + len(transferIr)

    # maybe add picking what to plot later
    def plot(self):
        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("Number of Susceptible People")
        ax1.set_title("Hub SIS Simulation")
        ax2.plot(t, self.I, label="Active Cases", color='b')
        ax2.set_ylabel("Active Cases")
        ax3.plot(t, self.R, label="Recovered", color='m')
        ax3.set_xlabel("Days")
        ax3.set_ylabel('Number of Recovered')
        ax1.legend()
        ax2.legend()
        ax3.legend()
        plt.show()

    # convert the arrays to dataframe
    def toDataFrame(self):
        # create the linspaced numpy array
        t = np.linspace(0, self.days, self.days + 1)
        # create a 2D array with the days and susceptible and infected arrays
        # do it over axis one so that it creates columns days, susceptible, infected
        arr = np.stack([t, self.S, self.I, self.R], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Infected", "Recovered"])
        return df