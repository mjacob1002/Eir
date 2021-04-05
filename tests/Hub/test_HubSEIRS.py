import numpy as np
import pandas as pd
import unittest

from Eir.DTMC.spatialModel.Hub.HubSEIRS import HubSEIRS
import Eir.exceptions as e
# keep this seed when running test so that outputs can be checked
np.random.seed(83636)

class Test_HubSEIRS(unittest.TestCase):
    
    def __init__(self):
        self.test = HubSEIRS(S0=999, E0=1, I0=1, R0=0, pss=.23, rho=.2, gamma=.15, kappa=.2, side=25, rstart=3, days=31, w0=.73, alpha=2)
        self.sdetails = self.test.run()
    
    def generateCSV(self):
        """ How CSV was generated in order to ensure reproducibility."""
        df = self.test.toDataFrame()
        df.to_csv("HubSEIRS.csv", index=False)
    
    def checkOutputs(self):
        df = self.test.toDataFrame()
        df2 = pd.read_csv("HubSEIRS.csv")
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
    
    def checkInput(self):
        # checks for int exception
        self.assertRaises(e.NotIntException, HubSEIRS, 999.0, 1, 1, 0, .23, .2, .15, .2, 25, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.NotIntException, HubSEIRS, 999, 1.0, 1, 0, .23, .2, .15, .2, 25, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.NotIntException, HubSEIRS, 999, 1, 1.0, 0, .23, .2, .15, .2, 25, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.NotIntException, HubSEIRS, 999, 1, 1, 0.0, .23, .2, .15, .2, 25, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.NotIntException, HubSEIRS, 999, 1, 1, 0, .23, .2, .15, .2, 25, 3, 31.0, 1.0, 6**0.5, 2)
        # checks for not float exception
        self.assertRaises(e.NotFloatException, HubSEIRS, 999, 1, 1, 0, '.23', .2, .15, .2, 25, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.NotFloatException, HubSEIRS, 999, 1, 1, 0, .23, True, .15, .2, 25, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.NotFloatException, HubSEIRS, 999, 1, 1, 0, .23, .2, 'apples', .2, 25, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.NotFloatException, HubSEIRS, 999, 1, 1, 0, .23, .2, .15, .2, False, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.NotFloatException, HubSEIRS, 999, 1, 1, 0, .23, .2, .15, .2, 25, '0', 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.NotFloatException, HubSEIRS, 999, 1, 1, 0, .23, .2, .15, .2, 25, 3, 31, 1.0, True, 2)
        self.assertRaises(e.NotFloatException, HubSEIRS, 999, 1, 1, 0, .23, .2, .15, .2, 25, 3, 31, 1.0, 6**0.5, '2')
        self.assertRaises(e.NotFloatException, HubSEIRS, 999, 1, 1, 0, .23, .2, .15, '.2', 25, 3, 31, 1.0, 6**0.5, 2)
        # checks for negative values
        self.assertRaises(e.NegativeValException, HubSEIRS, -999, 1, 1, 0, .23, .2, .15, .2, 25, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.NegativeValException, HubSEIRS, 999, -1, 1, 0, .23, .2, .15, .2, 25, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.NegativeValException, HubSEIRS, 999, 1, -1, 0, .23, .2, .15, .2, 25, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.NegativeValException, HubSEIRS, 999, 1, 1, 0, -.23, .2, .15, .2, 25, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.NegativeValException, HubSEIRS, 999, 1, 1, 0, .23, -.2, .15, .2, 25, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.NegativeValException, HubSEIRS, 999, 1, 1, 0, .23, .2, -.15, .2, 25, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.NegativeValException, HubSEIRS, 999, 1, 1, 0, .23, .2, .15, .2, -25, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.NegativeValException, HubSEIRS, 999, 1, 1, 0, .23, .2, -.15, .2, 25, 3, 31, 1.0, -6**0.5, 2)
        self.assertRaises(e.NegativeValException, HubSEIRS, 999, 1, 1, 0, .23, .2, .15, .2, 25, 3, 31, -1.0, 6**0.5, 2)
        self.assertRaises(e.NegativeValException, HubSEIRS, 999, 1, 1, 0, .23, .2, .15, -.2, 25, 3, 31, 1.0, 6**0.5, 2)
        # checks probability
        self.assertRaises(e.ProbabilityException, HubSEIRS, 999, 1, 1, 0, .23, .2, 1.15, .2, 25, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.ProbabilityException, HubSEIRS, 999, 1, 1, 0, .23, 1.2, .15, .2, 25, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.ProbabilityException, HubSEIRS, 999, 1, 1, 0, 1.23, .2, .15, .2, 25, 3, 31, 1.0, 6**0.5, 2)
        self.assertRaises(e.ProbabilityException, HubSEIRS, 999, 1, 1, 0, .23, .2, .15, .2, 25, 3, 31, 1.1, 6**0.5, 2)
        self.assertRaises(e.ProbabilityException, HubSEIRS, 999, 1, 1, 0, .23, .2, .15, 1.2, 25, 3, 31, 1.0, 6**0.5, 2)
        print("Input Test Passed")



if __name__ == '__main__':
    a = Test_HubSEIRS()
    #a.generateCSV()
    a.checkOutputs()
    a.checkSimulInputs()
    a.checkInput()
