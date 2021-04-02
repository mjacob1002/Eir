from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
# file purely used for testing code by running this file in the terminal
from src.DTMC.spatialModel.Hub.HubSIRS import HubSIRS
from src.DTMC.spatialModel.randomMovement.randMoveSIS import RandMoveSIS
from src.DTMC.spatialModel.randomMovement.randMoveSIR import RandMoveSIR
from src.DTMC.spatialModel.randomMovement.randMoveSIRS import RandMoveSIRS
from src.DTMC.spatialModel.Hub.HubSIR import HubSIR
from src.DTMC.spatialModel.Hub.HubSIRD import HubSIRD
from src.DTMC.spatialModel.Hub.HubSIRSD import HubSIRSD
from src.DTMC.spatialModel.Hub.HubSIRV import HubSIRV
from src.DTMC.spatialModel.Hub.HubSIRSV import HubSIRSV
from src.DTMC.spatialModel.Hub.HubSIRVD import HubSIRVD
from src.DTMC.spatialModel.Hub.HubSIRSVD import HubSIRSVD
from src.DTMC.spatialModel.Hub.HubSIS import HubSIS
from src.DTMC.spatialModel.Hub.HubSEIR import HubSEIR
from src.DTMC.spatialModel.Hub.HubSEIRS import HubSEIRS
from src.DTMC.spatialModel.Hub.HubSEIRV import HubSEIRV
from src.DTMC.spatialModel.Hub.HubSEIRSV import HubSEIRSV
from src.DTMC.spatialModel.Hub.HubSEIRD import HubSEIRD
from src.DTMC.spatialModel.Hub.HubSEIRSD import HubSEIRSD
from src.DTMC.spatialModel.Hub.HubSEIRSVD import HubSEIRSVD
from src.DTMC.spatialModel.Hub.HubSEIRVD import HubSEIRVD
from src.DTMC.spatialModel.Hub.Hub_ICUV import Hub_ICUV

from src.DTMC.spatialModel.StrongInfectious.StrongInfSIR import StrongInfSIR
from src.DTMC.spatialModel.StrongInfectious.StrongInf_ICUV import StrongInf_ICUV
from src.DTMC.spatialModel.StrongInfectious.StrongInfSEIRD import StrongInfSEIRD
from src.DTMC.spatialModel.StrongInfectious.StrongInfSEIR import StrongInfSEIR
from src.DTMC.spatialModel.StrongInfectious.StrongInfSIS import StrongInfSIS
from src.DTMC.spatialModel.StrongInfectious.StrongInfSIR import StrongInfSIR
from src.DTMC.spatialModel.StrongInfectious.StrongInfSEIRS import StrongInfSEIRS
from src.DTMC.spatialModel.StrongInfectious.StrongInfSEIRSD import StrongInfSEIRSD
from src.DTMC.spatialModel.StrongInfectious.StrongInfSEIRSV import StrongInfSEIRSV
from src.DTMC.spatialModel.StrongInfectious.StrongInfSEIRSVD import StrongInfSEIRSVD
from src.DTMC.spatialModel.StrongInfectious.StrongInfSEIRVD import StrongInfSEIRVD
from src.DTMC.spatialModel.StrongInfectious.StrongInfSEIRV import StrongInfSEIRV
from src.DTMC.spatialModel.StrongInfectious.StrongInfSIRD import StrongInfSIRD
from src.DTMC.spatialModel.StrongInfectious.StrongInfSIRSD import StrongInfSIRSD
from src.DTMC.spatialModel.StrongInfectious.StrongInfSIRSV import StrongInfSIRSV
from src.DTMC.spatialModel.StrongInfectious.StrongInfSIRSVD import StrongInfSIRSVD
from src.DTMC.spatialModel.StrongInfectious.StrongInfSIRV import StrongInfSIRV
from src.DTMC.spatialModel.StrongInfectious.StrongInfSIRVD import StrongInfSIRVD


