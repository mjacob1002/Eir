import numpy as np
import pandas as pd
import unittest

from Eir.DTMC.spatialModel.PeriodicMovement.periodicSIRD import PeriodicSIRD
import Eir.exceptions as e

np.random.seed(347446)

class Test_PeriodicSIRD(unittest.TestCase):

    def __init__(self):
        self.test = PeriodicSIRD(999, 1, 0, .25, .05, 25, 3, .5, 1, .2, 31, 1.0, 2.0)
        self.sdetails = self.test.run()

    def generateCSV(self):
        self.test.toDataFrame().to_csv('PeriodicSIRD.csv', index=False)
    
    def checkOutput(self):
        df = self.test.toDataFrame()
        df2 = pd.read_csv('PeriodicSIRD.csv')
        assert df.equals(df2)
        print("Output test passed")
    
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
        # int check
        self.assertRaises(e.NotIntException, PeriodicSIRD, 999.0, 1, 0, .3, .05, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NotIntException, PeriodicSIRD, 999, 1.0, 0, .3, .05, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NotIntException, PeriodicSIRD, 999, 1, 0, .3, .05, 25, 3, .3, 1, .25, 31.0, 1.0, 2.0)
        # float check
        self.assertRaises(e.NotFloatException, PeriodicSIRD, 999, 1, 0, '.3', .05, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NotFloatException, PeriodicSIRD, 999, 1, 0, .3, .05, "25", 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NotFloatException, PeriodicSIRD, 999, 1, 0, .3, .05, 25, "3", .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NotFloatException, PeriodicSIRD, 999, 1, 0, .3, .05, 25, 3, True, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NotFloatException, PeriodicSIRD, 999, 1, 0, .3, .05, 25, 3, .3, 1, .25, 31, False, 2.0)
        self.assertRaises(e.NotFloatException, PeriodicSIRD, 999, 1, 0, .3, '1.05', 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NotFloatException, PeriodicSIRD, 999, 1, 0, .3, '1.05', 25, 3, .3, 1, .25, 31, 1.0, 2.0, True)
        self.assertRaises(e.NotFloatException, PeriodicSIRD, 999, 1, 0, .3, '1.05', 25, 3, .3, 1, .25, 31, 1.0, 2.0, 6, False)
        # negvalue check
        self.assertRaises(e.NegativeValException, PeriodicSIRD, -999, 1, 0, .05, .3, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NegativeValException, PeriodicSIRD, 999, -1, 0, .3, .05, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NegativeValException, PeriodicSIRD, 999, 1, 0, -.3, .05, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NegativeValException, PeriodicSIRD, 999, 1, 0, .3, .05, -25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NegativeValException, PeriodicSIRD, 999, 1, 0, .3, .05, 25, -3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NegativeValException, PeriodicSIRD, 999, 1, -1, .3, .05, 25, -3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NegativeValException, PeriodicSIRD, 999, 1, 0, .3, -.13, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        # probability check
        self.assertRaises(e.ProbabilityException, PeriodicSIRD, 999, 1, 0, .3, .05, 25, 3, .3, 1, .25, 31, 1.01, 2.0)
        self.assertRaises(e.ProbabilityException, PeriodicSIRD, 999, 1, 0, 1.3, .05, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.ProbabilityException, PeriodicSIRD, 999, 1, 0, .3, 1.05, 25, 3, .3, 1, .25, 31, 1.0, 2.0)

        print("Input Test passed")
    


if __name__ == '__main__':
    a = Test_PeriodicSIRD()
    #a.generateCSV()
    a.checkOutput()
    a.checkSimulInputs()
    a.checkInputs()