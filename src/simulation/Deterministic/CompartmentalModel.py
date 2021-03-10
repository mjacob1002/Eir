import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from multipledispatch import dispatch


# sources:
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5348083/


# this is an abstract class that should never be instantiated
class CompartmentalModel:
    def __init__(self, S0, I0):
        assert S0 >= 0
        assert I0 >= 0
        self.S0 = S0
        self.I0 = I0

    @dispatch()
    def _deriv(self):
        pass

    @dispatch(float)
    # runs the Euler's Method
    def _update(self, dt: float):
        pass

    # creates the arrays & starting items, then calls _update() to run Euler's Method
    # then returns the completed arrays
    def _simulate(self, days: int, dt: float):
        pass

    @dispatch(int, float, bool)
    def run(self, days: int, dt: float, plot=True):
        pass



