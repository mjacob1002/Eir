# stores the class containing more detailed informaiton about transmission in spatial models
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import Eir.exceptions as e
"""


"""
class Simul_Details():
    """
    This class returns details about the simulation from the spatial model object. 
    It can give information about transmission chains, locations of individual people
    at any given time, and the state change history of each person in the simulation. 
    
    Parameters
    ----------
    
    days: int
        the number of days the simulation will go for. Found in the spatial model object
        
    popsize: int
        the number of people in the simulation.
    
    static: optional bool
        Used to detect whether the spatial object is static
    
    Attributes
    ----------
    transmissions: dictionary
        holds a list with a key "days" and values of tuples in the form of (infectious person, susceptible), 
        where infectious person and susceptible are numbers representing the people in the simulation. 
    
    locations: list<list>
        holds the (x,y) coordinates of every person in the simulation on different days. You can access
        the tuple location in the form of locations[day][personNumber]. For example, to access the 
        (x,y) location of person 5 on day 16, you'd look in locations[16][5]. If the model type is static,
        then simply look at locations[0] for a full list of the locations of the individuals in the simulation. 
    
    stateChanges: list
        holds the time and state change for every person in the simulation. In order to access the state
        history of person 5, you'd look at stateChanges[5]. The state changes are represented as tuples with
        the first element being the number day the state change occured, and the second element being a string
        representing the state which the person went to. For example, a state change tuple as (16,"S") would 
        mean that on day 16, a person transferred to state "S". 
    
    Methods
    -------

    personHistory(u: int, movement=False)
        Returns the state history of person u in the simulation. If movement=True, returns a tuple with
        the first element being a list containing the state history of person history and second element
        being a list containing the (x,y) coordinates of person u each day during the simulation. 
    
    getHistory()
        Returns a dictionary containing the entire transmission history each day. The key of the dictionary 
        is a day from [1,days] and the value is a list of all the transmissions for that day. 

    personTransmissionHistory(u: int)
        Returns a list of tuples containing two integers that represents the transmission history of person u. 
        The first integer represents the person that person u infected, and the second integer represents the day
        which the infection occured. 

    transmissionHistoryonDay(day: int)
        Get the transmission history on a particular day. Returns a list that contains tuples with two integers.
        The first integer represents the person who was infectious. The second integer represents the susceptible
        person who got infected. 
    
    sortedTransmisisons()
        Returns a list containing a tuple of an integer and a list. In the tuple, the integer represents 
        the number of transmissions, while the list contains integers representing the people who have made that many 
        transmissions. For example, for a tuple (6, [1,6,32]), this would mean that persons 1, 6, and 32 each delivered
        6 transmissions throughout the simulation. The list returned by sortedTransmissions() is sorted from highest
        to lowest. 
    
    plotTransmissions(bins=None)
        Returns a Figure object and displays a histogram with number of transmissions on the x-axis and
        the number of people who made that many transmissions on the y-axis. If bins=None, then the 
        method will automatically generate a histogram with 10 bins. If bins is an integer, then the method
        will automatically generate a histogram with that many bins. If a list of integers is passed in,
        then the method will use those integers as the bins for the histogram. 

    """

    def __init__(self, days: int, popsize : int, static=False):
        # boolean value to autodetect if it is static
        self.static = static
        # popsize is the size of the population
        self.popsize = popsize
        # number of days the simulation goes for
        self.days = days
        # Dictionary that stores the day as key and the transmission chain 
        # as value
        self.transmissions = {}
        # initialize the values of transmission
        for i in range(1, days+1):
            self.transmissions[i] = []

        # 2D array that will hold the locations of persons 0 ... n-1
        # from days 0 to self.days
        self.locations = []
        # putting arrays in the locations big array
        for i in range(days+1):
            self.locations.append([])
        
        # Contains a 2D array that will contain the day when someone changed
        # state

        self.stateChanges = []
        # this is the number of rows

        for i in range(int(popsize)):
            self.stateChanges.append([])  
    
    def _isPersonHere(self, u: int):
        """Checks to makes sure that the Person exists in the simulation."""
        if not 0 <= u < self.popsize:
            raise e.PersonNotFound(u)
    
    def _intCheck(self, nums:list):
        for num in nums:
            if type(num) != int:
                raise e.NotIntException(num)
    
    def _isDayHere(self, day: int):
        if not 0 <= day <= self.days:
            raise e.DayOutOfRange
    
    # Add the tuples of locations to the locations 2D array
    # day is the current day of the simulation, location
    # is a tuple containing the x,y coordinate of the person

    def addLocation(self, day: int, location: tuple):
        """
        Add the tuple containing (x,y) coordiante to the locations 2D list.

        Parameters
        ----------

        day: int
            the day for of the location added.
        
        location: tuple
            contains two floats, representing (x,y) coordinates of a particular person
        """
        self.locations[day].append(location)
    
    # add a state change for person number "u"
    # change will be in pair format, with first element being the day
    # and second being a letter representing state change

    def addStateChange(self, u: int, state: str, day: int):
        """
        Add the state changes for a given person a given day

        Parameters
        ----------

        u: int
            the person whose state change is beeing added.
        
        state: string
            the string representation of the state which person u is going to
        
        day: int
            the day which the person changed states
        """
        pair = (day, state)
        # for person u, append to their array the time of state change and state it became
        self.stateChanges[u].append(pair)
    
    # helper function for personHistory
    def _getMovementHistoryHelp(self, u:int):
        movementHistory = []
        if self.static:
            movementHistory.append(self.locations[0][u])
            return movementHistory
        for day, loc in enumerate(self.locations):
            movementHistory.append(loc[u])
        return movementHistory

    
    # get the history of a person, with states and times
    # movement=True will also return the movement history of the person
    def personHistory(self, u:int, movement=False):
        """
        Return the state history of a person u 

        Parameters
        ----------

        u: int
            the person whose history is returned.
        
        movement: bool, optional
            if set to True, will return a tuple containing the stateChanges list and a list
            representing movement history of a person with the index representing a specific day.
            Default is False
        
        Returns
        -------
        list:
            contains a list of tuples that represents the transmission history
        
        list; 
            only if movement=True. Returns a list of tuples representing (x,y) positions of person u
            on every day. 
        """
        # exception handling
        self._intCheck([u])
        self._isPersonHere(u)
        
        if movement:
            return self.stateChanges[u], self._getMovementHistoryHelp(u)
        return self.stateChanges[u]
    
    def addTransmission(self, day: int, inf: int, sus: int):
        # create a tuple containing the infectious number in [0], susceptible turned infectious in [1]
        transmission = (inf, sus)
        temp = self.transmissions[day]
        temp.append(transmission)
        self.transmissions[day] = temp
    
    # return the transmission dictionary, with days as the key
    def getTransmissionHistory(self):
        """
        Return the transmission dictionary, with the key being the day and the value being a list
        containing tuples with two integers representing people. The first element is the infectious individual 
        and the second element is the susceptible individual.

        Returns
        -------
        dictionary
            returns the class variable "transmissions"
        """
        return self.transmissions
    
    # get the specific transmission history of a single person
    def personTransmissionHistory(self, u: int):
        """
        Return the transmission history of a person u 

        Parameters
        ----------

        u: int
            the person whose history is returned.
        
        Returns
        -------
        list
            contains tuples of 2 integers representing the people which they infected and the day which 
            person u infected them, respectively. For example, (9, 3) means that person u infected person 9 on
            day 3. 
        """
        # exception handling
        self._intCheck([u])
        self._isPersonHere(u)

        history = []
        for i in range(1, self.days+1):
            # get the tranmission history on day i
            transmits = self.transmissions[i]
            # for each tuple in the transmission history on day i
            for j in transmits:
            # if the infectious person is person number u
                if j[0] == u:
                    #print("Pair:", j)
                    # append the susceptible person that was infected, and the day that it happened
                    history.append((j[1], i))
        return history
    
    # return the transmission history on a specific day
    def transmissionHistoryOnDay(self, day: int):
        """
        Return the transmission history of a particular day 

        Parameters
        ----------

        day: int
            the day of which the transmission history is returned.
        
        Returns
        -------
        list:
            a list containing tuples, the first element being the infectious individual, the second element
            representing the susceptible individual who was infected
        """
        # exception handling
        self._intCheck([day])
        self._isDayHere(day)
        return self.transmissions[day]
    
    # return a sort list of tuples from greatest to smallest, with first element being person "n"
    # with m transmissions
    def sortedTransmissions(self):
        """
        Returns a sorted list containing tuples. The first tuple is the number of tranmissions a person made,
        while the second element is a list containing the numbers of people who made that many transmissions is

        Returns
        -------

        list:
            a list containing tuples of two elements. 
        """
        # list containing the sorted  
        sortedTrans = []
        # creates the array of population size that stores number of tranmissions of each person
        transmits = np.zeros(self.popsize)
        # calculate the transmissions

        # for each day
        for i in range(1, self.days+1):
            # get the tranmissions history
            numTrans = self.transmissions[i]
            # for each tuple in the list, add one to the infectious person represented in the tuple
            for j in numTrans:
                transmits[j[0]] += 1
        
        transDict = {}
        # map the number of tranmissions with the people who transmitted
        for i, val in enumerate(transmits):
            if not transDict.get(val):
                transDict[val] = [i]
                continue
            temp = transDict[val]
            temp.append(i)
            transDict[val] = temp
        # sort in descending order
        transmits[::-1].sort()
        # create a final list to return, containing tuples
        # tuples of format (# of transmissions, list of people who had that many transmissions)
        # set to see if the value val has already been appended to the sortedTrans list
        seen = set()
        for val in transmits:
            # if it has already been added
            if val in seen:
                continue
            tup = (val, transDict[val])
            sortedTrans.append(tup)
            seen.add(val)
        return sortedTrans
    
    def plotTransmissions(self, bins=None):
        """
        Plots a histogram of the number of transmissions on the x, and number of people who had
        that many transmissions on the y. 

        Parameters
        ----------

        bins: optional
            If an integer is passed into bins, then it creates a histogram with that many bins. Otherwise,
            if a list is passed into bins, then the bins will be created as the integers in the list specify.
            bins=None by default, which means a default of 10 bins will be created.

        Returns
        -------

        fig: matplotlib.pytplot.figure
            A figure object that contains the histogram. 
        """
        if bins is None:
            bins = 10
        # creates the array of population size that stores number of tranmissions of each person
        transmits = np.zeros(self.popsize)
        # calculate the transmissions

        # for each day
        for i in range(1, self.days+1):
            # get the tranmissions history
            numTrans = self.transmissions[i]
            # for each tuple in the list, add one to the infectious person represented in the tuple
            for j in numTrans:
                transmits[j[0]] += 1
        fig = plt.hist(transmits, bins=bins, edgecolor='black')
        plt.show()
        return fig
    




        

    

    
    
    


    
