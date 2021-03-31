import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from .randMoveSEIRD import RandMoveSEIRD
from src.utility import Person1 as Person

class RandMoveSEIRDV(RandMoveSEIRD):
    def __init__(self, S0:int, E0:int, I0:int, R0:int, V0: int, rho: float, gamma: float, mu: float, eta:float, planeSize: float, move_r: float, sigma_R: float, 
        spread_r: float, sigma_r: float, days:int, w0=1.0, alpha=2.0, timeDelay=-1):
        super(RandMoveSEIRDV, self).__init__(S0=S0, E0=E0, I0=I0, R0=0, rho=rho, gamma=gamma, mu=mu, planeSize=planeSize, move_r=move_r, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r,
        days=days)
        self.eta = eta
        self.timeDelay = timeDelay
        self.Scollect, self.Ecollect, self.Icollect, self.Rcollect, self.Vcollect, self.Dcollect = [], [], [], [], [], []
        self.popsize += V0
        self.V = np.zeros(self.days+1)
        loc_x, loc_y, spreading_r = np.random.random(self.popsize)*planeSize, np.random.random(self.popsize)*planeSize, np.random.normal(spread_r, sigma_r, self.popsize)
        for i in range(self.popsize):
            persons = []
            for j in range(6):
                persons.append(Person(loc_x[i], loc_y[i], 0, spreading_r[i]))
            if i < S0:
                persons[0].isIncluded=True
                self.details.addStateChange(i, "S", 0)
            elif i< S0 + E0:
                persons[1].isIncluded=True
                self.details.addStateChange(i, "E", 0)
            elif i< S0 + E0 + I0:
                persons[2].isIncluded=True
                self.details.addStateChange(i, "I", 0)
            elif i< S0 + E0 + I0 + R0:
                persons[3].isIncluded=True
                self.details.addStateChange(i, "R", 0)
            else:
                persons[4].isIncluded=True
                self.details.addStateChange(i, "V", 0)
            self.Scollect.append(persons[0])
            self.Ecollect.append(persons[1])
            self.Icollect.append(persons[2])
            self.Rcollect.append(persons[3])
            self.Vcollect.append(persons[4])
            self.Dcollect.append(persons[5])
    
    def _StoV(self):
        return self._changeHelp(self.Scollect, self.eta)
    
    def run(self, getDetails=True):
        for i in range(1, self.days+1):
            # run the state changes and get the transfer sets
            StoE = self._StoE(i)
            StoV = set()
            if i > self.timeDelay:
                StoV = self._StoV()
            EtoI = self._EtoI()
            ItoR = self._ItoR()
            ItoD = self._ItoD()
            # change the states of those in the transfer sets
            self._stateChanger(StoE, self.Ecollect, "E", i)
            self._stateChanger(EtoI, self.Icollect, "I", i)
            self._stateChanger(ItoR, self.Rcollect, "R", i)
            self._stateChanger(ItoD, self.Dcollect, "D", i)
            self._stateChanger(StoV, self.Vcollect, "V", i)
            # modify the numbers
            self.S[i] = self.S[i-1] - len(StoE) - len(StoV)
            self.E[i] = self.E[i-1] + len(StoE) - len(EtoI)
            self.I[i] = self.I[i-1] + len(EtoI) - len(ItoR) - len(ItoD)
            #print("I[i-1]: ", self.I[i], " EtoI: ", len(EtoI), " ItoR: ", len(ItoR), " ItoD: ", len(ItoD), "I[i]: ", self.I[i], "Sum: ", self.I[i-1] + len(EtoI) - len(ItoR) - len(ItoD))
            self.R[i] = self.R[i-1] + len(ItoR)
            self.V[i] = self.V[i-1] + len(StoV)
            self.D[i] = self.D[i-1] + len(ItoD)
            # move everyone except dead compartment
            self._move(i, [self.Scollect, self.Ecollect, self.Icollect, self.Rcollect, self.Vcollect])
            #print("i: ", i, "(", self.S[i], ",",self.E[i],",", self.I[i],",", self.R[i], ",", self.D[i], ")")
        if getDetails:
            return self.details

    def toDataFrame(self):
        """
        Convert the data to a dataframe.
        
        Returns
        -------

        pd.DataFrame
            Holds the data of simulation in a DataFrame format.
        """
        t = np.linspace(0,self.days,self.days+1)
        arr = np.stack([t, self.S, self.E, self.I, self.R, self.D, self.V], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Exposed", "Infected", "Recovered", "Dead", "Vaccinated"])
        return df
    
    def plot(self):
        t = np.linspace(0,self.days, self.days+1)
        fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(nrows=6, sharex="all")
        ax1.set_title("Random Movement SEIRDV")
        ax6.set_xlabel("Days")
        ax1.set_ylabel('# Susceptibles')
        ax1.plot(t, self.S, label="Susceptibles")
        ax2.set_ylabel("# Exposed")
        ax2.plot(t, self.E, label="Exposed")
        ax3.set_ylabel("# Infected")
        ax3.plot(t, self.I, label="Infected")
        ax4.set_ylabel("# Recovered")
        ax4.plot(t, self.R, label="Recovered")
        ax5.set_ylabel("# Dead")
        ax5.plot(t, self.D, label='Dead')
        ax6.set_ylabel("# Vaccinated")
        ax6.plot(t, self.V, label="Vaccinated")
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        ax5.legend()
        ax6.legend()
        plt.show()