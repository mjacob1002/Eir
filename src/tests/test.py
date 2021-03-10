import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Deterministic.SIR import SIR
from Deterministic.SIRV import SIRV
import multiprocessing as mp

#x = SIR(1.5, 1.0, 999, 1, 0)
#y = x.accumulate(30, .1, plot=False)
#print(y.head())
#z = x.normalizeDataFrame(y)
#print(z.head())

x = SIRV(1.5, 1, .01, 99, 1, 0, 0)
y = x.run(91, .1)
print(y[0].head())