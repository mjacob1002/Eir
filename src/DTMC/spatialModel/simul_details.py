# stores the class containing more detailed informaiton about transmission in spatial models
import numpy as np
import pandas as pd

class Simul_Details():
    def __init__(self, days: int, popsize : int):
        # popsize is the size of the population
        self.popsize = popsize
        # number of days the simulation goes for
        self.days = days
        # dictionary that stores the day as key and the transmission chain 
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
        
        # contains a 2D array that will contain the day when someone changed
        # state
        self.stateChanges = []
        # this is the number of rows
        for i in range(popsize):
            self.stateChanges.append([])  
         
    
    # add the tuples of locations to the locations 2D array
    # day is the current day of the simulation, location
    # is a tuple containing the x,y coordinate of the person
    def addLocation(self, day, location):
        self.locations[day].append(location)
    
    # add a state change for person number "u"
    # change will be in pair format, with first element being the day
    # and second being a letter representing state change
    def addStateChange(self, u: int, state: string, day: int):
        pair = (day, state)
        # for person u, append to their array the time of state change and state it became
        self.stateChanges[u].append(pair)
    
    # helper function for personHistory
    def _getMovementHistoryHelp(self, u:int):
        movementHistory = []
        for day in self.locations:
            movementHistory.append(self.locations[day][u])
        return movementHistory

    
    # get the history of a person, with states and times
    # movement=True will also return the movement history of the person
    def personHistory(self, u:int, movement=False):
        if movement:
            return self.stateChanges[u], self._getMovementHistoryHelp(u)
        return self.stateChanges[u]
    
    def addTransmission(self, day: int, inf: int, sus: int):
        # create a tuple containing the infectious number in [0], susceptible turned infectious in [1]
        transmission = (inf, sus)
        self.transmissions[day] = self.transmissions[day].append(transmission)
    
    # return the transmission dictionary, with days as the key
    def getTransmissionHistory(self):
        return self.transmissions
    
    # get the specific transmission history of a single person
    def personTransmissionHistory(self, u: int):
        history = []
        for i in range(1, self.days+1):
            # get the tranmission history on day i
            transmits = self.transmissions[i]
            # for each tuple in the transmission history on day i
            for j in transmits:
            # if the infectious person is person number u
                if j[0] == u:
                    # append the susceptible person that was infected, and the day that it happened
                    history.append((transmits[1], i))
        return history
    
    # return the transmission history on a specific day
    def transmissionHistoryOnDay(self, day: int):
        return self.transmissions[day]
    
    # return a sort list of tuples from greatest to smallest, with first element being person "n"
    # with m transmissions
    def sortedTransmissions(self):
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
            transDict[val] = transDict[val].append(i)
        
        transmits.sort()
        # create a final list to return, containing tuples
        # tuples of format (# of transmissions, list of people who had that many transmissions)
        for val in transmits:
            tup = (val, transDict[val])
            sortedTrans.append(tup)
        return sortedTrans
    



        

    

    
    
    


    
