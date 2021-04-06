
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from multipledispatch import dispatch

from .HubSIS import HubSIS
from Eir.utility import Person
import Eir.utility as u
from Eir.DTMC.spatialModel.simul_details import Simul_Details



class HubSIR(HubSIS):
    """
    Hub Model with compartments S, I, R

    Parameters
    ----------
    S0: int
        The initial amount of susceptibles at the start of the simulation.
    
    I0: int
        The initial amount of infectious individuals at the start of the simulation.
    
    R0: int
        The inital amount of removed individuals at the start of the simulation.

    pss: float
        probability someone is considered a super spreader.
    
    rstart: float
        the spreading radius of every normal spreader.
    
    side: float
        size of one side of the square plane.
    
    days: int
        The number of days that are simulated.
    
    gamma: float
        The probability of someone from I going to R.
    
    w0: float (optional)
        The probability of infection if an infectious and susceptible individual are in the same location. Default is 1.0.
    
    hubConstant: float (optional)
        The factor k multliplied to the rstart if the person is a super spreader. Default is sqrt(6).
    
    alpha: float optional
        constant used in the P(infection) formula. Default is 2.0.

    
    Attributes
    ----------
    details: Simul_Details
        an object that can be returned using run(getDetails=True) that provides more insight about simulation
        by showing transmissions chains, personal history with states, and more. 
    S : ndarray
        stores the number of people S compartmet on each day.
    
    I : ndarray
        stores the number of people I compartmet on each day.
    
    R : ndarray
        stores the number of people R compartmet on each day.
    
    Scollect: list
        contains the Person objects of everyone in simulation. If an element in Scollect has isIncluded=True,
        that means person is currently in susceptible compartment.
    
    Icollect: list
        contains the Person objects of everyone in simulation. If an element in Icollect has isIncluded=True,
        that means person is currently in infected compartment.
    
    Rcollect: list
        contains the Person objects of everyone in simulation. If an element in Rcollect has isIncluded=True,
        that means person is currently in removed compartment.
    
    locx: ndarray
        stores the x coordinate of each person in the simulation.
    
    locy: ndarray
        stores the y coordinate of each person in the simulation.
    

    """
    def __init__(self, S0: int, I0: int, R0: int, pss: float, rstart: float, side: float, 
                 days: int, gamma: float, alpha=2.0, w0=1.0,hubConstant=6 ** 0.5):
        # error checking
        self.intCheck([S0, I0, R0,days])
        self.floatCheck([pss, gamma, side, rstart, w0, alpha, hubConstant])
        self.negValCheck([S0, I0, R0, pss, gamma, side, rstart, days, w0, hubConstant, alpha])
        self.probValCheck([pss, gamma, w0])
        super(HubSIR, self).__init__(S0=S0, I0=I0, pss=pss, rstart=rstart, alpha=alpha, days=days, side=side, w0=w0, gamma=gamma, hubConstant=hubConstant)
        #print(self.gamma)
        # reconfigure the population size
        self.popsize = S0 + I0 + R0
        #print(self.popsize)
        # initialize the Simul_Details object
        self.details = Simul_Details(days=days, popsize=int(self.popsize), static=True)

        self.R0 = R0
        # create new array of locations for all of the individuals in the population
        self.locx = np.random.random(self.popsize)*side
        self.locy = np.random.random(self.popsize) * side
        #print("Leng of locations: ", len(self.locx))
        self.R = np.zeros(days + 1)
        self.R[0] = R0
        # create the R collection data structure and set the array structures back to undefined array
        # to undo the effects of the inheritance
        self.Scollect = []
        self.Icollect = []
        self.Rcollect = []

        # initialize the Scollect and Icollect arrays
        # this loop will make the isIncluded = True for all the susceptible
        for i in range(0, S0):
            ss = u.randEvent(pss)
            # create the two person objects, with everything identical except the isIncluded boolean
            p1 = Person(self.locx[i], self.locy[i], ss, isIncluded=True)
            p2 = Person(self.locx[i], self.locy[i], ss)
            p3 = Person(self.locx[i], self.locy[i], ss)
            # push them to the data structure/ array structure
            self.Scollect.append(p1)
            self.Icollect.append(p2)
            self.Rcollect.append(p3)
            self.details.addLocation(0, (self.locx[i], self.locy[i]))
            self.details.addStateChange(i, "S", 0)

        # this loop will make the isIncluded = True for all the infecteds
        for i in range(S0, S0 + I0):
            ss = u.randEvent(pss)
            # create the two person objects, with everything identical except the isIncluded boolean
            p1 = Person(self.locx[i], self.locy[i], ss)
            p2 = Person(self.locx[i], self.locy[i], ss, isIncluded=True)
            p3 = Person(self.locx[i], self.locy[i], ss)
            # push them to the data structure/ array structure
            self.Scollect.append(p1)
            self.Icollect.append(p2)
            self.Rcollect.append(p3)
            self.details.addLocation(0, (self.locx[i], self.locy[i]))
            self.details.addStateChange(i, "I", 0)
        # initialize the Rcollect array
        for i in range(S0 + I0, S0 + I0 + R0):
            ss = u.randEvent(pss)
            # create the two person objects, with everything identical except the isIncluded boolean
            p1 = Person(self.locx[i], self.locy[i], ss)
            p2 = Person(self.locx[i], self.locy[i], ss)
            p3 = Person(self.locx[i], self.locy[i], ss, isIncluded=True)
            # push them to the data structure/ array structure
            self.Scollect.append(p1)
            self.Icollect.append(p2)
            self.Rcollect.append(p3)
            # add location at Day 0
            self.details.addLocation(0, (self.locx[i], self.locy[i]))
            self.details.addStateChange(i, "R", 0)
        #print("Initial S0: ", self.S[0], " Initial I0: ", self.I[0], " Initial R0: ", self.R[0])
    # run state changes from I to R
    def _ItoR(self):
        """
        Takes care of state changes from I to R. Events are generated independent of location and variables
        except kappa.

        Returns
        -------

        set
            Contains indices of those who will be transferred from I to R. For example, if set contains 3, then
            the self.Rollect[3].isIncluded=True and self.Icollect.isIncluded should be set to false within the
            _ItoR() function.
        """
        # set that keeps track of the indices of people that changed states
        transfers = set()
        for count, inf in enumerate(self.Icollect):
            if not inf.isIncluded:
                continue
            #print("infected person ", count)
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
            #print("Day ",i, "self.days: ", self.days)
            # run the transfers from different compartments
            transferSI = self._StoI(i)
            transferIr = self._ItoR()
            # go after and change the indices in the collection data structure thing
            for index in transferSI:
                #print("Person ", index)
                self.Icollect[index].isIncluded = True
                self.details.addStateChange(index, "I", i)
            for index in transferIr:
                #print("Person ", index)
                self.Rcollect[index].isIncluded = True
                self.details.addStateChange(index, "R", i)
            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSI)
            self.I[i] = self.I[i - 1] + len(transferSI) - len(transferIr)
            self.R[i] = self.R[i-1] + len(transferIr)
        if getDetails:
            return self.details

    # maybe add picking what to plot later
    def plot(self):
        """
        Plots the variables S, I, and R against the number of days. 
        """
        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("Number of Susceptible People")
        ax1.set_title("Hub SIR Simulation")
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
        """
        Converts the arrays to a pandas DataFrame.

        Returns
        -------

        pd.DataFrame:
            a dataframe containing the number of people in S, I, and R compartments per day.
        """
        # create the linspaced numpy array
        t = np.linspace(0, self.days, self.days + 1)
        # create a 2D array with the days and susceptible and infected arrays
        # do it over axis one so that it creates columns days, susceptible, infected
        arr = np.stack([t, self.S, self.I, self.R], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Infected", "Recovered"])
        return df