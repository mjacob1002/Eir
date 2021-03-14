from .dtmc import DTMC
from src.utility import randEvent
from multipledispatch import dispatch
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class DTMCSIS(DTMC):
    @dispatch(int, int, int, float, float)
    def __init__(self, S0: int, I0: int, days: int, beta: float, gamma: float):
        super(DTMCSIS, self).__init__(S0, I0, days)
        self.beta = beta
        self.gamma = gamma
        self.N = S0 + I0

    # determine if someone will go from S -> I
    # formula is standard and comes from the initial deterministic equation
    @dispatch(int)
    def __muSI__(self, pos: int):
        # calculate the probability
        w = self.beta * self.I[pos] / self.N
        # return the event of whether someone was infected or not
        return randEvent(w)

    # runs the simulations and changes the array values
    @dispatch()
    def run(self):
        for i in range(1, self.numSims):
            SIcount, IScount = 0, 0
            print("Suscpetibles")
            for j in range(int(self.S[i - 1])):
                event = self.__muSI__(i - 1)
                if event:
                    SIcount += 1
                print(SIcount)
            # print("Infecteds")
            for j in range(int(self.I[i - 1])):
                event = randEvent(self.gamma)
                if event:
                    IScount += 1
                print(IScount)
            self.S[i] = self.S[i - 1] - SIcount + IScount
            self.I[i] = self.I[i - 1] - IScount + SIcount

    @dispatch(S=bool, I=bool, title=str)
    def plot(self, S=True, I=True, title="Epidemiological Simulation"):
        t = np.linspace(0, self.days, self.numSims)
        if S:
            plt.plot(t, self.S, label="Susceptible", color='r')
        if I:
            plt.plot(t, self.I, label="Infected", color='b')

        plt.title(title)
        plt.xlabel("Days")
        plt.ylabel("Number of People")
        plt.legend()
        plt.show()

    def toDataFrame(self):
        # create the linspace object
        t = np.linspace(0,self.days, self.days+1)
        # convert the numpy array to one stacked into columns 
        arr = np.stack([t, self.S, self.I], axis=1)
        # convert that into dataframe with labels
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Infected"])
        return df

# test
N = 100
S0 = 75
I0 = 25
beta = 1.5
gamma = 0.3
days = 31

l = DTMCSIS(S0, I0, days, beta, gamma)
l.run()
print(l.toDataFrame())