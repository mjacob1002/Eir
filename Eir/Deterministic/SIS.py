from .CompartmentalModel import CompartmentalModel
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from multipledispatch import dispatch

# Flow of the Compartmental Model:
# S -> I - > S
class SIS(CompartmentalModel):
    """
    SIS deterministic model.

    Parameters
    ----------

    beta: float
        Effective transmission rate of an infectious person, on average.
    
    gamma: float 
        Proportion of people in I who go to S.
    
    S0: int
        Initial susceptibles.
    
    I0: int
        Initial infecteds.


    """ 
    def __init__(self, beta, gamma, S0, I0):
        self.intCheck([S0, I0])
        self.floatCheck([beta, gamma, S0, I0])
        self.probCheck([gamma])
        self.negValCheck([beta, gamma])
        
        super(SIS, self).__init__(S0, I0)
        # infection rate
        self.beta = beta
        # recovery rate (I -> S)
        self.gamma = gamma
        # population size
        self.N = S0 + I0

    @dispatch(float, float)
    def _deriv(self, s: float, i: float):
        x = self.beta * s * i / self.N
        y = self.gamma * i
        return -x + y, x - y

    @dispatch(float, np.ndarray, np.ndarray)
    def _update(self, dt, S1, I1):
        S, I = S1, I1
        for i in range(1, len(S)):
            f = self._deriv(S[i - 1], I[i - 1])
            S[i] = S[i - 1] + dt * f[0]
            I[i] = I[i - 1] + dt * f[1]
        return S, I

    def _simulate(self, days: int, dt: float):
        # total number of iterations that will be run + the starting value at time 0
        size = int(days / dt + 1)
        # create the arrays to store the different values
        S, I = np.zeros(size), np.zeros(size)
        # initialize the arrays
        S[0], I[0] = self.S0, self.I0
        # run the Euler's Method
        S, I = self._update(dt, S, I)
        return S, I

    # method that determines variables to be included in the plot
    def _includeVar(self, sx: bool, ix: bool):
        labels = []
        if sx:
            labels.append("Susceptible")
        if ix:
            labels.append("Infected")
        return labels

    @dispatch(int, float, plot=True, Sbool=True, Ibool=True)
    def run(self, days: int, dt: float, plot=True, Sbool=True, Ibool=True):
        # evenly space the days
        t = np.linspace(0, days, int(days / dt) + 1)
        # run a simulation and get the S and I arrays
        S, I = self._simulate(days=days, dt=dt)
        # data prepared to be turned into dataframe
        data1 = {
            "Days": t,
            "Susceptible": S,
            "Infected": I
        }
        # labels for the data in the dataframe
        labels = ["Days", "Susceptible", "Infected"]
        # turn into dataframe
        df = pd.DataFrame(data=data1, columns=labels)
        # plotting
        if plot:
            # retrieve the list of variables that will be plotted
            included = self._includeVar(Sbool, Ibool)
            fig = df.plot("Days", included)
            plt.xlabel("Number of Days")
            plt.ylabel("Number of People")
            plt.show()
            return df, fig
        return df

    def normalizeRun(self, days: int, dt: float):
        df = self.run(days, dt, plot=False)
        # calculate the population size
        popSize = df["Susceptible"].iloc[0] + df["Infected"].iloc[0]
        colnames = list(df.columns)
        colnames.pop(0)
        for i in colnames:
            df[i] = df[i].div(popSize)
        return df

