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


class SIR(CompartmentalModel):
    # beta is the transmission rate, gamma is the recovery rate
    # S0, I0, R0 are the starting Susceptible, infected, and removed people respectively
    def __init__(self, beta: float, gamma: float, S0: int, I0: int, R0: int):
        # makes sure all values are non-negative
        assert beta > 0, gamma > 0
        assert S0 >= 0
        assert I0 >= 0
        assert R0 >= 0
        super(SIR, self).__init__(S0, I0)
        self.R0 = R0
        self.beta = beta
        self.gamma = gamma
        self.N = S0 + I0 + R0

    # meant to change the starting value of S, S0, of SIR object
    def changeS0(self, x: int):
        self.S0 = x
        # after modifying S0, change N accordingly
        self.N = self.S0 + self.I0 + self.R0

    # meant to change the starting value of I, I0, of SIR object
    def changeI0(self, x: int):
        self.I0 = x
        # after modifying I0, change N accordingly
        self.N = self.S0 + self.I0 + self.R0

    # meant to change the starting value of R, R0, of SIR object
    def changeR0(self, x: int):
        self.R0 = x
        # after modifying R0, change N accordingly
        self.N = self.S0 + self.I0 + self.R0

    # meant to change the value of beta of SIR object
    def changeBeta(self, x: float):
        self.beta = x

    # meant to change the value of gamma of SIR object
    def changeGamma(self, x: float):
        self.gamma = x

    # computes the derivatives at a particular point, given the beta/gamma of object and current s and i values
    @dispatch(float, float)
    def _deriv(self, s, i) -> tuple:
        # x is the amount of leaving S compartment and entering I
        x = self.beta * s * i / self.N
        # y is the amount leaving I compartment and entering R compartment
        y = self.gamma * i
        return -x, x - y, y

    # runs Euler's Method
    @dispatch(float, np.ndarray, np.ndarray, np.ndarray)
    def _update(self, dt, S1, I1, R1) -> tuple:
        # copy the inputted arrays
        S, I, R = S1, I1, R1
        # for all the days that ODE will be solved
        for i in range(1, len(S)):
            f = self._deriv(S[i - 1], I[i - 1])
            S[i] = S[i - 1] + dt * f[0]
            I[i] = I[i - 1] + dt * f[1]
            R[i] = R[i - 1] + dt * f[2]
        return S, I, R

    # combines the Euler's Method with all initialization and stuff and runs full simulation
    # days is the number of days being simulated, dt is the step size for Euler's method
    def _simulate(self, days: int, dt: float) -> tuple:
        # total number of iterations that will be run + the starting value at time 0
        size = int(days / dt + 1)
        # create the arrays to store the different values
        S, I, R = np.zeros(size), np.zeros(size), np.zeros(size)
        # initialize the arrays
        S[0], I[0], R[0] = self.S0, self.I0, self.R0
        # run the Euler's Method
        S, I, R = self._update(dt, S, I, R)
        return S, I, R

    def _includeVar(self, sx: bool, ix: bool, rx: bool) -> list:
        # list of the strings that will be returned and then passed into plot function
        labels = []
        # if the user wants to plot susceptible
        if sx:
            labels.append("Susceptible")
        # if the user wants to plot infected
        if ix:
            labels.append("Infected")
        # if the user wants to plot removed
        if rx:
            labels.append("Removed")
        return labels

    def run(self, days: int, dt: float, plot=True, Sbool=True, Ibool=True, Rbool=True):
        # creates evenly spaced array that spans day 0 to the day wanted
        t = np.linspace(0, days, int(days / dt) + 1)
        S, I, R = self._simulate(days, dt)
        # makes a dictionary so that it can be easily converted to a dataframe
        data1 = {
            "Days": t,
            "Susceptible": S,
            "Infected": I,
            "Removed": R
        }
        # create the labels that will be the columns of the dataframe
        label = ["Days", "Susceptible", "Infected", "Removed"]
        # create a dataframe
        df = pd.DataFrame(data=data1, columns=label)
        # if the plot boolean is true aka they want a plot to be shown
        if plot:
            # determine what should be plotted
            included = self._includeVar(Sbool, Ibool, Rbool)
            # create the plot & label the x and y axis
            fig = df.plot(x="Days", y=included)
            plt.xlabel("Number of Days")
            plt.ylabel("Number of People")
            # display the plot
            plt.show()
            # return dataframe & plot object
            return df, fig
        # return the dataframe
        return df

    # plot an accumulation function of total cases
    def accumulate(self, days: int, dt: float, plot=True):
        t = np.linspace(0, days, int(days / dt) + 1)
        S, I, R = self._simulate(days, dt)
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
            "Total Cases": cases
        }
        # create the column labels
        labels = ['Days', "Susceptible", "Infected", "Removed", "Total Cases"]
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

    # create everything as a percentage of the total population, given a dataframe
    def normalizeDataFrame(self, df: pd.DataFrame) -> pd.DataFrame:
        popSize = df["Susceptible"].iloc[0] + df["Infected"].iloc[0] + df["Removed"].iloc[0]
        print(popSize)
        colnames = list(df.columns)
        colnames.pop(0)
        for i in colnames:
            df[i] = df[i].div(popSize)
        return df

    def normalizeRun(self, days: int, dt: float, accumulate=True) -> pd.DataFrame:
        df: pd.DataFrame
        if accumulate:
            df = self.accumulate(days, dt, plot=False)
            # calculate the population size
            popSize = df["Susceptible"].iloc[0] + df["Infected"].iloc[0] + df["Removed"].iloc[0]
            colnames = list(df.columns)
            # get rid of the days column in the list
            colnames.pop(0)
            for i in colnames:
                df[i] = df[i].div(popSize)
        else:
            df = self.run(days, dt, plot=False)
            # calculate the population size
            popSize = df["Susceptible"].iloc[0] + df["Infected"].iloc[0] + df["Removed"].iloc[0]
            colnames = list(df.columns)
            colnames.pop(0)
            for i in colnames:
                df[i] = df[i].div(popSize)
        return df

    # feed in the number of runs and the distributions that will be used
    def monteCarlo(self, numRuns: int, beta: np.random, gamma: np.random):
        # to be implemented
        pass


