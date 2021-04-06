from .SIR import SIR
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from multipledispatch import dispatch


class SIRS(SIR):
    """
    SIRS deterministic model.

    Parameters
    ----------

    beta: float
        Effective transmission rate of an infectious person, on average.
    
    gamma: float
        Proportion of people that go from I to R.
    
    kappa: float
        Proportion of people that go from R to S
    
    S0: int
        Initial susceptibles at the start of the simulation.
    
    I0: int
        Initial infecteds at the start of the simulation.
    
    R0: int
        Initial recovereds at the start of the simulation.
    """
    def __init__(self, beta: float, gamma: float, kappa: float, S0, I0, R0):
        # error checking 
        self.intCheck([S0, I0, R0])
        self.floatCheck([beta, gamma, kappa, S0, I0, R0])
        self.negValCheck([beta, gamma, kappa, S0, I0, R0])
        self.probCheck([gamma, kappa])
        # call the superclass constructor
        super(SIRS, self).__init__(beta, gamma, S0, I0, R0)
        # map kappa to a class variable
        self.kappa = kappa

    # if you want to modify the kappa value
    def changeKappa(self, x: float):
        self.kappa = x

    @dispatch(float, float, float)
    def _deriv(self, s, i, r):
        # doing all of the changes from SIR model
        a, b, c = super(SIRS, self)._deriv(s, i)
        # compute the people becoming resusceptible from the R compartment
        k = r * self.kappa
        # return the values in S, I, R, accumulation format
        return a + k, b, c - k

    # run Euler 's method, when accumulating cases, which is different from usual
    @dispatch(float, float, float)
    def _derivAccumulate(self, s, i, r):
        # doing all of the changes from SIR model
        a, b, c = super(SIRS, self)._deriv(s, i)
        # compute the people becoming resusceptible from the R compartment
        k = r * self.kappa
        # return the values in S, I, R, accumulation format
        return a + k, b, c - k, -a
        #

    # update function adjusted for accumulation of cases
    def _updateAccumulate(self, dt, S, I, R, cases):
        # for all the days that ODE will be solved
        for i in range(1, len(S)):
            f = self._derivAccumulate(S[i - 1], I[i - 1], R[-1])
            S[i] = S[i - 1] + dt * f[0]
            I[i] = I[i - 1] + dt * f[1]
            R[i] = R[i - 1] + dt * f[2]
            cases[i] = cases[i - 1] + dt * f[3]
        return S, I, R, cases

    # _simulate function adjusted for the accumulation of cases
    def _simulateAccumulate(self, days: int, dt: float):
        # total number of iterations that will be run + the starting value at time 0
        size = int(days / dt + 1)
        # create the arrays to store the different values
        S, I, R, case = np.zeros(size), np.zeros(size), np.zeros(size), np.zeros(size)
        # initialize the arrays
        S[0], I[0], R[0], case[0] = self.S0, self.I0, self.R0, self.I0
        # run the Euler's Method
        S, I, R, case = self._updateAccumulate(dt, S, I, R, cases=case)
        return S, I, R, case

    # runs Euler's Method
    @dispatch(float, np.ndarray, np.ndarray, np.ndarray)
    def _update(self, dt, S, I, R) -> tuple:
        # for all the days that ODE will be solved
        for i in range(1, len(S)):
            f = self._deriv(S[i - 1], I[i - 1], R[i - 1])
            S[i] = S[i - 1] + dt * f[0]
            I[i] = I[i - 1] + dt * f[1]
            R[i] = R[i - 1] + dt * f[2]
        return S, I, R

    # does the work of initializing arrays and then updating the arrays using Euler's method
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

    # function uses to determine the total number of cases cumulatively
    def accumulate(self, days: int, dt: float, plot=True):
        self.floatCheck([days, dt])
        self.negValCheck([days, dt])
        # create a linrange object
        t = np.linspace(0, days, int(days / dt) + 1)
        # return the S, I, R, and accumulated cases
        S, I, R, cases = self._simulateAccumulate(days, dt)
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


#test = SIRS(beta=1.5, gamma=.3, kappa=.05, S0=99999, I0=1, R0=0)
#x = test.accumulate(31, .1)
#print(x)
