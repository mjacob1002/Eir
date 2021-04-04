import numpy as np
import pandas as pd
import unittest

from src.DTMC.spatialModel.Hub.HubSIRS import HubSIRS
import src.exceptions as e 

# seed the RNG; only for unit testing and reproducibility purposes
np.random.seed(0)

class Test_HubSIRS(unittest.TestCase):

    def __init__(self):
        self.test = HubSIRS(pss=.2, rstart=3, alpha=2, side=25, S0=999, I0=1, R0=0, days=31, gamma=.4, kappa= .2, w0=.7)
        self.sdetails = self.test.run()
    
    def generateCSV(self):
        df = self.test.toDataFrame()
        df.to_csv("HubSIRS.csv", index=False)
    
    def checkOutputs(self):
        df = self.test.toDataFrame()
        df2 = pd.read_csv("HubSIRS.csv")
        assert df.equals(df2)
        print("Output Test Passed")
    
    def checkSimulInputs(self):
        # checks for invalid person inputs
        self.assertRaises(e.NotIntException, self.sdetails.personHistory, 100.0)
        self.assertRaises(e.PersonNotFound, self.sdetails.personHistory, 1001)
        # checks for exceptions when inputting days
        self.assertRaises(e.DayOutOfRange, self.sdetails.transmissionHistoryOnDay, 65)
        self.assertRaises(e.DayOutOfRange, self.sdetails.transmissionHistoryOnDay, -1)
        self.assertRaises(e.NotIntException, self.sdetails.transmissionHistoryOnDay, 25.0)
        print("Simul_Details input test passed: throws error for invalid inputs")
    
    def checkInputs(self):
        # test less, as most of stuff tested in Parent class
        self.assertRaises(e.NotFloatException, HubSIRS, .2, 3, 2, 25, 999, 1, 0, 31, .4, '.2', .7)
        self.assertRaises(e.ProbabilityException, HubSIRS, .2, 3, 2, 25, 999, 1, 0, 31, .4, 1.2, .7)
        print("Inputs Test Passed")

if __name__== '__main__':
    test = Test_HubSIRS()
    #test.generateCSV()
    test.checkOutputs()
    test.checkSimulInputs()
    test.checkInputs()
    

    
    
    