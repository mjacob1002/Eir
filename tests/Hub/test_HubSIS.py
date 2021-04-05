import sys
import os
import numpy as np
import pandas as pd
import unittest

from Eir.DTMC.spatialModel.Hub.HubSIS import HubSIS
import Eir.exceptions as e

np.random.seed(0)

class Test_Hub_SIS(unittest.TestCase):

    def __init__(self):
        self.test = HubSIS(S0=999, I0=1, pss=.2, rstart=3, side=25, days=31, gamma=.3)
        self.sdetails = self.test.run()
    
    def checkOutputs(self):
        df = self.test.toDataFrame()
        df2 = pd.read_csv("Hub_SIS.csv")
        assert df.equals(df2)
        print("Output Test Passed")
    
    def checkSimulInputs(self):
        # checks for invalid person inputs
        self.assertRaises(e.NotIntException, self.sdetails.personHistory, 100.0)
        self.assertRaises(e.PersonNotFound, self.sdetails.personHistory, 1000)
        # checks for exceptions when inputting days
        self.assertRaises(e.DayOutOfRange, self.sdetails.transmissionHistoryOnDay, 65)
        self.assertRaises(e.DayOutOfRange, self.sdetails.transmissionHistoryOnDay, -1)
        self.assertRaises(e.NotIntException, self.sdetails.transmissionHistoryOnDay, 25.0)
        print("Simul_Details input test passed: throws error for invalid inputs")
    
    def checkInputs(self):
        self.assertRaises(e.NotIntException, HubSIS, 999.0, 1, .2, 3, 25, 31, .3)
        self.assertRaises(e.NotIntException, HubSIS, 999, 1.0, .2, 3, 25, 31, .3)
        self.assertRaises(e.NotIntException, HubSIS, 999, 1, .2, 3, 25, 31.0, .3)
        self.assertRaises(e.NotFloatException, HubSIS, 99, 1, ".2", 3, 25, 31, .3)
        self.assertRaises(e.NegativeValException, HubSIS, 999, -1, .2, 3, 25, 31, .3)
        self.assertRaises(e.NegativeValException, HubSIS, 999, 1, .2, 3, 25, 31, -.3)
        self.assertRaises(e.ProbabilityException, HubSIS, 99, 1, 1.2, 3, 25, 31, .3)
        self.assertRaises(e.ProbabilityException, HubSIS, 99, 1, .2, 3, 25, 31, 1.3)
        print("Input Test Passed")

    
    def generateCSV(self):
        df = self.test.toDataFrame()
        df.to_csv("Hub_SIS.csv", index=False)


if __name__ == '__main__':
    test = Test_Hub_SIS()
    test.checkOutputs()
    test.checkSimulInputs()
    test.checkInputs()
    