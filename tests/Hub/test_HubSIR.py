import unittest
import numpy as np
import pandas as pd

from Eir.DTMC.spatialModel.Hub.HubSIR import HubSIR
import Eir.exceptions as e 

# seed the RNG for reproducible results
np.random.seed(0)

class Test_HubSIR(unittest.TestCase):

    def __init__(self):
        self.test = HubSIR(S0=999, I0=1, R0=1, pss=.2, rstart=3, alpha=2, side=25,days=31, gamma=.2, w0=1.0)
        self.sdetails = self.test.run()
    
    def generateCSV(self):
        """ How CSV was generated in order to ensure reproducibility."""
        df = self.test.toDataFrame()
        df.to_csv("HubSIR.csv", index=False)
    
    def checkOutputs(self):
        df = self.test.toDataFrame()
        df2 = pd.read_csv("HubSIR.csv")
        assert df.equals(df2)
        print("Outputs test passed")
    
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
        self.assertRaises(e.NotIntException, HubSIR, 999.0, 1, 1, .2, 3, 2, 25, 31, .2, 1.0)
        self.assertRaises(e.NotIntException, HubSIR, 999, 1, 1.0, .2, 3, 2, 25, 31, .2, 1.0)
        self.assertRaises(e.NotIntException, HubSIR, 999, 1.0, 1, .2, 3, 2, 25, 31, .2, 1.0)
        self.assertRaises(e.NotIntException, HubSIR, 999, 1.0, 1, .2, 3, 2, 25, 31.0, .2, 1.0)
        self.assertRaises(e.NotFloatException, HubSIR, 999, 1, 1, '.2', 3, 2, 25, 31, .2, 1.0)
        self.assertRaises(e.NotFloatException, HubSIR, 999, 1, 1, .2, 3, True, 2, 31, .2, 1.0)
        self.assertRaises(e.NotFloatException, HubSIR, 999, 1, 1, .2, 3, 2, 25, 31, .2, False)
        self.assertRaises(e.NegativeValException, HubSIR, 999, 1, 1, .2, 3, 2, -25, 31, .2, 1.0)
        self.assertRaises(e.NegativeValException, HubSIR, 999, 1, 1, .2, 3, 2, 25, 31, -.2, 1.0)
        self.assertRaises(e.ProbabilityException, HubSIR, 999, 1, 1, .2, 3, 2, 25, 31, .2, 1.01)
        self.assertRaises(e.ProbabilityException, HubSIR, 999, 1, 1, 1.2, 3, 2, 25, 31, .2, 1.0)
        self.assertRaises(e.ProbabilityException, HubSIR, 999, 1, 1, .2, 3, 2, 25, 31, 1.2, 1.0)
        print("Inputs Test Passed")


if __name__ == '__main__':
    test = Test_HubSIR()
    #test.generateCSV()
    test.checkOutputs()
    test.checkSimulInputs()
    test.checkInputs()