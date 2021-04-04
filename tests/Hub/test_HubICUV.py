import sys
import os
import numpy as np
import pandas as pd
import unittest


from src.DTMC.spatialModel.Hub.Hub_ICUV import Hub_ICUV
import src.exceptions as e
# seed the RNG for reproducibility. Seed it to 0
np.random.seed(0)


class Test_Hub_ICUV(unittest.TestCase):

    def __init__(self):
        # the test object that will be used for verifying reproducibility; not used for checking for errors
        self.test = Hub_ICUV(S0=999, E0=0, I0=1, R0=0, V0=0, rho=.3, ioda=.3, gamma=.25, mu=0.007, omega=.14, phi = .42, chi=.15, kappa=.05, eta=.02, rstart=3, pss=.17, side=25, days=62)
        # run the simulation
        self.sdetails = self.test.run()
    
    def checkOutputs(self):
        """ Verifies that the output of the file is the same as anticipated by seeding np.random"""
        # convert the output of Hub_ICUV object as dataframe
        df = self.test.toDataFrame()
        # read the expected output csv file as a csv
        df2 = pd.read_csv("Hub_ICUV.csv")
        assert df.equals(df2)
        print("Test Outputs passed: outputs are as anticipated")
    
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
        # checks for input exceptions
        self.assertRaises(e.NotIntException, Hub_ICUV, 999, 0, 1, 0, 0, .3, .3, .25, 0.007, .14, .42, .15, .05, .02, 3, .17, 25, 62.0)
        self.assertRaises(e.NotIntException, Hub_ICUV, 999, 0, 1, 0, 0.0, .3, .3, .25, 0.007, .14, .42, .15, .05, .02, 3, .17, 25, 62)
        self.assertRaises(e.NotFloatException, Hub_ICUV, 999, 0, 1, 0, 0, .3, .3, '0.25', 0.007, .14, .42, .15, .05, .02, 3, .17, 25, 62)
        self.assertRaises(e.NegativeValException, Hub_ICUV, 999, 0, -1, 0, 0, .3, .3, 0.25, 0.007, .14, .42, .15, .05, .02, 3, .17, 25, 62)
        self.assertRaises(e.NegativeValException, Hub_ICUV, 999, 0, -1, 0, 0, .3, .3, 0.25, 0.007, .14, .42, .15, .05, .02, 3, .17, 25, -62)
        self.assertRaises(e.NegativeValException, Hub_ICUV, -999, 0, 1, 0, 0, .3, .3, 0.25, 0.007, .14, .42, .15, .05, .02, 3, .17, 25, 62)
        self.assertRaises(e.ProbabilityException, Hub_ICUV, 999, 0, 1, 0, 0, .3, .3, 0.25, 0.007, .14, 1.42, .15, .05, .02, 3, .17, 25, 62)
        print("Input Test Passed")
    
    #def generateCSV(self):
    #    df = self.test.toDataFrame()
    #    df.to_csv("Hub_ICUV.csv", index=False)
    

if __name__ == '__main__':

    print("Running Hub_ICUV Test")
    test = Test_Hub_ICUV()
    test.checkOutputs()
    test.checkSimulInputs()
    test.checkInputs()