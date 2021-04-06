import numpy as np
import pandas as pd
import unittest

from Eir.Deterministic.SEIR import SEIR
import Eir.exceptions as e

class Test_SEIR(unittest.TestCase):

    def __init__(self):
        self.test = SEIR(1.5, .2, .15, 999999, 0, 1, 0)
        self.result = self.test.run(31, .1, plot=False)
        
    
    def checkOutput(self):
        df = pd.read_csv("SEIR.csv")
        #print(df)
        #print(self.result)
        pd.testing.assert_frame_equal(self.result, df)
        accum = self.test.accumulate(31, .1, False)
        df2 = pd.read_csv("SEIR_a.csv")
        pd.testing.assert_frame_equal(accum, df2)
        print("Output test passed")

    def generateCSV(self):
        self.test.run(31, .1, plot=False).to_csv("SEIR.csv", index=False)
        self.test.accumulate(31, .1, plot=False).to_csv("SEIR_a.csv", index=False)
    
    def checkInput(self):
        self.assertRaises(e.NotFloatException, self.test.run, '31', .1, False)
        self.assertRaises(e.NotFloatException, self.test.run, 31, ".1", False)
        self.assertRaises(e.NegativeValException, self.test.run, -31, 1, False)
        self.assertRaises(e.NegativeValException, self.test.run, 31, -1, False)
        self.assertRaises(e.NotFloatException, self.test.accumulate, '31', .1, False)
        self.assertRaises(e.NotFloatException, self.test.accumulate, 31, ".1", False)
        self.assertRaises(e.NegativeValException, self.test.accumulate, -31, 1, False)
        self.assertRaises(e.NegativeValException, self.test.accumulate, 31, -1, False)
        print("Input test passed")
    

if __name__ == '__main__':
    a = Test_SEIR()
    #a.generateCSV()
    a.checkOutput()
    a.checkInput()

    