from src.DTMC.spatialModel.randomMovement.randMoveSEIRS import RandMoveSEIRS
from src.DTMC.spatialModel.randomMovement.randMoveSIRV import RandMoveSIRV
from src.DTMC.spatialModel.randomMovement.randMoveSIRVS import RandMoveSIRVS
from src.DTMC.spatialModel.randomMovement.randMoveSEIRV import RandMoveSEIRV
from src.DTMC.spatialModel.randomMovement.randMoveSEIRVS import RandMoveSEIRVS
from src.DTMC.spatialModel.randomMovement.randMoveSIRD import RandMoveSIRD
from src.DTMC.spatialModel.randomMovement.randMoveSIRSD import RandMoveSIRSD
from src.DTMC.spatialModel.randomMovement.randMoveSIRDV import RandMoveSIRDV
from src.DTMC.spatialModel.randomMovement.randMoveSIRSDV import RandMoveSIRSDV
from src.DTMC.spatialModel.randomMovement.randMoveSEIRD import RandMoveSEIRD
from src.DTMC.spatialModel.randomMovement.randMoveSEIRSD import RandMoveSEIRSD
from src.DTMC.spatialModel.randomMovement.randMoveSEIRDV import RandMoveSEIRDV
from src.DTMC.spatialModel.randomMovement.randMoveSEIRSDV import RandMoveSEIRSDV

def getStrongInfSIS():
    S0 = 999
    I0 = 1
    rstart = 3
    side = 33
    days=31
    gamma = 0.3
    pss = .17
    test = StrongInfSIS(S0=S0, I0=I0, pss=pss, rstart=rstart, side=side, days=days, gamma=gamma)
    test.run()
    df = test.toDataFrame()
    print(df)


def testRandSEIRDV():
    S0 = 999
    E0 = 0
    I0 = 1
    rho = .2
    gamma = 0.4
    mu = .1
    eta=.03
    plane = 25
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSEIRDV(S0=S0, E0=E0, I0=I0, R0=0, V0=0, rho=rho, gamma=gamma, mu=mu, eta=eta, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r,
    days=days)
    details = test.run()
    df = test.toDataFrame()
    print(df)
    print("###########################")
    print(details.sortedTransmissions())
    print("######################")
    print(test.Scollect[999].r0)
    #print("#######################")
    #print(details.personHistory(686)
    #print("#######################")
    #print(details.personHistory(3))
    test.plot()

def testRandSEIRSDV():
    S0 = 999
    E0 = 0
    I0 = 1
    rho = .2
    gamma = 0.4
    mu = .1
    eta=.03
    kappa = .1
    plane = 25
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSEIRSDV(S0=S0, E0=E0, I0=I0, R0=0, V0=0, rho=rho, gamma=gamma, mu=mu, eta=eta, kappa=kappa, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r,
    days=days)
    details = test.run()
    df = test.toDataFrame()
    print(df)
    print("###########################")
    print(details.sortedTransmissions())
    print("#######################")
    print(details.personHistory(3))
    test.plot()

def testRandSEIRD():
    S0 = 999
    E0 = 0
    I0 = 1
    rho = .2
    gamma = 0.4
    mu = .1
    plane = 25
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSEIRD(S0=S0, E0=E0, I0=I0, R0=0, rho=rho, gamma=gamma, mu=mu, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r,
    days=days)
    details = test.run()
    df = test.toDataFrame()
    print(df)
    print("###########################")
    print(details.sortedTransmissions())
    print("#######################")
    print(details.personHistory(3))
    test.plot()

def testRandSEIRSD():
    S0 = 999
    E0 = 0
    I0 = 1
    rho = .2
    gamma = 0.4
    mu = .1
    kappa = .4
    plane = 25
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSEIRSD(S0=S0, E0=E0, I0=I0, R0=0, rho=rho, gamma=gamma, mu=mu, kappa=kappa, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r,
    days=days)
    details = test.run()
    df = test.toDataFrame()
    print(df)
    print("###########################")
    print(details.sortedTransmissions())
    print("#######################")
    print(details.personHistory(3))
    test.plot()


def testRandMoveSIRSDV():
    S0 = 999
    V0 = 0
    I0 = 1
    eta = .03
    gamma = 0.4
    mu = .03
    kappa = .2
    plane = 25
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSIRSDV(S0=S0, I0=I0, R0=0, V0=V0, gamma=gamma, mu=mu, kappa=kappa, eta=eta, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r, days=days, timeDelay=4)
    details = test.run()
    df = test.toDataFrame()
    print(df)
    print("###########################")
    #print(details.sortedTransmissions())
    #print("#######################")
    for i in range(1000):
        print(details.personHistory(i))
    test.plot()

