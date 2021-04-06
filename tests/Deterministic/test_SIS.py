import unittest
import numpy as np
import pandas as pd

from Eir.Deterministic.SIS import SIS
import Eir.exceptions as e

class Test_SIS(unittest.TestCase):

    def __init__(self):
        self.test = SIS(1.5, .3, 999999, 1)
        self.result = self.test.run(31, .1, plot=False)
    
    def generateCSV(self):
        self.test.run(31, .1, plot=False).to_csv("SIS.csv", index=False)
        self.test.accumulate(31, .1, plot=False).to_csv("SIS_a.csv", index=False)
    
    def checkOutput(self):
        df = pd.read_csv('SIS.csv')
        pd.testing.assert_frame_equal(df, self.result)
        print("Output test passed")
    
    #def checkInput(self):
    #    self.assertRaises(e.NotFloatException, self.test.run, '31', .1, False)
    #    self.assertRaises(e.NotFloatException, self.test.run, 31, ".1", False)
    #    self.assertRaises(e.NegativeValException, self.test.run, -31, 1, False)
    #    self.assertRaises(e.NegativeValException, self.test.run, 31, -1, False)
    #    self.assertRaises(e.NotFloatException, self.test.accumulate, '31', .1, False)
    #    self.assertRaises(e.NotFloatException, self.test.accumulate, 31, ".1", False)
    #    self.assertRaises(e.NegativeValException, self.test.accumulate, -31, 1, False)
    #    self.assertRaises(e.NegativeValException, self.test.accumulate, 31, -1, False)
    #    print("Input test passed")

if __name__ == '__main__':
    a = Test_SIS()
    #a.generateCSV()
    a.checkOutput()
    #a.checkInput()