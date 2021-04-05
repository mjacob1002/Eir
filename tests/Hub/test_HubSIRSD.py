import numpy as np
import pandas as pd
import unittest

from Eir.DTMC.spatialModel.Hub.HubSIRSD import HubSIRSD
import Eir.exceptions as e


np.random.seed(0)


class Test_HubSIRSD(unittest.TestCase):

    def __init__(self):
        self.test = HubSIRSD(S0=999, I0=1, R0=0, pss=.17, gamma=.23, kappa=.2, mu=.05,side=25, rstart=3, alpha=2, 
        days=31)
        self.sdetails = self.test.run()
    
    def generateCSV(self):
        df = self.test.toDataFrame()
        df.to_csv("HubSIRSD.csv", index=False)
    
    def checkOutput(self):
        df = self.test.toDataFrame()
        df2 = pd.read_csv("HubSIRSD.csv")
        assert df.equals(df2)
        print("Output test passed")
    
    def checkSimulDetails(self):
        # checks for invalid person inputs
        self.assertRaises(e.NotIntException, self.sdetails.personHistory, 100.0)
        self.assertRaises(e.PersonNotFound, self.sdetails.personHistory, 1001)
        # checks for exceptions when inputting days
        self.assertRaises(e.DayOutOfRange, self.sdetails.transmissionHistoryOnDay, 65)
        self.assertRaises(e.DayOutOfRange, self.sdetails.transmissionHistoryOnDay, -1)
        self.assertRaises(e.NotIntException, self.sdetails.transmissionHistoryOnDay, 25.0)
        print("Simul_Details input test passed: throws error for invalid inputs")
    
    def checkInput(self):
        # Refer to HubSIRSD for the order of parameter sof HubSIRSD constructor
        # testing int inputs
        self.assertRaises(e.NotIntException, HubSIRSD, 999.0, 1, 0, .17, 3, 25, 31, .23, .2, .05, 2, 1.0, 6**0.5)
        self.assertRaises(e.NotIntException, HubSIRSD, 999, 1.0, 0, .17, 3, 25, 31, .23, .2, .05, 2, 1.0, 6**0.5)
        self.assertRaises(e.NotIntException, HubSIRSD, 999, 1, 0.0, .17, 3, 25, 31, .23, .2, .05, 2, 1.0, 6**0.5)
        self.assertRaises(e.NotIntException, HubSIRSD, 999, 1, 0, .17, 3, 25, 31.0, .23, .2, .05, 2, 1.0, 6**0.5)
        # testing float outputs
        self.assertRaises(e.NotFloatException, HubSIRSD, 999, 1, 0, True, 3, 25, 31, .23, .2, .05, 2, 1.0, 6**0.5)
        self.assertRaises(e.NotFloatException, HubSIRSD, 999, 1, 0, .17, 3, 25, 31, False, .2, .05, 2, 1.0, 6**0.5)
        self.assertRaises(e.NotFloatException, HubSIRSD, 999, 1, 0, .17, 3, 25, 31, .23, 'apples', .05, 2, 1.0, 6**0.5)
        # testing NegativeValues
        self.assertRaises(e.NegativeValException, HubSIRSD, -999, 1, 0, .17, 3, 25, 31, .23, .2, .05, 2, 1.0, 6**0.5)
        self.assertRaises(e.NegativeValException, HubSIRSD, 999, 1, 0, .17, 3, 25, 31, .23, .2, -.05, 2, 1.0, 6**0.5)
        self.assertRaises(e.NegativeValException, HubSIRSD, 999, 1, 0, .17, 3, 25, 31, .23, .2, .05, 2, 1.0, -6**0.5)
        self.assertRaises(e.NegativeValException, HubSIRSD, 999, 1, 0, .17, 3, 25, 31, .23, -.2, .05, 2, 1.0, -6**0.5)
        # testing probabilities
        self.assertRaises(e.ProbabilityException, HubSIRSD, 999, 1, 0, .17, 3, 25, 31, .23, .2, .05, 2, 1.25, 6**0.5)
        self.assertRaises(e.ProbabilityException, HubSIRSD, 999, 1, 0, .17, 3, 25, 31, 1.23, .2, .05, 2, 1.0, 6**0.5)
        self.assertRaises(e.ProbabilityException, HubSIRSD, 999, 1, 0, .17, 3, 25, 31, 1.23, 1.2, .05, 2, 1.0, 6**0.5)
        print("Input test passed")


if __name__ == "__main__":
    a = Test_HubSIRSD()
    #a.generateCSV()
    a.checkOutput()
    a.checkSimulDetails()
    a.checkInput()