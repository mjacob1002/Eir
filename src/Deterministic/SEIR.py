from .SIR import SIR
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from multipledispatch import dispatch


# Flow of the Compartmental Model'
# S -> E -> I -> R
class SEIR(SIR):

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
        x = self.beta * s * i / self.N
        y = self.rho * e
        z = self.gamma * i
        return -x, x - y, y - z, z

    @dispatch(float, np.ndarray, np.ndarray, np.ndarray, np.ndarray)
    def _update(self, dt: float, S: np.ndarray, E: np.ndarray, I: np.ndarray, R: np.ndarray):
        for i in range(1, len(S)):
            f = self._deriv(S[i - 1], E[i - 1], I[i - 1])
            S[i] = S[i - 1] + dt * f[0]
            E[i] = E[i - 1] + dt * f[1]
            I[i] = I[i - 1] + dt * f[2]
            R[i] = R[i - 1] + dt * f[3]
        return S, E, I, R

    def _simulate(self, days: int, dt: float):
        # total number of iterations that will be run + the starting value at time 0
        size = int(days / dt + 1)
        # create the arrays to store the different values
        S, E, I, R = np.zeros(size), np.zeros(size), np.zeros(size), np.zeros(size)
        # initialize the arrays
        S[0], E[0], I[0], R[0] = self.S0, self.E0, self.I0, self.R0
        # run the Euler's Method
        S, E, I, R = self._update(dt, S, E, I, R)
        return S, E, I, R