def testRandMoveSIRDV():
    S0 = 999
    V0 = 0
    I0 = 1
    eta = .03
    gamma = 0.4
    mu = .03
    #kappa = .2
    plane = 25
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSIRDV(S0=S0, I0=I0, R0=0, V0=V0, gamma=gamma, mu=mu, eta=eta, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r, days=days, timeDelay=4)
    details = test.run()
    df = test.toDataFrame()
    print(df)
    print("###########################")
    #print(details.sortedTransmissions())
    #print("#######################")
    for i in range(1000):
        print(details.personHistory(i))
    test.plot()


def testRandSEIRV():
    S0 = 999
    E0=0
    V0 = 0
    I0 = 1
    rho = .3
    eta = .03
    gamma = 0.4
    #kappa = .2
    plane = 25
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSEIRV(S0=S0, E0=E0, I0=I0, R0=0, V0=V0, gamma=gamma, rho=rho, eta=eta, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r, days=days, timeDelay=4)
    details = test.run()
    df = test.toDataFrame()
    print(df)
    print("###########################")
    #print(details.sortedTransmissions())
    #print("#######################")
    for i in range(1000):
        print(details.personHistory(i))
    
    test.plot()
def testRandSEIRVS():
    S0 = 999
    E0=0
    V0 = 0
    I0 = 1
    rho = .3
    eta = .03
    gamma = 0.4
    kappa = .2
    plane = 25
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSEIRVS(S0=S0, E0=E0, I0=I0, R0=0, V0=V0, gamma=gamma, rho=rho, eta=eta, kappa=kappa, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r, days=days, timeDelay=4)
    details = test.run()
    df = test.toDataFrame()
    print(df)
    print("###########################")
    #print(details.sortedTransmissions())
    #print("#######################")
    for i in range(1000):
        print(details.personHistory(i))
    test.plot()




def main():
    test = HubSIS(S0=999, I0=1, pss=.2, rstart=3, side=25, days=31, gamma=.3)
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
    gamma = 0.4
    plane = 25
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSIS(S0=S0, I0=I0, gamma=gamma, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r,
    days=days)
    details = test.run()
    df = test.toDataFrame()
    #print(df)
    #print(details.personHistory(4))
    #print(details.transmissions)
    print("#####################################")
    print(details.personTransmissionHistory(7))
    #dic = details.sortedTransmissions()
    #print(dic)


def getHubSIRS():
    test = HubSIRS(popsize=1000, pss=.2, rstart=3, alpha=2, side=25, S0=999, I0=1, R0=0, days=31, gamma=.4, kappa= .2, w0=.7)
    d = test.run()
    print(d.personHistory(652))
    test.plot()
    df = test.toDataFrame()
    print(df)

def getStrongInfSIR():
    S0 = 999
    I0 = 1
    R0 = 0
    rstart = 3
    side=33
    days=31
    pss=.17
    gamma = .3
    test= StrongInfSIR(S0=S0, I0=I0, R0=R0, pss=pss, rstart=rstart, side=side, days=days, gamma=gamma)
    test.run()
    print(test.toDataFrame())


def getHubSEIR():
    test = HubSEIR(S0=999, E0=0, I0=1, R0=0, pss=.17, rho=.3, gamma=.23, side=25, rstart=3, alpha=2, 
    days=31)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())

def getHubSEIRD():
    test = HubSEIRD(S0=999, E0=0, I0=1, R0=0, pss=.17, rho=.3, gamma=.23, mu=.05,side=25, rstart=3, alpha=2, 
    days=31)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    test.plot()

def getStrongInfSEIRD():
    test = StrongInfSEIRD(S0=999, E0=0, I0=1, R0=0, pss=.17, rho=.3, gamma=.23, mu=.05,side=25, rstart=3, alpha=2, 
    days=31)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    test.plot()

def getStrongInfSEIR():
    test = StrongInfSEIR(S0=999, E0=0, I0=1, R0=0, pss=.17, rho=.3, gamma=.23, side=25, rstart=3, alpha=2.0, days=31)
    test.run()
    print(test.toDataFrame())

def getHubSIRD():
    test = HubSIRD(S0=999, I0=1, R0=0, pss=.17, gamma=.23, mu=.05,side=25, rstart=3, alpha=2, 
    days=31)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    test.plot()

def getHubSIRSD():
    test = HubSIRSD(S0=999, I0=1, R0=0, pss=.17, gamma=.23, kappa=.15, mu=.05,side=25, rstart=3, alpha=2, 
    days=31)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    print(df.personHistory(46))
    test.plot()

