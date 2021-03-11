from src.simulation.utility import randEvent
import multiprocessing as mp
from multipledispatch import dispatch
import numpy as np
import matplotlib.pyplot as plt


class DTMC:
    @dispatch(int, int, int, float)
    def __init__(self, S0, I0, days:int, dt: float):
        self.S0 = S0
        self.I0 = I0
        self.days = days
        self.dt = dt
        self.numSims = int(days / dt + 1)
        self.S, self.I = np.zeros(self.numSims), np.zeros(self.numSims)
        self.S[0], self.I[0] = S0, I0
