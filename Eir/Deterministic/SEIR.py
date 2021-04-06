from .SIR import SIR
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from multipledispatch import dispatch


# Flow of the Compartmental Model'
# S -> E -> I -> R
class SEIR(SIR):
    """
    Deterministic SEIR model that allows one to use constant values to generate plot.

    Parameters
    ----------

    beta: float
        Represents the effective transmission rate between people.
    
    rho: float
        The proportion of people that go from E to I. 
    
    gamma: float
        The proportion of people that go from I to R.
    
    S0: int
        The initial number of susceptible individuals.
    
    E0: int
        The initial number of exposed individuals.
    
    I0: int
        The initial number of infected individuals.
    
    R0: int
        The initial number of removed individuals.

    """
    def __init__(self, beta, rho, gamma, S0, E0, I0, R0):
        self.intCheck([S0, E0, I0, R0])
        self.floatCheck([beta, rho, gamma, S0, E0, I0, R0])
        self.negValCheck([beta, rho, gamma, S0, E0, I0, R0])
        self.probCheck([rho, gamma])
        super(SEIR, self).__init__(beta=beta, gamma=gamma, S0=S0, I0=I0, R0=R0)
        # starting amount of exposed individuals
        self.E0 = E0
        # constant for going from E to I
        self.rho = rho
        self.N = S0 + E0 + I0 + R0

    def changeE0(self, x: int):
        self.E0 = x
        self.N = self.S0 + self.E0 + self.I0 + self.R0

    def changeRho(self, x: float):
        self.rho = x

    @dispatch(float, float, float)
    def _deriv(self, s, e, i):
        """ 
        Calculates the derivatives

        Parameters
        ----------
        s: float
            The current number of susceptible individuals at the time the derivative is taken, as according to ODEs.
        
        e: float
            The current number of exposed individuals at the time derivative is taken, as according to ODEs.
        
        i: float
            The current number of infected individuals at the time derivative is taken, as according to ODEs.
        
        Returns
        -------

        tuple:
            contains the derivatives S, E, I, and R arrays.

        """
        x = self.beta * s * i / self.N
        y = self.rho * e
        z = self.gamma * i
        return -x, x - y, y - z, z

    @dispatch(float, np.ndarray, np.ndarray, np.ndarray, np.ndarray)
    def _update(self, dt: float, S: np.ndarray, E: np.ndarray, I: np.ndarray, R: np.ndarray):
        """
        Uses Euler's method to update the array values.

        Parameters
        ----------

        dt: float
            The small differential used for Euler's method
        
        S: ndarray
            The array that will hold the S values

        E: ndarray
            The array that will hold the E values
        
        I: ndarray
            The array that will hold the I values
        
        R: ndarray
            The array that will hold the R values

        """
        for i in range(1, len(S)):
            f = self._deriv(S[i - 1], E[i - 1], I[i - 1])
            S[i] = S[i - 1] + dt * f[0]
            E[i] = E[i - 1] + dt * f[1]
            I[i] = I[i - 1] + dt * f[2]
            R[i] = R[i - 1] + dt * f[3]
        return S, E, I, R

    def _simulate(self, days: int, dt: float):
        """ 
        Runs the simulation.

        Parameters
        ----------

        days: int
            The number of days to be simulated.
        
        dt: float
            The differential used for Euler's method.
        
        Returns
        -------

        ndarray:
            The array that will hold the S values

        ndarray:
            The array that will hold the E values
        
        ndarray:
            The array that will hold the I values
        
        ndarray:
            The array that will hold the R values
        """
        self.floatCheck([days, dt])
        self.negValCheck([days, dt])
        # total number of iterations that will be run + the starting value at time 0
        size = int(days / dt + 1)
        # create the arrays to store the different values
        S, E, I, R = np.zeros(size), np.zeros(size), np.zeros(size), np.zeros(size)
        # initialize the arrays
        S[0], E[0], I[0], R[0] = self.S0, self.E0, self.I0, self.R0
        # run the Euler's Method
        S, E, I, R = self._update(dt, S, E, I, R)
        return S, E, I, R
    

    def _includeVar(self, sx: bool, ex: bool, ix: bool, rx: bool):
        # list of the strings that will be returned and then passed into plot function
        labels = []
        # if the user wants to plot susceptible
        if sx:
            labels.append("Susceptible")
        # if the user wants to plot infected
        if ex:
            labels.append("Exposed")
        if ix:
            labels.append("Infected")
        # if the user wants to plot removed
        if rx:
            labels.append("Removed")
        return labels

    def run(self, days: int, dt: float, plot=True, Sbool=True, Ebool=True, Ibool=True, Rbool=True):
        """
        Runs the actual simulation; user method.

        days: int
            The number of days being simulated.
        
        dt: float
            The differential used for Euler's method.
        
        plot: bool optional
            Default is True. Determines whether dataframe is plotted.
        
        Sbool: bool optional
            Default is True. Determines whether Susceptible is plotted.

        Ebool: bool optional
            Default is True. Determines whether exposed is plotted.

        Ibool: bool optional
            Default is True. Determines whether infected is plotted.

        Rbool: bool optional
            Default is True. Determines whether recovered is plotted.
        
        Returns
        -------

        pd.DataFrame
            DataFrame containing data of the simulation.
        
        Matplotlib.pyplot.Figure
            Only if plot=True

        """
        self.floatCheck([days, dt])
        self.negValCheck([days, dt])
        # creates evenly spaced array that spans day 0 to the day wanted
        t = np.linspace(0, days, int(days / dt) + 1)
        S, E, I, R = self._simulate(days, dt)
        # makes a dictionary so that it can be easily converted to a dataframe
        data1 = {
            "Days": t,
            "Susceptible": S,
            "Exposed": E,
            "Infected": I,
            "Removed": R
        }
        # create the labels that will be the columns of the dataframe
        label = ["Days", "Susceptible", "Exposed", "Infected", "Removed"]
        # create a dataframe
        df = pd.DataFrame(data=data1, columns=label)
        # if the plot boolean is true aka they want a plot to be shown
        if plot:
            # determine what should be plotted
            included = self._includeVar(Sbool, Ebool, Ibool, Rbool)
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
        """ 
        Does everything run does except gather total cases, or everyone who has been infected, which means I + R.
        
        Parameters
        ---------

        days: int
            Number of days being simulated.
        
        dt: float
            The differential used for Euler's method
        
        plot: bool optional
            Default is True. Plots the dataframe if true.
        
        Returns
        -------

        pd.DataFrame
            Contains information of the simulation.
        """
        self.floatCheck([days, dt])
        self.negValCheck([days, dt])
        t = np.linspace(0, days, int(days / dt) + 1)
        S, E, I, R = self._simulate(days, dt)
        # create a numpy array that will hold all of the values
        cases = np.zeros(len(I))
        # add up the total infected and removed at given time to account for everyone with the virus
        for i in range(len(I)):
            cases[i] = I[i] + R[i]
        # create a dictionary that holds the data for easy conversion to dataframe
        data1 = {
            "Days": t,
            "Susceptible": S,
            "Exposed": E, 
            "Infected": I,
            "Removed": R,
            "Total Cases": cases
        }
        # create the column labels
        labels = ['Days', "Susceptible", "Exposed", "Infected", "Removed", "Total Cases"]
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