def getHubSEIRSD():
    test = HubSEIRSD(S0=999, E0=0, I0=1, R0=0, pss=.17, rho=.3, gamma=.23, kappa=.2, mu=.05,side=25, rstart=3, alpha=2, 
    days=31)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    test.plot()

def getHubSEIRVD():
    test = HubSEIRVD(S0=999, E0=0, I0=1, R0=0, V0=0, pss=.17, rho=.3, gamma=.23, eta=.02, mu=.05,side=25, rstart=3, alpha=2, 
    days=31, timeDelay=5)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    test.plot()

def getHubSEIRSVD():
    test = HubSEIRSVD(S0=999, E0=0, I0=1, R0=0, V0=0, pss=.17, rho=.3, gamma=.23, kappa=.2, eta=.02, mu=.05,side=25, rstart=3, alpha=2, 
    days=31, timeDelay = 5)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    test.plot()

def getHubSIRVD():
    test = HubSIRVD(S0=999, I0=1, R0=0, V0=0, pss=.17, gamma=.23, eta=.02, mu=.01,side=25, rstart=3, alpha=2, 
    days=31, timeDelay=5)
    details = test.run()
    print(test.toDataFrame())
    print(details.personHistory(44))
    test.plot()

def getHubSIRSVD():
    test = HubSIRSVD(S0=999, I0=1, R0=0, V0=0, pss=.17, gamma=.23, kappa = .2, eta=.02, mu=.01,side=25, rstart=3, alpha=2, days=31, timeDelay=5)
    details = test.run()
    print(test.toDataFrame())
    print(details.personHistory(44))
    test.plot()

def getHubSEIRV():
    test = HubSEIRV(S0=999, E0=0, I0=1, R0=0, V0=0, pss=.17, rho=.3, gamma=.23, eta=.03, side=25, rstart=3, alpha=2, 
    days=31, timeDelay=5)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    test.plot()

def getHubSEIRSV():
    test = HubSEIRSV(S0=999, E0=0, I0=1, R0=0, V0=0, pss=.17, rho=.3, gamma=.23, eta=.03, kappa=.2, side=25, rstart=3, alpha=2, 
    days=31, timeDelay=5)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    test.plot()

def getHubSIRV():
    test = HubSIRV(S0=999, I0=1, R0=0, V0=0, pss=.17, gamma=.23, eta=.03, side=50, rstart=3, alpha=2, 
    days=31, timeDelay=5)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    test.plot()

def getHubSIRSV():
    test = HubSIRSV(S0=999, I0=1, R0=0, V0=0, pss=.17, gamma=.23, eta=.03, kappa=.2, side=50, rstart=3, alpha=2, 
    days=61, timeDelay=5)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    test.plot()

def getHubSIR():
    for i in range(1, 31+1):
        print(i)
    test = HubSIR(S0=999, I0=1, R0=1, pss=.2, rstart=3, alpha=2, side=25,days=31, gamma=.2, w0=.7)
    d = test.run()
    print(len(test.locx))
    print(d.personHistory(652))
    test.plot()
    df = test.toDataFrame()
    print(df)

def testRandSIR():
    S0 = 999
    I0 = 1
    gamma = 0.4
    plane = 25
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSIR(S0=S0, I0=I0, R0=0, gamma=gamma, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r,
    days=days)
    details = test.run()
    df = test.toDataFrame()
    print(df)
    print("###########################")
    print(details.sortedTransmissions())
    print("#######################")
    print(details.personHistory(686))
    test.plot()

def testRandSIRD():
    S0 = 999
    I0 = 1
    gamma = 0.4
    mu = .2
    plane = 25
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSIRD(S0=S0, I0=I0, R0=0, gamma=gamma, mu=mu, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r,
    days=days)
    details = test.run()
    df = test.toDataFrame()
    print(df)
    print("###########################")
    print(details.sortedTransmissions())
    print("#######################")
    print(details.personHistory(686))
    test.plot()

def testRandSIRSD():
    S0 = 999
    I0 = 1
    gamma = 0.4
    mu = .2
    kappa = .3
    plane = 25
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSIRSD(S0=S0, I0=I0, R0=0, gamma=gamma, mu=mu, kappa=kappa, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r,
    days=days)
    details = test.run()
    df = test.toDataFrame()
    print(df)
    print("###########################")
    print(details.sortedTransmissions())
    print("#######################")
    print(details.personHistory(686))
    test.plot()


