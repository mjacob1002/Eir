from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
# file purely used for testing code by running this file in the terminal
from src.DTMC.spatialModel.Hub.HubSIRS import HubSIRS
from src.DTMC.spatialModel.randomMovement.randMoveSIS import RandMoveSIS
from src.DTMC.spatialModel.Hub.HubSIR import HubSIR
from src.DTMC.spatialModel.Hub.HubSEIR import HubSEIR
from src.DTMC.spatialModel.StrongInfectious.StrongInfSIR import StrongInfSIR
def main():
    test = HubSIS(1000, .17, 4, 2, 25, 999, 1, 31, .3)
    details = test.run()
    test.plot()
    ddf = details.personHistory(5)
    print(ddf)
    #print(test.toDataFrame())

def testHistogram():
    test = HubSIS(1000, .17, 4, 2, 100, 999, 1, 31, .3)
    details = test.run()
    bin = range(0, 600, 25)
    details.plotTransmissions(bins=bin)

def testRandMoveSIS():
    S0 = 999
    I0 = 1
    gamma = 0.6
    plane = 10
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSIS(S0=S0, I0=I0, gamma=gamma, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r,
    days=days)
    details = test.run()
    dic = details.sortedTransmissions()
    print(dic)


def getHubSIRS():
    test = HubSIRS(popsize=1000, pss=.2, rstart=3, alpha=2, side=25, S0=999, I0=1, R0=0, days=31, gamma=.4, kappa= .2, w0=.7)
    d = test.run()
    print(d.personHistory(652))
    test.plot()
    df = test.toDataFrame()
    print(df)

def getStrongInfSIR():
    test = StrongInfSIR(popsize=1000, pss=.2, rstart=4, alpha=2, side=50, S0=999, I0=1, R0=0, days=31, gamma=.4)
    d = test.run()
    print(d.personHistory(999))
    test.plot()
    df = test.toDataFrame()
    print(df)

def getHubSEIR():
    test = HubSEIR(S0=999, I0=1, R0=0, pss=.17, rho=.3, gamma=.23, side=25, rstart=3, alpha=2, 
    days=31)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())

def getHubSIR():
    test = HubSIR(popsize=1000, pss=.2, rstart=3, alpha=2, side=45, S0=999, I0=1, R0=0, days=31, gamma=.4, w0=.7)
    d = test.run()
    print(d.personHistory(652))
    test.plot()
    df = test.toDataFrame()
    print(df)
    
if  __name__ == '__main__':
    getHubSIR()

