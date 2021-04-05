import numpy as np
import pandas as pd
import unittest

from Eir.DTMC.spatialModel.Hub.HubSIRV import HubSIRV
import Eir.exceptions as e

np.random.seed(0)

class Test_HubSIRV(unittest.TestCase):

    def __init__(self):
        self.test = HubSIRV(S0=999, I0=1, R0=0, V0=0, pss=.17, gamma=.23, eta=.03, side=50, rstart=3, alpha=2, 
        days=31, timeDelay=5)
        self.sdetails = self.test.run()
    
    def generateCSV(self):
        df = self.test.toDataFrame()
        df.to_csv("HubSIRV.csv", index=False)
    
    def checkOutput(self):
        df = self.test.toDataFrame()
        df2 = pd.read_csv("HubSIRV.csv")
        assert df.equals(df2)
        print("Output test passed")
    
    def checkSimulInputs(self):
        # checks for invalid person inputs
        self.assertRaises(e.NotIntException, self.sdetails.personHistory, 100.0)
        self.assertRaises(e.PersonNotFound, self.sdetails.personHistory, 1000)
        # checks for exceptions when inputting days
        self.assertRaises(e.DayOutOfRange, self.sdetails.transmissionHistoryOnDay, 65)
        self.assertRaises(e.DayOutOfRange, self.sdetails.transmissionHistoryOnDay, -1)
        self.assertRaises(e.NotIntException, self.sdetails.transmissionHistoryOnDay, 25.0)
        print("Simul_Details input test passed: throws error for invalid inputs")
    
    def checkInput(self):
        # check int exception
        self.assertRaises(e.NotIntException, HubSIRV, 999.0, 1, 0, 0, .23, .2, .03, 3, 25, 31, 2, 1.0, 6**0.5, 1)
        self.assertRaises(e.NotIntException, HubSIRV, 999, 1.0, 0, 0, .23, .2, .03, 3, 25, 31, 2, 1.0, 6**0.5, 1)
        self.assertRaises(e.NotIntException, HubSIRV, 999, 1, 0.0, 0, .23, .2, .03, 3, 25, 31, 2, 1.0, 6**0.5, 1)
        self.assertRaises(e.NotIntException, HubSIRV, 999, 1, 0, 0.0, .23, .2, .03, 3, 25, 31, 2, 1.0, 6**0.5, 1)
        self.assertRaises(e.NotIntException, HubSIRV, 999, 1, 0, 0, .23, .2, .03, 3, 25, 31.0, 2, 1.0, 6**0.5, 1)
        # check flaot exception
        self.assertRaises(e.NotFloatException, HubSIRV, 999, 1, 0, 0, '.23', .2, .03, 3, 25, 31, 2, 1.0, 6**0.5, 1)
        self.assertRaises(e.NotFloatException, HubSIRV, 999, 1, 0, 0, .23, .2, .03, 3, 25, 31, 2, 1.0, 6**0.5, '1')
        self.assertRaises(e.NotFloatException, HubSIRV, 999, 1, 0, 0, .23, .2, .03, 3, 25, 31, 2, 1.0, True, 1)
        self.assertRaises(e.NotFloatException, HubSIRV, 999, 1, 0, 0, .23, .2, .03, 3, 25, 31, 2, '1.0', 6**0.5, 1)
        # check negative values
        self.assertRaises(e.NegativeValException, HubSIRV, -999, 1, 0, 0, .23, .2, .03, 3, 25, 31, 2, 1.0, 6**0.5, 1)
        self.assertRaises(e.NegativeValException, HubSIRV, 999, 1, 0, 0, -.23, .2, .03, 3, 25, 31, 2, 1.0, 6**0.5, 1)
        self.assertRaises(e.NegativeValException, HubSIRV, 999, 1, 0, 0, .23, .2, .03, 3, 25, 31, 2, 1.0, -6**0.5, 1)
        self.assertRaises(e.NegativeValException, HubSIRV, 999, 1, 0, 0, .23, .2, .03, 3, -25, 31, 2, 1.0, 6**0.5, 1)
        # check probability exceptions
        self.assertRaises(e.ProbabilityException, HubSIRV, 999, 1, 0, 0, 1.23, .2, .03, 3, 25, 31, 2, 1.0, 6**0.5, 1)
        self.assertRaises(e.ProbabilityException, HubSIRV, 999, 1, 0, 0, .23, 1.2, .03, 3, 25, 31, 2, 1.0, 6**0.5, 1)
        self.assertRaises(e.ProbabilityException, HubSIRV, 999, 1, 0, 0, .23, .2, 1.03, 3, 25, 31, 2, 1.0, 6**0.5, 1)
        self.assertRaises(e.ProbabilityException, HubSIRV, 999, 1, 0, 0, .23, .2, .03, 3, 25, 31, 2, 1.00001, 6**0.5, 1)
        print("Input test passed")


if __name__ == '__main__':
    a = Test_HubSIRV()
    #a.generateCSV()
    a.checkOutput()
    a.checkSimulInputs()
    a.checkInput()


        








