import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from .randMoveSEIRDV import RandMoveSEIRDV

class RandMoveSEIRSDV(RandMoveSEIRDV):

    def __init__(self, S0:int, E0:int, I0:int, R0:int, V0: int, rho: float, gamma: float, mu: float, eta:float, kappa: float, planeSize: float, move_r: float, sigma_R: float, 
        spread_r: float, sigma_r: float, days:int, w0=1.0, alpha=2.0, timeDelay=-1):
        super(RandMoveSEIRSDV, self).__init__(S0=S0, E0=E0, I0=I0, R0=0, V0=V0, rho=rho, gamma=gamma, mu=mu, eta=eta, planeSize=planeSize, move_r=move_r, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r,
        days=days)
        self.kappa = kappa
    
    def _RtoS(self):
        return self._changeHelp(self.Rcollect, self.kappa)
    
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
            RtoS = self._RtoS()
            # change the states of those in the transfer sets
            self._stateChanger(StoE, self.Ecollect, "E", i)
            self._stateChanger(EtoI, self.Icollect, "I", i)
            self._stateChanger(ItoR, self.Rcollect, "R", i)
            self._stateChanger(ItoD, self.Dcollect, "D", i)
            self._stateChanger(StoV, self.Vcollect, "V", i)
            self._stateChanger(RtoS, self.Scollect, "S", i)
            # modify the numbers
            self.S[i] = self.S[i-1] - len(StoE) - len(StoV) + len(RtoS)
            self.E[i] = self.E[i-1] + len(StoE) - len(EtoI)
            self.I[i] = self.I[i-1] + len(EtoI) - len(ItoR) - len(ItoD)
            #print("I[i-1]: ", self.I[i], " EtoI: ", len(EtoI), " ItoR: ", len(ItoR), " ItoD: ", len(ItoD), "I[i]: ", self.I[i], "Sum: ", self.I[i-1] + len(EtoI) - len(ItoR) - len(ItoD))
            self.R[i] = self.R[i-1] + len(ItoR) - len(RtoS)
            self.V[i] = self.V[i-1] + len(StoV)
            self.D[i] = self.D[i-1] + len(ItoD)
            # move everyone except dead compartment
            self._move(i, [self.Scollect, self.Ecollect, self.Icollect, self.Rcollect, self.Vcollect])
            #print("i: ", i, "(", self.S[i], ",",self.E[i],",", self.I[i],",", self.R[i], ",", self.D[i], ")")
        if getDetails:
            return self.details
    
    def plot(self):
        t = np.linspace(0,self.days, self.days+1)
        fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(nrows=6, sharex="all")
        ax1.set_title("Random Movement SEIRSDV")
        ax6.set_xlabel("Days")
        ax1.set_ylabel('# Susceptibles')
        ax1.plot(t, self.S, label="Susceptibles", color='r')
        ax2.set_ylabel("# Exposed")
        ax2.plot(t, self.E, label="Exposed", color='g')
        ax3.set_ylabel("# Infected")
        ax3.plot(t, self.I, label="Infected")
        ax4.set_ylabel("# Recovered")
        ax4.plot(t, self.R, label="Recovered", color='c')
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