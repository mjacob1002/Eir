import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from Eir.DTMC.spatialModel.HubModel import Hub
from Eir.DTMC.spatialModel.simul_details import Simul_Details
from Eir.utility import Person, dist, randEvent


class HubSEIR(Hub):
    """
    Object that represents the Hub Model with compartments S, E, I, and R. In this model, E is assumed to not be
    able to spread the virus.

    Parameters
    ----------
    S0: int
        Initial amount of susceptibles at the start of the simulation.

    E0: int
        Initial amount of exposed at the start of the simulation.
    
    I0: int
        Initial amount of infected at the start of the simulation.
    
    R0: int
        Initial amount of recovered at the start of the simulation. 

    pss: float
        The probability that the randomly generated person at the start of the simulation is a super spreader.
    
    rho: float
        Rho is the probability of someone moving from E to I compartment. Rho is in [0, 1]. 
    
    gamma: float
        The probability of someone going from I to R.
    
    rstart: float
        The spreading radius of a normal spreader.
    
    days: int   
        The nubmer of days being simulated.
    
    w0: float optional
        The probability of a susceptible getting infected if the distance between the infectious person and susceptible is 0. Default is 1.0.
    
    hubConstant: float optional
        The scale by which the spreading radius of a super spreader increases. Default is sqrt(6).
    
    alpha: float optional
        Constant used in the infect probability generator. Default is 2.0.
    
    Attributes
    ----------

    S: ndarray
        A numpy array that stores the number of people in the susceptible state on each given day of the simulation.
    
    E: ndarray
        A numpy array that stores the number of people in the exposed state on each given day of the simulation.
    
    I: ndarray
        A numpy array that stores the number of people in the infected state on each given day of the simulation.
    
    R: ndarray
        A numpy array that stores the number of people in the recovered state on each given day of the simulation.
    
    popsize: int
        The total size of the population in the simulation. Given by S0 + E0 +I0 + R0 + V0.
        
    Scollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is SUSCEPTIBLE. Has a total of popsize Person objects,
        with numbers [0, popsize). 
    
    Ecollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is EXPOSED. Has a total of popsize Person objects,
        with numbers [0, popsize). 
    
    Icollect: list
         Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is INFECTED. Has a total of popsize Person objects,
        with numbers [0, popsize).
    
    Rcollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is RECOVERED. Has a total of popsize Person objects,
        with numbers [0, popsize).


    details: Simul_Details 
        An object that can be returned to give a more in-depth look into the simulation. With this object,
        one can see transmission chains, state changes, the movement history of each individaul, the state
        history of each person, and more.
    

    """
    def __init__(self, S0: int, E0: int, I0: int, R0: int, pss: float, rho: float, 
    gamma: float, side: float, rstart:float, days: int, w0=1.0, hubConstant=6**0.5, alpha=2.0):
        #error checking
        self.intCheck([S0, E0, I0, R0, days])
        self.floatCheck([pss, rho, gamma, side, rstart, w0, alpha, hubConstant])
        self.negValCheck([S0, E0, I0, R0, pss, rho, gamma, side, rstart, days, w0, hubConstant, alpha])
        self.probValCheck([pss, rho, gamma, w0])

        super(HubSEIR, self).__init__(popsize=S0+I0+R0, pss=pss, rstart=rstart, alpha=alpha, side=side, S0=S0, I0=I0,
                 days=days, w0=w0,hubConstant=hubConstant)
        # adjust the popsize
        self.popsize += E0
        # locations in the plane
        self.locx, self.locy = np.random.random(self.popsize)*self.side, np.random.random(self.popsize)*self.side
        # probability of going from I to R
        self.gamma = gamma
        # initialize the probability of leaving E
        self.rho = rho
        # make the initial R class variable
        self.R0 = R0
        # create the R collect datastructure
        self.Rcollect = []
        # create the E collect datastructure
        self.Ecollect = []
        self.E0 = E0
        # create numpy arrays to store number of people in each compartment
        self.E = np.zeros(days+1)
        self.E[0] = E0
        self.R = np.zeros(days+1)
        # put the initial removed values into the array
        self.R[0] = R0
        # create a Simul_Details object
        self.details = Simul_Details(days=days, popsize=self.popsize, static=True)
        for i in range(self.popsize):
            # event is whether person is a super spreader
            event = randEvent(self.pss)
            # susceptible version
            p1 = Person(self.locx[i], self.locy[i], event)
            # exposed version
            p2 = Person(self.locx[i], self.locy[i], event)
            # infectious version
            p3 = Person(self.locx[i], self.locy[i], event)
            # removed version
            p4 = Person(self.locx[i], self.locy[i], event)
            # depending on the number, say that the person is in S, I, R. Add that state to the Simul_Details object
            if i < S0:
                p1.isIncluded = True
                self.details.addStateChange(i, "S", 0)
            elif i < S0 + I0:
                p3.isIncluded = True
                
                self.details.addStateChange(i, "I", 0)
            elif i < S0 + E0 + I0:
                p2.isIncluded=True
                self.details.addStateChange(i, "E", 0)
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
        """
        Deals with the transfers from S compartment to E compartment.

        Parameters
        ----------

        day: int
            feed in the current day the state transfer is taking place on.
        
        Return
        ------

        set:
            returns the set contianing the indices of those that whose self.Ecollect[index].isIncluded must be set to True

        """
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
        """
        Deals with transferring those from E compartment to I compartment.

        Return
        ------

        set:
            the indices of people who will be transferred from E compartment to I compartment
        """
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
        """
        Deals with transferring those from E compartment to I compartment.

        Return
        ------

        set:
            the indices of people who will be transferred from I compartment to R compartment
        """
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
            #print("Day: ", i)
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
        return fig
    
    # convert the arrays to dataframe
    def toDataFrame(self):
        """
        Converts the arrays to a pandas DataFrame.

        Return
        ------

        pd.DataFrame:
            a dataframe containing the people in S, E, I, and R compartments per day.
        """
        # create the linspaced numpy array
        t = np.linspace(0, self.days, self.days + 1)
        # create a 2D array with the days and susceptible and infected arrays
        # do it over axis one so that it creates columns days, susceptible, infected
        arr = np.stack([t, self.S, self.E, self.I, self.R], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Exposed", "Infected", "Recovered"])
        return df



        
    