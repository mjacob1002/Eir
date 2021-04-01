import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from .HubSIR import HubSIR
from src.utility import Person, randEvent

class HubSIRV(HubSIR):

    def __init__(self, popsize: int, S0: int, I0: int, R0:int, V0: int, gamma: float, eta:float, rstart: float, side: float, alpha=2, hubConstant=6**0.5):
        assert popsize == S0 + I0 + R0 + V0
        