# Flow of the Compartmental Model:
# S -> I - > S
class SIS(CompartmentalModel):

    def __init__(self, beta, gamma, S0, I0):
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

    def _simulate(self, days: int, dt: float) -> tuple:
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

    @dispatch(int, float, plot=bool, Sbool=bool, Ibool=bool)
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


# Flow of the Compartmental Model:
# S -> I -> R, S- > V
class SIRV(SIR):

    def __init__(self, beta, gamma, rho, S0, I0, R0, V0):
        super(SIRV, self).__init__(beta, gamma, S0, I0, R0)
        self.V0 = V0
        self.rho = rho
        self.N = S0 + I0 + R0 + V0

    def changeV0(self, x: int):
        self.V0 = x
        self.N = self.S0 + self.I0 + self.R0 + self.V0

    def changeRho(self, x: int):
        self.rho = x

    def _deriv(self, s, i):
        # amount of people going from S -> I
        x = self.beta * s * i / self.N
        # amount of people going from I -> R
        y = self.gamma * i
        # amount of people going from S -> V after people left from S -> I
        z = self.rho * (s - x)
        return -x - z, x - y, y, z

    @dispatch(float, np.ndarray, np.ndarray, np.ndarray, np.ndarray)
    def _update(self, dt: float, S1, I1, R1, V1):
        # map arrays into these variables
        S, I, R, V = S1, I1, R1, V1
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
    def _includeVar(self, sx: bool, ix: bool, rx: bool, vx) -> list:
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


# Flow of the Compartmental Model'
# S -> E -> I -> R
class SEIR(SIR):

    def __init__(self, beta, EI, gamma, S0, E0, I0, R0):
        super(SEIR, self).__init__(beta=beta, gamma=gamma, S0=S0, I0=I0, R0=R0)
        # starting amount of exposed individuals
        self.E0 = E0
        # constant for going from E to I
        self.EI = EI
        self.N = S0 + E0 + I0 + R0

    def changeE0(self, x: int):
        self.E0 = x
        self.N = self.S0 + self.E0 + self.I0 + self.R0

    def changeEI(self, x: float):
        self.EI = x

    @dispatch(float, float, float)
    def _deriv(self, s, e, i):
        x = self.beta * s * i / self.N
        y = self.EI * e
        z = self.gamma * i
        return -x, x-y, y-z, z

    @dispatch(float, np.ndarray, np.ndarray, np.ndarray, np.ndarray)
    def _update(self, dt: float, S1: np.ndarray, E1: np.ndarray, I1: np.ndarray, R1: np.ndarray):
        S, E, I, R = S1, E1, I1, R1
        for i in range(1, len(S)):
            f = self._deriv(S[i-1], E[i-1], I[i-1])
            S[i] = S[i-1] + dt * f[0]
            E[i] = E[i-1] + dt * f[1]
            I[i] = I[i-1] + dt * f[2]
            R[i] = R[i-1] + dt * f[3]
        return S, E, I, R

    def _simulate(self, days: int, dt: float):
        # total number of iterations that will be run + the starting value at time 0
        size = int(days / dt + 1)
        # create the arrays to store the different values
        S, E, I, R = np.zeros(size), np.zeros(size), np.zeros(size), np.zeros()
        # initialize the arrays
        S[0], E[0], I[0], R[0] = self.S0, self.E0, self.I0, self.R0
        # run the Euler's Method
        S, E, I, R = self._update(dt, S, E, I, R)
        return S, E, I, R
