from .SIR import SIR
import numpy as np
from matplotlib import pyplot as plt
from multipledispatch import dispatch
import pandas as pd


class SIRD(SIR):
    """
    SIRD deterministic model.

    Parameters
    ----------

    beta: float
        Effective transmission rate of infectious person, on average
    
    gamma: float
        Proportion of people who go from I to R
    
    omega: float
        Proportion of people who go from I to D.
    
    S0: int
        Initial number of susceptibles
    
    I0: int
        Initial number of infecteds
    
    R0: int
        Initial number of removeds.
    """
    # omega is the amount of people that go from I to D
    def __init__(self, beta: float, gamma: float, omega: float, S0: int, I0: int, R0: int):
        self.intCheck([S0, I0, R0])
        self.floatCheck([beta, gamma, omega, S0, I0, R0])
        self.negValCheck([beta, gamma, omega, S0, I0, R0])
        self.probCheck([gamma, omega])
        super(SIRD, self).__init__(beta, gamma, S0, I0, R0)
        self.omega = omega
        assert self.gamma + self.omega <= 1

    # change the variable omega
    def changeOmega(self, x: float):
        self.omega = x

    @dispatch(float, float, int)
    # calculate the derivatives; because open pop, feed in the current alive population
    def _deriv(self, s: float, i: float, n):
        # amount leaving S -> I
        x = self.beta * s * i / n
        # amount leaving I -> R
        y = self.gamma * i
        # amount leaving I -> D
        z = self.omega * i
        # returns in the order S, I, R, D
        return -x, x - y - z, y, z

    # run Euler's method

    @dispatch(float, np.ndarray, np.ndarray, np.ndarray, np.ndarray)
    def _update(self, dt, S, I, R, D) -> tuple:
        # run Euler's method
        for i in range(1, len(S)):
            n = int(S[i - 1] + I[i - 1] + R[i - 1])
            # get the derivatives at the point before for the Euler's method
            f = self._deriv(S[i - 1], I[i - 1], n)
            # computer the Euler's approximation f(x+h) = f(x) + h * (df/dx)
            S[i] = S[i - 1] + dt * f[0]
            I[i] = I[i - 1] + dt * f[1]
            R[i] = R[i - 1] + dt * f[2]
            D[i] = D[i - 1] + dt * f[3]
            # remove the deaths from the living population
            n = n - f[3] * dt
        return S, I, R, D

    def _simulate(self, days: int, dt: float):
        # total number of iterations that will be run + the starting value at time 0
        size = int(days / dt + 1)
        # create the arrays to store the different values
        S, I, R, D = np.zeros(size), np.zeros(size), np.zeros(size), np.zeros(size)
        # initialize the arrays
        S[0], I[0], R[0], D[0] = self.S0, self.I0, self.R0, 0
        # run the Euler's Method
        S, I, R, D = self._update(dt, S, I, R, D)
        return S, I, R, D

    # create the variable labels for the 'run' function
    @dispatch(bool, bool, bool, bool)
    def _includeVar(self, sx: bool, ix: bool, rx: bool, Dx: bool):
        labels = []
        if sx:
            labels.append("Susceptible")
        if ix:
            labels.append("Infected")
        if rx:
            labels.append("Removed")
        if Dx:
            labels.append("Deaths")
        return labels

    @dispatch(int, float, plot=bool, Sbool=bool, Ibool=bool, Rbool=bool, Dbool=bool)
    def run(self, days: int, dt: float, plot=True, Sbool=True, Ibool=True, Rbool=True, Dbool=True):
        # evenly space the days
        t = np.linspace(0, days, int(days / dt) + 1)
        # run a simulation to get the numpy arrays
        S, I, R, D = self._simulate(days, dt)
        # data prepared to be converted into Pandas dataframe
        data1 = {
            "Days": t,
            "Susceptible": S,
            "Infected": I,
            "Removed": R,
            "Deaths": D
        }
        # labels for the data
        label = ["Days", "Susceptible", "Infected", "Removed", "Deaths"]
        df = pd.DataFrame(data=data1, columns=label)
        # plotting
        if plot:
            # retrieve the list of variables that will be plotted
            included = self._includeVar(Sbool, Ibool, Rbool, Dbool)
            fig = df.plot("Days", included)
            plt.xlabel("Number of Days")
            plt.ylabel("Number of People")
            plt.show()
            return df, fig
        return df

    # plot an accumulation function of total cases
    def accumulate(self, days: int, dt: float, plot=True):
        self.floatCheck([days, dt])
        self.negValCheck([days, dt])
        t = np.linspace(0, days, int(days / dt) + 1)
        S, I, R, D = self._simulate(days, dt)
        # create a numpy array that will hold all of the values
        cases = np.zeros(len(I))
        # add up the total infected and removed at given time to account for everyone with the virus
        for i in range(len(I)):
            cases[i] = I[i] + R[i] + D[i]
        # create a dictionary that holds the data for easy conversion to dataframe
        data1 = {
            "Days": t,
            "Susceptible": S,
            "Infected": I,
            "Removed": R,
            "Deaths": D,
            "Total Cases": cases
        }
        # create the column labels
        labels = ['Days', "Susceptible", "Infected", "Removed", "Deaths", "Total Cases"]
        # convert to dataframe
        df = pd.DataFrame(data=data1, columns=labels)
        if plot:
            # do some plotting
            df.plot(x="Days", y=["Total Cases"])
            plt.xlabel("Days")
            plt.ylabel("Total Cases")
            plt.show()
        # return dataframe
        return df