def testRandSIRS():
    S0 = 999
    I0 = 1
    gamma = 0.4
    kappa = .2
    plane = 25
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSIRS(S0=S0, I0=I0, R0=0, gamma=gamma, kappa=kappa, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r,
    days=days)
    details = test.run()
    df = test.toDataFrame()
    print(df)
    print("###########################")
    print(details.sortedTransmissions())
    print("#######################")
    print(details.personHistory(686))
    test.plot()

def testRandSEIR():
    S0 = 999
    E0 = 0
    I0 = 1
    rho = .2
    gamma = 0.4
    kappa = .2
    plane = 25
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSEIR(S0=S0, E0=E0, I0=I0, R0=0, rho=rho, gamma=gamma, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r,
    days=days)
    details = test.run()
    df = test.toDataFrame()
    print(df)
    print("###########################")
    print(details.sortedTransmissions())
    print("#######################")
    print(details.personHistory(686))
    test.plot()

def testRandSEIRS():
    S0 = 999
    E0 = 0
    I0 = 1
    rho = .2
    gamma = 0.4
    kappa = .2
    plane = 25
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSEIRS(S0=S0, E0=E0, I0=I0, R0=0, rho=rho, gamma=gamma, kappa=kappa, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r, days=days)
    details = test.run()
    df = test.toDataFrame()
    print(df)
    print("###########################")
    print(details.sortedTransmissions())
    print("#######################")
    print(details.personHistory(686))
    test.plot()

def testRandSIRV():
    S0 = 999
    V0 = 0
    I0 = 1
    eta = .03
    gamma = 0.4
    #kappa = .2
    plane = 25
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSIRV(S0=S0, I0=I0, R0=0, V0=V0, gamma=gamma, eta=eta, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r, days=days, timeDelay=4)
    details = test.run()
    df = test.toDataFrame()
    print(df)
    print("###########################")
    print(details.sortedTransmissions())
    print("#######################")
    print(details.personHistory(686))
    test.plot()

def testRandSIRVS():
    S0 = 999
    V0 = 0
    I0 = 1
    eta = .03
    gamma = 0.4
    kappa = .2
    plane = 25
    move_R = 5
    sigma_R = 2
    spread_r = 1
    sigma_r = .25
    days = 31
    test = RandMoveSIRVS(S0=S0, I0=I0, R0=0, V0=V0, gamma=gamma, eta=eta, kappa=kappa, planeSize=plane, move_r=move_R, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r, days=days, timeDelay=4)
    details = test.run()
    df = test.toDataFrame()
    print(df)
    print("###########################")
    print(details.sortedTransmissions())
    print("######################")
    print(test.Scollect[999].r0)
    print("#######################")
    print(details.personHistory(686))
    test.plot()

def getHubSEIRS():
    kappa = .2
    test = HubSEIRS(S0=999, E0=0, I0=1, R0=0, pss=.17, rho=.3, gamma=.23, kappa=kappa, side=25, rstart=3, alpha=2, 
    days=31)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())

def getHub_ICUV():
    test = Hub_ICUV(S0=999, E0=0, I0=1, R0=0, V0=0, rho=.3, ioda=.3, gamma=.25, mu=0.007, omega=.14, phi = .42, chi=.15, kappa=.05, eta=.03, rstart=3, pss=.17, side=25, days=62)
    d = test.run()
    print(test.toDataFrame())
    print(d.personHistory(473))
    test.plot()

def getStrongInf_ICUV():
    test = StrongInf_ICUV(S0=999, E0=0, I0=1, R0=0, V0=0, rho=.3, ioda=.3, gamma=.25, mu=0.007, omega=.14, phi = .42, chi=.15, kappa=.05, eta=.03, rstart=3, pss=.17, side=25, days=62, w0=.7)
    d = test.run()
    print(test.toDataFrame())
    print(d.personHistory(473))
    test.plot()

def getStrongInfSEIRS():
    kappa = .2
    test = StrongInfSEIRS(S0=999, E0=0, I0=1, R0=0, pss=.17, rho=.3, gamma=.23, kappa=kappa, side=25, rstart=3, alpha=2, 
    days=61)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())

def getStrongInfSEIRSD():
    test = StrongInfSEIRSD(S0=999, E0=0, I0=1, R0=0, pss=.17, rho=.3, gamma=.23, kappa=.2, mu=.05,side=25, rstart=3, alpha=2, 
    days=31)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    test.plot()

def getStrongInfSEIRSV():
    test = StrongInfSEIRSV(S0=999, E0=0, I0=1, R0=0, V0=0, pss=.17, rho=.3, gamma=.23, eta=.03, kappa=.2, side=25, rstart=3, alpha=2, 
    days=31, timeDelay=5)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    test.plot()

