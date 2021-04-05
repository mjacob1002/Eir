import numpy as np
import pandas as pd
import unittest

from Eir.DTMC.spatialModel.randomMovement.randMoveSEIRSD import RandMoveSEIRSD
import Eir.exceptions as e


np.random.seed(35235)

class Test_RandMoveSEIRSD(unittest.TestCase):

    def __init__(self):
        self.test = RandMoveSEIRSD(999, 0, 2, 0, .25, .3, .05, .15, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.sdetails = self.test.run()
    
    def generateCSV(self):
        df = self.test.toDataFrame()
        df.to_csv("randMoveSEIRSD.csv", index=False)
    
    def checkOutput(self):
        df = self.test.toDataFrame()
        df2 = pd.read_csv("randMoveSEIRSD.csv")
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
        self.assertRaises(e.NotIntException, RandMoveSEIRSD, 999.0, 0, 1, 0, .25, .3, .05, .2, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NotIntException, RandMoveSEIRSD, 999, 0, 1.0, 0, .25, .3, .05, .2, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NotIntException, RandMoveSEIRSD, 999, 0, 1, 0, .25, .3, .05, .2, 25, 3, .3, 1, .25, 31.0, 1.0, 2.0)
        # float check
        self.assertRaises(e.NotFloatException, RandMoveSEIRSD, 999, 0, 1, 0, ".25", .3, .05, .2, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NotFloatException, RandMoveSEIRSD, 999, 0, 1, 0, .25, '.3', .05, .2, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NotFloatException, RandMoveSEIRSD, 999, 0, 1, 0, .25, .3, .05, .2, "25", 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NotFloatException, RandMoveSEIRSD, 999, 0, 1, 0, .25, .3, .05, .2, 25, "3", .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NotFloatException, RandMoveSEIRSD, 999, 0, 1, 0, .25, .3, .05, .2, 25, 3, True, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NotFloatException, RandMoveSEIRSD, 999, 0, 1, 0, .25, .3, .05, .2, 25, 3, .3, 1, .25, 31, False, 2.0)
        self.assertRaises(e.NotFloatException, RandMoveSEIRSD, 999, 0, 1, 0, .25, .3, .05, '.2', 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NotFloatException, RandMoveSEIRSD, 999, 0, 1, 0, .25, .3, ".05", .2, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        # negvalue check
        self.assertRaises(e.NegativeValException, RandMoveSEIRSD, 999, 0, 1, 0, -.25, .3, .05, .2, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NegativeValException, RandMoveSEIRSD, -999, 0, 1, 0, .25, .3, .05, .2, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NegativeValException, RandMoveSEIRSD, 999, 0, -1, 0, .25, .3, .05, .2, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NegativeValException, RandMoveSEIRSD, 999, 1, 0, 0, .25, -.3, .05, .2, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NegativeValException, RandMoveSEIRSD, 999, 1, 0, 0, .25, .3, .05, .2, -25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NegativeValException, RandMoveSEIRSD, 999, 1, 0, 0, .25, .3, .05, .2, 25, -3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NegativeValException, RandMoveSEIRSD, 999, 1, -1, 0, .25, .3, .05, .2, 25, -3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NegativeValException, RandMoveSEIRSD, 999, 1, 1, 0, .25, .3, .05, -.2, 25, -3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.NegativeValException, RandMoveSEIRSD, 999, 1, 1, 0, .25, .3, -.05, .2, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        # probability check
        self.assertRaises(e.ProbabilityException, RandMoveSEIRSD, 999, 1, 0, 0, .25, .3, .05, .2, 25, 3, .3, 1, .25, 31, 1.01, 2.0)
        self.assertRaises(e.ProbabilityException, RandMoveSEIRSD, 999, 1, 0, 0, .25, 1.3, .05, .2, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.ProbabilityException, RandMoveSEIRSD, 999, 1, 1, 0, 1.25, .3, .05, .2, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.ProbabilityException, RandMoveSEIRSD, 999, 1, 1, 0, .25, .3, .05, 1.2, 25, 3, .3, 1, .25, 31, 1.0, 2.0)
        self.assertRaises(e.ProbabilityException, RandMoveSEIRSD, 999, 1, 1, 0, .25, .3, 1.05, .2, 25, 3, .3, 1, .25, 31, 1.0, 2.0)

        print("Input Test passed")

if __name__ == '__main__':
    a = Test_RandMoveSEIRSD()
    #a.generateCSV()
    a.checkOutput()
    a.checkSimulInputs()
    a.checkInputs()