import numpy as np
import pandas as pd
import unittest

from Eir.DTMC.spatialModel.PeriodicMovement.periodicICUV import PeriodicICUV
import Eir.exceptions as e

np.random.seed(68351937)

class Test_PeriodicICUV(unittest.TestCase):

    def __init__(self):
        self.test = PeriodicICUV(S0=999, E0=0, I0=1, R0=0, V0=0, rho=.3, ioda=.3, gamma=.25, mu=0.007, omega=.14, phi = .42, chi=.15, kappa=.05, eta=.02, spread_r=2, sigma_r=.25, move_R=4, sigma_R=.75, side=33, days=31, timeDelay=15)
        self.sdetails = self.test.run()
    
    def generateCSV(self):
        df = self.test.toDataFrame()
        df.to_csv("PeriodicICUV.csv", index=False)
    
    def checkOutput(self):
        df = self.test.toDataFrame()
        df2 = pd.read_csv("PeriodicICUV.csv")
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
    
    def checkInput(self):
        # int check
        self.assertRaises(e.NotIntException, PeriodicICUV, 999.0, 0, 1, 0, 0, .3, .3, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.NotIntException, PeriodicICUV, 999, 0.0, 1, 0, 0, .3, .3, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.NotIntException, PeriodicICUV, 999, 0, 1.0, 0, 0, .3, .3, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.NotIntException, PeriodicICUV, 999, 0, 1, 0.0, 0, .3, .3, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.NotIntException, PeriodicICUV, 999, 0, 1, 0, 0.0, .3, .3, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.NotIntException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31.0, 15)
        # float check
        self.assertRaises(e.NotFloatException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, False, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.NotFloatException, PeriodicICUV, 999, 0, 1, 0, 0, .3, True, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.NotFloatException, PeriodicICUV, 999, 0, 1, 0, 0, ".3", .3, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.NotFloatException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, .14, .42, .15, .05, .02, "2", .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.NotFloatException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, "33", 31, 15)
        self.assertRaises(e.NotFloatException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, ".007", .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.NotFloatException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, True, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.NotFloatException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, .14, ".42", .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.NotFloatException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, .14, .42, ".15", .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.NotFloatException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, .14, .42, .15, ".05", .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.NotFloatException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, .14, .42, .15, .05, ".02", 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.NotFloatException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, .14, .42, .15, .05, .02, 2, ".25", 4, .75, 33, 31, 15)
        self.assertRaises(e.NotFloatException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, True)
        self.assertRaises(e.NotFloatException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15, "32")
        self.assertRaises(e.NotFloatException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15, 5, "123")
        self.assertRaises(e.NotFloatException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, ".75", 33, 31, 15)
        self.assertRaises(e.NotFloatException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, .14, .42, .15, .05, .02, 2, .25, "4", .75, 33, 31, 15)
        # negative value check
        self.assertRaises(e.NegativeValException, PeriodicICUV, -999, 0, 1, 0, 0, .3, .3, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.NegativeValException, PeriodicICUV, 999, 0, -1, 0, 0, .3, .3, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.NegativeValException, PeriodicICUV, 999, 0, 1, -32, 0, .3, .3, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        # probability check
        self.assertRaises(e.ProbabilityException, PeriodicICUV, 999, 0, 1, 0, 0, 1.3, .3, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.ProbabilityException, PeriodicICUV, 999, 0, 1, 0, 0, .3, 1.3, .25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.ProbabilityException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, 1.25, .007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.ProbabilityException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, 1.007, .14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.ProbabilityException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, 1.14, .42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.ProbabilityException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, .14, 1.42, .15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.ProbabilityException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, .14, .42, 1.15, .05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.ProbabilityException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, .14, .42, .15, 1.05, .02, 2, .25, 4, .75, 33, 31, 15)
        self.assertRaises(e.ProbabilityException, PeriodicICUV, 999, 0, 1, 0, 0, .3, .3, .25, .007, .14, .42, .15, .05, 1.02, 2, .25, 4, .75, 33, 31, 15)
        print("Input Test Passed")

if __name__ == '__main__':
    a = Test_PeriodicICUV()
    #a.generateCSV()
    a.checkOutput()
    a.checkSimulInputs()
    a.checkInput()