def getStrongInfSEIRSVD():
    test = StrongInfSEIRSVD(S0=999, E0=0, I0=1, R0=0, V0=0, pss=.17, rho=.3, gamma=.23, kappa=.2, eta=.02, mu=.05,side=25, rstart=3, alpha=2, 
    days=31, timeDelay = 5)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    test.plot()

def getStrongInfSEIRV():
    test = StrongInfSEIRV(S0=999, E0=0, I0=1, R0=0, V0=0, pss=.17, rho=.3, gamma=.23, eta=.03, side=25, rstart=3, alpha=2, 
    days=31, timeDelay=5)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    test.plot()

def getStrongInfSEIRVD():
    test = StrongInfSEIRVD(S0=999, E0=0, I0=1, R0=0, V0=0, pss=.17, rho=.3, gamma=.23, eta=.02, mu=.05,side=25, rstart=3, alpha=2, 
    days=31, timeDelay=5)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    test.plot()

def getStrongInfSIRD():
    test = StrongInfSIRD(S0=999, I0=1, R0=0, pss=.17, gamma=.23, mu=.05,side=25, rstart=3, alpha=2, 
    days=31)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    test.plot()

def getStrongInfSIRSD():
    kappa = .2
    test = StrongInfSIRSD(S0=999, I0=1, R0=0, pss=.17, gamma=.23, kappa=kappa, mu=.05,side=25, rstart=3, alpha=2, 
    days=31)
    df = test.run()
    print(df.sortedTransmissions())
    print(test.toDataFrame())
    test.plot()

def getStrongInfSIRSV():
    test = StrongInfSIRSV(S0=999, I0=1, R0=0, V0=0, pss=.17, gamma=.23, kappa = .2, eta=.02, side=25, rstart=3, alpha=2, days=31, timeDelay=5)
    details = test.run()
    print(test.toDataFrame())
    print(details.personHistory(44))
    test.plot()

def getStrongInfSIRSVD():
    test = StrongInfSIRSVD(S0=999, I0=1, R0=0, V0=0, pss=.17, gamma=.23, kappa = .2, eta=.02, mu=.01,side=25, rstart=3, alpha=2, days=31, timeDelay=5)
    details = test.run()
    print(test.toDataFrame())
    print(details.personHistory(44))
    test.plot()

def getStrongInfSIRV():
    test = StrongInfSIRV(S0=999, I0=1, R0=0, V0=0, pss=.17, gamma=.23, eta=.02, side=25, rstart=3, alpha=2, days=31, timeDelay=5)
    details = test.run()
    print(test.toDataFrame())
    print(details.personHistory(44))
    test.plot()

def getStrongInfSIRVD():
    test = StrongInfSIRVD(S0=999, I0=1, R0=0, V0=0, pss=.17, gamma=.23, eta=.02, mu=.02, side=25, rstart=3, alpha=2, days=31, timeDelay=5)
    details = test.run()
    print(test.toDataFrame())
    print(details.personHistory(44))
    test.plot()




if  __name__ == '__main__':
    #main()
    #getStrongInfSEIRS()
    #getStrongInfSEIRSD()
    #getStrongInfSEIRSV()
    #getStrongInfSEIRSVD()
    #getStrongInfSEIRV()
    #getStrongInfSEIRVD()
    #getStrongInfSIRD()
    #getStrongInfSIRSD()
    #getStrongInfSIRSVD()
    #getStrongInfSIRSV()
    #getStrongInfSIRSVD()
    #getStrongInfSIRV()
    getStrongInfSIRVD()
    #getStrongInfSEIR()
    #getStrongInfSIR()
    #getStrongInfSIS()
    #getStrongInfSEIRD()
    #getStrongInf_ICUV()
    #getHub_ICUV()
    #getHubSIR()
    #getHubSEIR()
    #getHubSIRV()
    #getHubSIRSVD()
    #getHubSIRVD()
    #getHubSIRSV()
    #getHubSEIRVD()
    #testRandSEIRDV()
    #testRandMoveSIRDV()
    #testRandSIRSD()
    #testRandSEIRVS()
    #testRandSEIRV()
    #testRandSEIR()
    #testRandSIRV()
    #testRandSEIRS()
    #testRandMoveSIS()
    #testRandSIRS()
    #testRandSIR()
