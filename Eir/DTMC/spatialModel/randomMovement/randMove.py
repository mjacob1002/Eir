import numpy as np
import pandas as pd
import math
import Eir.utility as u
from Eir.DTMC.spatialModel.simul_details import Simul_Details
from Eir.utility import static_prob_help
import Eir.exceptions as e

# not to be confused with the person object that is used in the Hub/Strong Infectious Model
from Eir.utility import Person1 as Person

class RandMove():
    """
    Abstract class that isn't meant to be instantiated. Base class for all concrete randMove objects.

    Parameters
    ----------

    planeSize: float
        This is the size of the plane which the people are confined to.
    
    move_r: float
        The mean of the normal distribution from which the random distance is pulled from each time step.
    
    spread_r: float
        The mean of the normal distribution from which the random spreading radius for each person is pulled from.
    
    w0: float
        The starting probability if an infected and susceptible person are on the same (x,y) coordinate. Used in the _infect method.
    
    alpha: float, optional
        Constant used in the _infect method. Default value is 2.0. 

    """
    def __init__(self, planeSize, move_r, spread_r, w0, alpha=2.0):
        # size of the plane
        self.planeSize = planeSize
        # mean movement radius
        self.move_r = move_r
        # mean spreading radius
        self.spread_r = spread_r
        # initial probability of infection
        self.w0 = w0
        # constant for the infected equation
        self.alpha = alpha
        # pop size. This will typically be intialized for the subclasses, but make it a number for now
        self.popsize = 100
        # Simul_Details object
        self.details = Simul_Details(0, self.popsize)

    # determine whether an infection event has occured
    def _infect(self, inf: Person, sus: Person):
        """
        Both calculates the probability of infection and generates an infection event.

        Parameters
        ----------

        inf: Person
            The infectious Person object that may or may not infect sus.

        sus: Person
            The susceptible Person object that may or may not become infected by sus.
        
        Return
        ------

        bool:
            If True, then sus became infected. Otherwise, sus didn't become infected.
        """
        # get the distance between two points
        r = u.dist(inf, sus)
        # if the distance between two people is greater than the infected person's spreading radius
        if r > inf.r0:
            return False
        # compute the probability given that r is within range
        w = self.w0 * (1.0 - r/inf.r0)**self.alpha
        # generate a random infection event based on the probability of infection
        inf_event = u.randEvent(w)
        # return the event
        return inf_event

    # eventually do it for every person in each collection array; will be implemented in the sublcasses
    def _move(self, day: int, collect: list):
        """
        Responsible for moving the locations of each Person in the simulation. Does it in place.

        Parameters
        ----------
        day: int
            The current day that the move is taking place on. Is important for the Simul_Details() object in order to keep track of the movement patterns each day.
        
        collect: list
            Contains all of the collection data structures that will be cycled through for the moves. This allows for easy object-oriented design.
        """
        # generate the correct number of movement radii
        movement_r = np.random.normal(self.move_R, self.sigma_R, self.popsize)
        # generate the random thetas
        thetas = np.random.uniform(low=0, high=2*math.pi, size=self.popsize)

    # apply this check to every x and y coordinate to make sure they're always within the plane
    def _boundaryCheck(self, coordinate):
        """
        Makes sure that after each movement, the x and y coordinates stay within the plane.

        Parameters
        ----------

        coordiante: float
            The coordinate that is being checked to make sure that it is within range [0,planeSize].
        
        Returns
        -------
        float:
            The coordinate that is within bounds of the plane. If coordinate was >planeSize, this method returns planeSize. If the coordinate was <planeSize, this method returns 0.
            Otherwise, it returns the original coordinate value.
        """
        # if the coordinate is too low( below/ to the left of the square plane)
        if coordinate < 0:
            coordinate = 0
        # if the coordinate is too high(above/to the right of the square plane)
        elif coordinate > self.planeSize:
            coordinate = self.planeSize
        return coordinate
    
    # used to run the state changes
    def _stateChanger(self, values: set, collect: list, symbol: str, day:int):
        """
        Takes care of the state changes to a particular state. 

        Parameters
        ----------

        values: set
            values contains all of the indices of the people who need to be set to isIncluded=True in the collect list
        
        collect: list
            The particular list of Person objects that are going to be modified.
        
        symbol: str 
            The string representing the particular state that is going to. Used for details.
        
        day: int
            The day on which the transfer happened. Used for details.
        """
        for index in values:
            #print("Index: ", index)
            collect[index].isIncluded = True
            self.details.addStateChange(index, symbol, day)
    
    def _changeHelp(self, collect: list, prob: float):
        """
        Used in order to determine who goes from collect state to another using probability prob. 

        Parameters
        ----------

        collect:list
            collect is a list of Person objects. Edits in place because passes a reference.
    
        prob: float
            The probability of a Person object going from one state to another
        """
        return static_prob_help(collect, prob)

    def negValCheck(self, *args):
        """
        Checks to make sure that values are non-negative
        """
        for val in args:
            if val < 0:
                raise e.NegativeValException(val)
    
    def probValCheck(self, probs: list):
        """Checks to make sure probability values are 0<=p<=1"""
        for p in probs:
            # if the value is less than 0
            if p < 0:
                raise e.ProbabilityException(p, False)
            # if the value is greater than 1
            elif p > 1:
                raise e.ProbabilityException(p, True)
        
    def intCheck(self, nums:list):
        """ Makes sure everything in nums is an int"""
        for num in nums:
            if type(num) != int:
                raise e.NotIntException(num)
    
    def floatCheck(self, *args):
        """Makes sure everything in nums is either a float or an int"""
        for num in args:
            if type(num) != int and type(num) != float:
                raise e.NotFloatException(num)
