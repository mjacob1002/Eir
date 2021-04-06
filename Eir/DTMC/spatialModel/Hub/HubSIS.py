from matplotlib import pyplot as plt
from multipledispatch import dispatch
import numpy as np
import pandas as pd

from Eir.utility import Person
from ..HubModel import Hub
from Eir.DTMC.spatialModel.simul_details import Simul_Details
import Eir.utility as u



class HubSIS(Hub):
    """
    Hub model with compartments S and I. 

    Parameters
    ----------

    S0: int
        The initial amount of susceptibles at the start of the simulation.
    
    I0: int
        The initial amount of infectious individuals at the start of the simulation.
    
    pss: float
        probability someone is considered a super spreader.
    
    rstart: float
        the spreading radius of every normal spreader.
    
    alpha: int
        constant used in the P(infection) formula.
    
    side: float
        size of one side of the square plane.
        
    days: int
        The number of days that are simulated.
    
    gamma: float
        The probability of someone from I going to S.
    
    w0: float (optional)
        The probability of infection if an infectious and susceptible individual are in the same location.
    
    hubConstant: float (optional)
        The factor k multliplied to the rstart if the person is a super spreader.

    
    Attributes
    ----------
    details: Simul_Details
        an object that can be returned using run(getDetails=True) that provides more insight about simulation
        by showing transmissions chains, personal history with states, and more. 
    S : ndarray
        stores the number of people S compartmet on each day.
    
    I : ndarray
        stores the number of people I compartmet on each day.
    
    Scollect: list
        contains the Person objects of everyone in simulation. If an element in Scollect has isIncluded=True,
        that means person is currently in susceptible compartment.
    
    Icollect: list
        contains the Person objects of everyone in simulation. If an element in Icollect has isIncluded=True,
        that means person is currently in infected compartment.

    locx: ndarray
        stores the x coordinate of each person in the simulation.
    locy: ndarray
        stores the y coordinate of each person in the simulation. 

    """
    def __init__(self, S0: int, I0: int, pss: float, rstart: float, side: float, days: int,
                 gamma: float, w0=1.0,
                 hubConstant=6 ** 0.5, alpha=2.0):
        # error checking
        self.intCheck([S0, I0, days])
        self.floatCheck([pss, rstart, side, gamma, w0, hubConstant, alpha])
        self.negValCheck([S0, I0, pss, rstart, side, days, gamma, w0, hubConstant, alpha])
        self.probValCheck([pss, gamma, w0])
        self.popsize = S0 + I0
        # initialize the Simul_Details object
        self.details = Simul_Details(days=days, popsize=self.popsize, static=True)

        self.gamma = gamma
        # call the super constructor
        super(HubSIS, self).__init__(self.popsize, pss, rstart, alpha, side, S0, I0, days=days, w0=w0,
                                     hubConstant=hubConstant)
        # initialize the Scollect and Icollect arrays
        # this loop will make the isIncluded = True for all the susceptible
        for i in range(0, S0):
            ss = u.randEvent(pss)
            # create the two person objects, with everything identical except the isIncluded boolean
            p1 = Person(self.locx[i], self.locy[i], ss, isIncluded=True)
            p2 = Person(self.locx[i], self.locy[i], ss)
            # put the locations in the Simul_Details object
            self.details.addLocation(0, (self.locx[i], self.locy[i]))
            # put the starting states in Simul_Details
            self.details.addStateChange(i, "S", 0)
            # push them to the data structure/ array structure
            self.Scollect.append(p1)
            self.Icollect.append(p2)
        # this loop will make the isIncluded = True for all the infecteds
        for i in range(S0, S0 + I0):
            ss = u.randEvent(pss)
            # put the locations in the Simul_Details object
            self.details.addLocation(0, (self.locx[i], self.locy[i]))
            # put the starting states in Simul_Details
            self.details.addStateChange(i, "I", 0)
            # create the two person objects, with everything identical except the isIncluded boolean
            p1 = Person(self.locx[i], self.locy[i], ss)
            p2 = Person(self.locx[i], self.locy[i], ss, isIncluded=True)
            # push them to the data structure/ array structure
            self.Scollect.append(p1)
            self.Icollect.append(p2)
        #print("Length of Scollect: ", len(self.Scollect))

    # run state changes from S to I
    def _StoI(self, day: int):
        """
        Takes care of state changes from S compartment to I compartmet. This uses the _infect function.

        Parameters
        ----------

        day: int
            The day that the state change is occuring. Used mainly to add to transmission chain in Simul_Details
            object. 
        
        Returns
        -------

        set
            Includes the people that will be transferred from S to I. For example, if set inclues the number 3
            then self.Icollect[3].isIncluded = True.
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
                event = u.randEvent(prob)
                # if an infection doesn't occur
                if not event:
                    continue
                # remove the person from the susceptible state
                self.Scollect[count2].isIncluded = False
                self.details.addTransmission(day, count, count2)
                # put the person in the transfer set to be made an infectious person
                transfers.add(count2)
        return transfers

    # run state changes from I to S
    def __ItoS(self):
        """
        Takes care of state changes from I to S. Operates independent of location.
        """
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
    def run(self, getDetails=True):
        """
        This method runs the simulation of the HubSIS object. 

        Parameters
        ----------

        getDetails : bool, optional
            Default is True. If True, returns a Simul_Details() object that will allow user to look more closely
            into the details of the simulation, including transmission chains, state history of particular people,
            and more. 

        Return
        ------
        Simul_Details():
            This is returned if getDetails=True. It allows the user to more closely examine the particular simulation.
            This includes, transmission chains, state history of particular people, and more. 
        """
        for i in range(1, self.days + 1):
            #print("Day: ", i)
            # run the transfers from different compartments
            transferSI = self._StoI(i)
            transferIS = self.__ItoS()
            # go after and change the indices in the collection data structure thing
            for index in transferSI:
                self.Icollect[index].isIncluded = True
                self.details.addStateChange(index, "I", i)
            for index in transferIS:
                self.Scollect[index].isIncluded = True
                self.details.addStateChange(index, "S", i)
            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSI) + len(transferIS)
            self.I[i] = self.I[i - 1] + len(transferSI) - len(transferIS)
        if getDetails:
            return self.details

    # maybe add picking what to plot later
    def plot(self):
        """
        Plots the variables S and I against the number of days. 
        """
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
        """
        Converts the arrays of S and I to a pandas dataframe.

        Returns
        -------

        pd.DataFrame
            Contains the number of susceptibles and infecteds on each day in the simulation.
        """
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
