from Eir.Deterministic.CompartmentalModel import CompartmentalModel
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from multipledispatch import dispatch


class SIR(CompartmentalModel):
    # beta is the transmission rate, gamma is the recovery rate
    # S0, I0, R0 are the starting Susceptible, infected, and removed people respectively
    """ SIR Deterministic Model 
    
    Parameters
    ----------

    beta: float
        Effective transmission rate of infected people, on average.
    
    gamma: float
        Proportion of I that goes to R.
    
    S0: int
        Initial susceptibles.
    
    I0: int
        Initial infecteds.
    
    R0: int
        Initial removed.
    
    """
    
    def __init__(self, beta: float, gamma: float, S0: int, I0: int, R0: int):
        # run error checks
        self.intCheck([S0, I0, R0])
        self.floatCheck([beta, gamma, S0, I0, R0])
        self.negValCheck([beta, gamma, S0, I0, R0])
        self.probCheck([gamma])
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
    def _deriv(self, s, i):
        # x is the amount of leaving S compartment and entering I
        x = self.beta * s * i / self.N
        # y is the amount leaving I compartment and entering R compartment
        y = self.gamma * i
        return -x, x - y, y

    # runs Euler's Method
    @dispatch(float, np.ndarray, np.ndarray, np.ndarray)
    def _update(self, dt, S, I, R):
        # for all the days that ODE will be solved
        for i in range(1, len(S)):
            f = self._deriv(S[i - 1], I[i - 1])
            S[i] = S[i - 1] + dt * f[0]
            I[i] = I[i - 1] + dt * f[1]
            R[i] = R[i - 1] + dt * f[2]
        return S, I, R

    # combines the Euler's Method with all initialization and stuff and runs full simulation
    # days is the number of days being simulated, dt is the step size for Euler's method
    def _simulate(self, days: int, dt: float):
        # total number of iterations that will be run + the starting value at time 0
        size = int(days / dt + 1)
        # create the arrays to store the different values
        S, I, R = np.zeros(size), np.zeros(size), np.zeros(size)
        # initialize the arrays
        S[0], I[0], R[0] = self.S0, self.I0, self.R0
        # run the Euler's Method
        S, I, R = self._update(dt, S, I, R)
        return S, I, R

    def _includeVar(self, sx: bool, ix: bool, rx: bool):
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
        self.floatCheck([days, dt])
        self.negValCheck([days, dt])
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
        self.floatCheck([days, dt])
        self.negValCheck([days, dt])
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
    def normalizeDataFrame(self, df: pd.DataFrame):
        """ 
        Divide all of the columns by the total population in order to get numbers as a proportion of population.
        
        Parameters
        ----------

        df: pd.DataFrame
            The dataframe to be normalized
        
        Returns
        -------

        pd.DataFrame
            Normalized dataframe.
        """
        colnames = list(df.columns)
        colnames.pop(0)
        for i in colnames:
            df[i] = df[i].div(self.N)
        return df

    def normalizeRun(self, days: int, dt: float, accumulate=True):
        """
        Does a normalized run of the simulation.

        Parameters
        ---------

        days: int
            Number of days being simulated.
        
        dt: float
            The differential used for Euler's method.

        """
        df: pd.DataFrame
        if accumulate:
            df = self.accumulate(days, dt, plot=False)
            colnames = list(df.columns)
            # get rid of the days column in the list
            colnames.pop(0)
            for i in colnames:
                df[i] = df[i].div(self.N)
        else:
            df = self.run(days, dt, plot=False)
            colnames = list(df.columns)
            colnames.pop(0)
            for i in colnames:
                df[i] = df[i].div(self.N)
        return df


