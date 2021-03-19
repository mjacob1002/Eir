import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from src.DTMC.spatialModel.HubModel import Hub
from src.DTMC.spatialModel.simul_details import Simul_Details
from src.utility import Person, dist, randEvent


class HubSEIR(Hub):
    def __init__(self, S0: int, I0: int, R0: int, pss: float, rho: float, 
    gamma: float, side: float, rstart:float, alpha: int, days: int, w0=1.0, hubConstant=6**0.5):
        super(HubSEIR, self).__init__(popsize=S0+I0+R0, pss=pss, rstart=rstart, alpha=alpha, side=side, S0=S0, I0=I0,
                 days=days, w0=w0,hubConstant=hubConstant)
        self.gamma = gamma
        # initialize the probability of leaving E
        self.rho = rho
        # make the initial R class variable
        self.R0 = R0
        # create the R collect datastructure
        self.Rcollect = []
        # create the E collect datastructure
        self.Ecollect = []
        # create numpy arrays to store number of people in each compartment
        self.E = np.zeros(days+1)
        self.R = np.zeros(days+1)
        # put the initial removed values into the array
        self.R[0] = R0
        # create a Simul_Details object
        self.details = Simul_Details(days=days, popsize=self.popsize)
        for i in range(self.popsize):
            # susceptible version
            p1 = Person(self.locx[i], self.locy[i], randEvent(self.pss))
            # exposed version
            p2 = Person(self.locx[i], self.locy[i], randEvent(self.pss))
            # infectious version
            p3 = Person(self.locx[i], self.locy[i], randEvent(self.pss))
            # removed version
            p4 = Person(self.locx[i], self.locy[i], randEvent(self.pss))
            # depending on the number, say that the person is in S, I, R. Add that state to the Simul_Details object
            if i < S0:
                p1.isIncluded = True
                self.details.addStateChange(i, "S", 0)
            elif i < S0 + I0:
                p3.isIncluded = True
                
                self.details.addStateChange(i, "I", 0)
            else:
                p4.isIncluded = True
                self.details.addStateChange(i, "R", 0)
            # add the locations to the Simul_Details object
            self.details.addLocation(0, (self.locx[i], self.locy[i]))
            # append the Person objects to the collections
            self.Scollect.append(p1)
            self.Ecollect.append(p2)
            self.Icollect.append(p3)
            self.Rcollect.append(p4)
    
    # run state changes from S to E
    def _StoE(self, day: int):
        # set that keeps track of the indices of people that changed states
        transfers = set()
        for count, inf in enumerate(self.Icollect):
            if not inf.isIncluded:
                continue
            for count2, sus in enumerate(self.Scollect):
                #print("Susceptible Person ", count2)
                if not sus.isIncluded:
                    continue
                # generate the probability of infection
                prob = self._infect(inf, sus)
                # generate a random event based on the P(infection)
                event = randEvent(prob)
                # if an infection doesn't occur
                if not event:
                    continue
                # remove the person from the susceptible state
                self.Scollect[count2].isIncluded = False
                self.details.addTransmission(day, count, count2)
                # put the person in the transfer set to be made an exposed person
                transfers.add(count2)
        return transfers
    # run state changes from E to I
    def _EtoI(self):
        # set that keeps track of the indices of people that changed states
        transfers = set()
        for count, per in enumerate(self.Ecollect):
            if not per.isIncluded:
                continue
            event = randEvent(self.rho)
            if not event:
                continue
            self.Ecollect[count].isIncluded = False
            transfers.add(count)
        return transfers
    
    def _ItoR(self):
        # set that keeps track of the indices of people that changed states
        transfers = set()
        for count, inf in enumerate(self.Icollect):
            if not inf.isIncluded:
                continue
            event = randEvent(self.gamma)
            if not event:
                continue
            self.Icollect[count].isIncluded = False
            transfers.add(count)
        return transfers
    
    # run the simulation using
    def run(self, getDetails=True):
        for i in range(1, self.days + 1):
            print("Day: ", i)
            # run the transfers from different compartments
            transferSE = self._StoE(i)
            transferEI = self._EtoI()
            transferIR = self._ItoR()

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

            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSE)
            self.E[i] = self.E[i-1] +len(transferSE) - len(transferEI)
            self.I[i] = self.I[i - 1] + len(transferEI) - len(transferIR)
            self.R[i] = self.R[i-1] + len(transferIR)
        if getDetails:
            return self.details

    def plot(self):
        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("Number of Susceptible People")
        ax1.set_title("Hub SEIR Simulation")
        ax3.plot(t, self.I, label="Active Cases", color='b')
        ax3.set_ylabel("Active Cases")
        ax2.plot(t, self.E, label="Exposed", color='c')
        ax2.set_ylabel("# of Exposed")
        ax4.plot(t, self.R, label="Recovered", color='m')
        ax4.set_xlabel("Days")
        ax4.set_ylabel('Number of Recovered')
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        plt.show()
    
    # convert the arrays to dataframe
    def toDataFrame(self):
        # create the linspaced numpy array
        t = np.linspace(0, self.days, self.days + 1)
        # create a 2D array with the days and susceptible and infected arrays
        # do it over axis one so that it creates columns days, susceptible, infected
        arr = np.stack([t, self.S, self.E, self.I, self.R], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Exposed", "Infected", "Recovered"])
        return df



        
    