from ..HubModel import Hub
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from src.simulation.utility import Person
import src.simulation.utility as u
from multipledispatch import dispatch


class HubSIS(Hub):
    def __init__(self, popsize: int, pss: float, rstart: float, alpha: int, side: float, S0: int, I0: int, days: int,
                 gamma: float, w0=1.0,
                 hubConstant=6 ** 0.5):
        self.gamma = gamma
        # call the super constructor
        super(HubSIS, self).__init__(popsize, pss, rstart, alpha, side, S0, I0, days=days, w0=w0,
                                     hubConstant=hubConstant)
        # initialize the Scollect and Icollect arrays
        # this loop will make the isIncluded = True for all the susceptible
        for i in range(0, S0):
            # create the two person objects, with everything identical except the isIncluded boolean
            p1 = Person(self.locx[i], self.locy[i], u.randEvent(pss), isIncluded=True)
            p2 = Person(self.locx[i], self.locy[i], u.randEvent(pss))
            # push them to the data structure/ array structure
            self.Scollect.append(p1)
            self.Icollect.append(p2)
        # this loop will make the isIncluded = True for all the infecteds
        for i in range(S0, S0 + I0):
            # create the two person objects, with everything identical except the isIncluded boolean
            p1 = Person(self.locx[i], self.locy[i], u.randEvent(pss))
            p2 = Person(self.locx[i], self.locy[i], u.randEvent(pss), isIncluded=True)
            # push them to the data structure/ array structure
            self.Scollect.append(p1)
            self.Icollect.append(p2)

    # run state changes from S to I
    def _StoI(self):
        # set that keeps track of the indices of people that changed states
        transfers = set()
        for count, inf in enumerate(self.Icollect):
            if not inf.isIncluded:
                continue
            for sus in self.Scollect:
                if not sus.isIncluded:
                    continue
                # generate the probability of infection
                prob = self._infect(inf, sus)
                # generate a random event based on the P(infection)
                event = u.randEvent(prob)
                # if an infection doesn't occur
                if not event:
                    continue
                # remove the person from the susceptible state
                self.Scollect[count].isIncluded = False
                # put the person in the transfer set to be made an infectious person
                transfers.add(count)
        return transfers

    # run state changes from I to S
    def __ItoS(self):
        # set that keeps track of the indices of people that changed states
        transfers = set()
        for count, inf in enumerate(self.Icollect):
            if not inf.isIncluded:
                continue
            event = u.randEvent(self.gamma)
            if not event:
                continue
            self.Icollect[count].isIncluded = False
            transfers.add(count)
        return transfers

    # run the simulation using
    def run(self):
        for i in range(1, self.days + 1):
            # run the transfers from different compartments
            transferSI = self._StoI()
            transferIS = self.__ItoS()
            # go after and change the indices in the collection data structure thing
            for index in transferSI:
                self.Icollect[index].isIncluded = True
            for index in transferIS:
                self.Scollect[index].isIncluded = True
            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSI) + len(transferIS)
            self.I[i] = self.I[i - 1] + len(transferSI) - len(transferIS)

    # maybe add picking what to plot later
    def plot(self):
        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2) = plt.subplots(nrows=2, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("Number of Susceptible People")
        ax1.set_title("Hub SIS Simulation")
        ax2.plot(t, self.I, label="Active Cases", color='b')
        ax2.set_xlabel("Days")
        ax2.set_ylabel("Active Cases")
        ax1.legend()
        ax2.legend()
        plt.show()

    # convert the arrays to dataframe
    def toDataFrame(self):
        # create the linspaced numpy array
        t = np.linspace(0, self.days, self.days + 1)
        # create a 2D array with the days and susceptible and infected arrays
        # do it over axis one so that it creates columns days, susceptible, infected
        arr = np.stack([t, self.S, self.I], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Infected"])
        return df


# brief test: will delete later

#popsize = 1000
#pss = 0.2
#rstart = 4
#alpha = 2
#side = 50
#S0 = 999
#I0 = 1
#days = 31
#gamma = .2
#test = HubSIS(popsize=popsize, pss=pss, rstart=rstart, alpha=alpha, side=side, S0=S0, I0=I0, days=days, gamma=gamma)
#test.run()
#df = test.toDataFrame()
#print(df)
