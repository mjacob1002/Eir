import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import math

import Eir.utility as u
from Eir.DTMC.spatialModel.simul_details import Simul_Details
# not to be confused with the person object that is used in the Hub/Strong Infectious Model
from Eir.utility import Person1 as Person
from .randMove import RandMove


class RandMoveSIS(RandMove):
    """
    An SIS model that follows the Random Movement Model. When the individuals in the simulation move, 
    they move according to a randomly generated angle and a randomly generated radius.

    Parameters:
    ----------

    S0: int
        The starting number of susceptible individuals in the simulation.
    
    I0: int
        The starting number of infectious individuals in the simulation. 

    gamma: float
        The recovery probability of an individual going from I -> S
    
    planeSize : float
        The length of each side of the square plane in which the individuals are confined to. For example,
        if planeSize=50, then the region which people in the simulation are confined to is the square with
        vertices (0,0), (50,0), (50,50), and (0,50).
    
    move_r: float
        The mean of the movement radius of each person in the simulation. Will be used as mean along with 
        sigma_R as the standard deviation to pull from a normal distribution movement radii each time 
        _move(day) function is called.
    
    sigma_R: float
        The standard deviation of the movement radius of each person in the simulation. Will be used along with 
        move_R as the mean to pull from a normal distribution movement radii each time _move(day) function is 
        called.

    spread_r: float
        The mean of the spreading radius of each person in the simulation. Will be used along with sigma_r 
        as the standard deviation to pull from an normal distribution spreading radii for each individaul person
        when the RandMoveSIS object is initialized. 
    
    sigma_r: float
        The standard deviation of the spreading radius of each person in the simulation. 
        Will be used along with spread_r as the mean to pull from an normal distribution spreading radii 
        for each individaul person when the RandMoveSIS object is initialized. 
    
    days: int
        The number of days that was simulated.
    
    W0: float optional
        The probability of infection if the distance between an infectious person and susceptible person is 0.
    
    alpha: float optional
        A constant used in the _infect() method. The greater the constant, the greater the infection probability.

    Attributes
    ----------

    S: ndarray
        A numpy array that stores the number of people in the susceptible state on each given day of the simulation.
    
    I: ndarray
        A numpy array that stores the number of people in the susceptible state on each given day of the simulation.
    
    popsize: int
        The total size of the population in the simulation. Given by S0 + I0
        
    Scollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is susceptible. Has a total of popsize Person objects,
        with numbers [0, popsize). 
    
    Icollect: list
         Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is INFECTED. Has a total of popsize Person objects,
        with numbers [0, popsize).


    details: Simul_Details 
        An object that can be returned to give a more in-depth look into the simulation. With this object,
        one can see transmission chains, state changes, the movement history of each individaul, the state
        history of each person, and more.
    
     """

    def __init__(self, S0:int, I0:int, gamma:float, planeSize:float, move_r:float, sigma_R:float, spread_r:float, sigma_r: float,
    days:int, w0=1.0, alpha=2.0):
        # error checks
        self.intCheck([S0, I0, days])
        self.floatCheck(gamma, planeSize, move_r, sigma_R, spread_r, sigma_r, w0, alpha)
        self.negValCheck(S0, I0, gamma, planeSize, move_r, sigma_R, spread_r, sigma_r, days, w0, alpha)
        self.probValCheck([gamma, w0])
        # call to super constructor
        super(RandMoveSIS, self).__init__(planeSize, move_r, spread_r, w0=w0)
        self.details = Simul_Details(days=days, popsize=S0+I0)
        # standard deviation of movement radius
        self.sigma_R = sigma_R
        # total population size
        self.popsize = S0 + I0
        # get the days
        self.days = days
        # initialize the gamma value
        self.gamma = gamma
        # generate the data structure with the arrays
        self.S, self.I = np.zeros(days+1), np.zeros(days+1)
        # initialize day 0 to have the starting susceptibles and infecteds
        self.S[0], self.I[0] = S0, I0
        # generate the special collections that hold the Person objects
        self.Scollect = []
        self.Icollect = []
        spreading_r = np.random.normal(spread_r, sigma_r, S0+I0)
        # generate the random x, y locations
        loc_x = np.random.random(S0+I0) * planeSize
        loc_y = np.random.random(S0+I0) * planeSize
        # create the special objects:
        for i in range(self.popsize):
            # create the person object
            # for this model, the people will move with random radius R each timestep
            # therefore, the R component can be made 0, as that is only relevant for the 
            # periodic mobility model
            p1 = Person(loc_x[i], loc_y[i], 0, spreading_r[i])
            p2 = Person(loc_x[i], loc_y[i], 0, spreading_r[i]) 
            self.details.addLocation(0, (loc_x[i], loc_y[i]))       
            # if the person is in the susceptible objects created
            if i < S0:
                p1.isIncluded = True
                self.details.addStateChange(i, "S", 0)
            elif S0 <= i < S0+I0:
                p2.isIncluded = True
                self.details.addStateChange(i, "I", 0)
            # append them to the data structure
            self.Scollect.append(p1)
            self.Icollect.append(p2)
            self.details.addLocation(0, (p1.x, p1.y))

    # helps _move method with boundary checks
    
    # move people within the planSize x planeSize plane
    def _move(self, day: int, collects: list):
        """
        Method that moves each person at the end of each state chage.

        Parameters
        ----------

        days: int
            The day that the movement is for. Used to log information in the details class variable. 

        collects: list
            A list of the different collection data structures in the model. Cycle through the list and change the coordinates to allow for better
            inheritance. 
        """
        # generate the correct number of movement radii
        movement_r = np.random.normal(self.move_r, self.sigma_R, self.popsize)
        # generate the random thetas
        thetas = np.random.uniform(low=0, high=2*math.pi, size=self.popsize)
        # looping through everyone and moving them; same person coordinates in Scollect and Icoolect,
        # so which array is looped through doesn't matter
        for index, person in enumerate(collects[0]):
            # adjust the x,y coordinate using polar coordinates
            # conduct the boundary check at the same time
            x = self._boundaryCheck(person.x + movement_r[index] * math.cos(thetas[index]))
            y = self._boundaryCheck(person.y + movement_r[index] * math.sin(thetas[index]))
            # add the new location to the Simul_Details object
            self.details.addLocation(day, (x,y))
            # change the x, y coordinates
            for j, collect in enumerate(collects):
                collects[j][index].x = x
                collects[j][index].y = y
            #self.Scollect[index].x, self.Icollect[index].x = x, x
            #self.Scollect[index].y, self.Icollect[index].y = y, y
    
    # deal with transfers from S to I compartments
    def _StoI(self, day: int):
        """
        Takes care of running state changes from S compartment to I compartment

        Parameters
        ----------

        day: int
            The day that the state chagne is for. Used to log information in the details class variable
        """
        #print("I've been called!")
        # set containing the indices for transfers
        transfers = set()
        for count, inf in enumerate(self.Icollect):
            # if the person isn't infected, check the next person
            if inf.isIncluded == False:
                continue
            for index, sus in enumerate(self.Scollect):
                # if the person isn't in the susceptible bin
                if sus.isIncluded == False:
                    continue
                event = self._infect(inf, sus)
                # if there is a successful infection
                if event:
                    #print("Infection")
                    # add the index to the transfer set to be transferred later
                    transfers.add(index)
                    # change the status to be not included in S collection
                    self.Scollect[index].isIncluded = False
                    # adjust the state change in the Simul_Details object
                    self.details.addTransmission(day, count, index)
        return transfers
    
    def _ItoS(self):
        """Takes care of running state changes from I compartment to S compartment """
        # set that contains the indices for transfering from I to S
        return self._changeHelp(self.Icollect, self.gamma)
    
    # run the simulation
    def run(self, getDetails=True):
        """
        Run the actual simulation. 

        Parameters
        ----------

        getDetails: bool optional
            If getDetails=True, then run will return a Simul_Details object which will allow the user to 
            examine details of the simulation that aren't immediately obvious.
        
        Returns
        -------

        Simul_Details:
            Allows the user to take a deeper look into the dynamics of the simulation by examining transmission
            chains. User can also examine transmission history and state changes of individuals in the object
            by utilizing the Simul_Details object. 
        """
        # for all the days in the simulation
        for i in range(1, self.days+1):
            #print("Day ", i)
            #print("Location: (", self.Scollect[0].x, ",", self.Scollect[0].y, ").")
            # run the state changes
            StoI = self._StoI(i)
            ItoS = self._ItoS()
            # change the indices of the transfers
            self._stateChanger(values=StoI, collect=self.Icollect, symbol="I", day=i)
            self._stateChanger(values=ItoS, collect=self.Scollect, symbol="S", day=i)
            # make everyone move randomly
            self._move(i, [self.Scollect, self.Icollect])
            # change the values in the arrays
            self.S[i] = self.S[i-1] - len(StoI) + len(ItoS)
            self.I[i] = self.I[i-1] + len(StoI) - len(ItoS)
        if getDetails:
            return self.details

    # switch everything to a dataframe
    def toDataFrame(self):
        """
        Gives user access to pandas dataframe with amount of people in each state on each day.

        Parameters
        ----------

        Returns
        -------

        pd.DataFrame
            DataFrame object containing the number of susceptibles and number of infecteds on each day. 

        """
        # create the linspaced numpy array
        t = np.linspace(0, self.days, self.days + 1)
        # create a 2D array with the days and susceptible and infected arrays
        # do it over axis one so that it creates columns days, susceptible, infected
        arr = np.stack([t, self.S, self.I], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Infected"])
        return df
    
    # maybe add picking what to plot later
    def plot(self):
        
        "Plots the number of susceptible and infected individuals on the y-axis and the number of days on the x-axis."

        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2) = plt.subplots(nrows=2, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("Number of Susceptible People")
        ax1.set_title("Random Movement SIS Simulation")
        ax2.plot(t, self.I, label="Active Cases", color='b')
        ax2.set_xlabel("Days")
        ax2.set_ylabel("Active Cases")
        ax1.legend()
        ax2.legend()
        plt.show()


                

                



            


    





        





