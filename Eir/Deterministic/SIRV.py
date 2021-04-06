from .SIR import SIR
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from multipledispatch import dispatch


# Flow of the Compartmental Model:
# S -> I -> R, S- > V
class SIRV(SIR):
    """
    SIRV deterministic model.

    Parameters
    ----------

    beta: float
        Effective transmission rate of an infectious person, on average.
    
    gamma: float
        Proportion of people that go from I to R.
    
    eta: float
        Proportion of people that go from S to V.
    
    S0: int
        Initial susceptibles at the start of the simulation.
    
    I0: int
        Initial infecteds at the start of the simulation.
    
    R0: int
        Initial recovereds at the start of the simulation.
    
    V0: int
        Initial vaccinated at the start of the simulation.
    """
    def __init__(self, beta, gamma, eta, S0, I0, R0, V0):
        self.intCheck([S0, I0, R0, V0])
        self.floatCheck([beta, gamma, eta])
        self.negValCheck([beta, gamma, eta, S0, I0, R0, V0])
        self.probCheck([gamma, eta])
        super(SIRV, self).__init__(beta, gamma, S0, I0, R0)
        self.V0 = V0
        self.eta = eta
        self.N = S0 + I0 + R0 + V0

    def changeV0(self, x: int):
        self.V0 = x
        self.N = self.S0 + self.I0 + self.R0 + self.V0

    def changeEta(self, x: int):
        self.eta = x

    def _deriv(self, s, i):
        # amount of people going from S -> I
        x = self.beta * s * i / self.N
        # amount of people going from I -> R
        y = self.gamma * i
        # amount of people going from S -> V
        z = self.eta * s
        return -x - z, x - y, y, z

    @dispatch(float, np.ndarray, np.ndarray, np.ndarray, np.ndarray)
    def _update(self, dt: float, S, I, R, V):
        # run Euler's Method
        for i in range(1, len(S)):
            # get the derivatives at a point before
            f = self._deriv(S[i - 1], I[i - 1])
            # compute the euler's method: f(x+h) = f(x) + h * (df/dx)
            S[i] = S[i - 1] + dt * f[0]
            I[i] = I[i - 1] + dt * f[1]
            R[i] = R[i - 1] + dt * f[2]
            V[i] = V[i - 1] + dt * f[3]
        return S, I, R, V

    def _simulate(self, days: int, dt: float):
        # total number of iterations that will be run + the starting value at time 0
        size = int(days / dt + 1)
        # create the arrays to store the different values
        S, I, R, V = np.zeros(size), np.zeros(size), np.zeros(size), np.zeros(size)
        # initialize the arrays
        S[0], I[0], R[0], V[0] = self.S0, self.I0, self.R0, self.V0
        # run the Euler's Method
        S, I, R, V = self._update(dt, S, I, R, V)
        return S, I, R, V

    # include the variables that will be plotted in the run function
    @dispatch(bool, bool, bool, bool)
    def _includeVar(self, sx: bool, ix: bool, rx: bool, vx):
        labels = []
        if sx:
            labels.append("Susceptible")
        if ix:
            labels.append("Infected")
        if rx:
            labels.append("Removed")
        if vx:
            labels.append("Vaccinated")
        return labels

    @dispatch(int, float, plot=bool, Sbool=bool, Ibool=bool, Rbool=bool, Vbool=bool)
    def run(self, days: int, dt: float, plot=True, Sbool=True, Ibool=True, Rbool=True, Vbool=True):
        # evenly space the days
        t = np.linspace(0, days, int(days / dt) + 1)
        # run a simulation and get the numpy arrays
        S, I, R, V = self._simulate(days, dt)
        # data prepared to be converted into Pandas dataframe
        data1 = {
            "Days": t,
            "Susceptible": S,
            "Infected": I,
            "Removed": R,
            "Vaccinated": V
        }
        # labels for the data
        label = ["Days", "Susceptible", "Infected", "Removed", "Vaccinated"]
        df = pd.DataFrame(data=data1, columns=label)
        # plotting
        if plot:
            # retrieve the list of variables that will be plotted
            included = self._includeVar(Sbool, Ibool, Rbool, Vbool)
            fig = df.plot("Days", included)
            plt.xlabel("Number of Days")
            plt.ylabel("Number of People")
            plt.show()
            return df, fig
        return df

    def accumulate(self, days: int, dt: float, plot=True):
        self.floatCheck([days, dt])
        self.negValCheck([days, dt])
        t = np.linspace(0, days, int(days / dt) + 1)
        S, I, R, V = self._simulate(days, dt)
        # create a numpy array that will hold all of the values
        cases = np.zeros(len(I))
        # add up the total infected and removed at given time to account for everyone with the virus
        for i in range(len(I)):
            cases[i] = I[i] + R[i]
        # create a dictionary that holds the data for easy conversion to dataframe
        data1 = {
            "Days": t,
            "Susceptible": S,
            "Infected": I,
            "Removed": R,
            "Vaccinated": V,
            "Total Cases": cases
        }
        # create the column labels
        labels = ['Days', "Susceptible", "Infected", "Removed", "Vaccinated", "Total Cases"]
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
