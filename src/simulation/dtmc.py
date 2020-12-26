from utility import randEvent
import multiprocessing as mp
from multipledispatch import dispatch
import numpy as np
import matplotlib.pyplot as plt


class DTMC:
    def __init__(self, S0, I0):
        self.S0 = S0
        self.I0 = I0
