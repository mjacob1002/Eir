import multiprocessing as mp
from multipledispatch import dispatch
import numpy as np
import matplotlib.pyplot as plt
from src.utility import randEvent
 

print("Running DTMC Test. Please Fucking Work")

class DTMC:
    @dispatch(int, int, int)
    def __init__(self, S0, I0, days:int):
        self.S0 = S0
        self.I0 = I0
        self.days = days
        self.numSims = int(days + 1)
        self.S, self.I = np.zeros(self.numSims), np.zeros(self.numSims)
        self.S[0], self.I[0] = S0, I0
        
