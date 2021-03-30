import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from .randMoveSIRDV import RandMoveSIRDV

class RandMoveSIRSDV(RandMoveSIRDV):

    def __init__(self, S0, I0, R0, V0, gamma, mu, eta, kappa, planeSize, move_r:float, sigma_R:float, spread_r:float, sigma_r: float, days:int, w0=1.0, alpha=2.0, timeDelay=-4):
        super(RandMoveSIRSDV, self).__init__(S0=S0, I0=I0, R0=R0, V0=V0, gamma=gamma, mu=mu, eta=eta, planeSize=planeSize, move_r=move_r, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r, days=days, timeDelay=4)
        self.kappa = kappa
    
    def _RtoS(self):
        return self._changeHelp(self.Rcollect, self.kappa)
    
    def run(self, getDetails=True):
        """
        Run the actual simulation. 

        Parameters
        ----------

        getDetails: bool optional
            If getDetails=True, then run will return a Simul_Details object which will allow the user to 
            examine details of the simulation that aren't immediately obvious.
        
        Returns
        -------

        Simul_Details:
            Allows the user to take a deeper look into the dynamics of the simulation by examining transmission
            chains. User can also examine transmission history and state changes of individuals in the object
            by utilizing the Simul_Details object. 
        """

        # for all the days in the simulation
        for i in range(1, self.days+1):
            print("Day ", i)
            #print("Location: (", self.Scollect[0].x, ",", self.Scollect[0].y, ").")
            # run the state changes
            StoI = self._StoI(i)
            StoV = set()
            if i > self.timeDelay:
                StoV = self._StoV()
            ItoR = self._ItoR()
            ItoD = self._ItoD()
            RtoS = self._RtoS()
            # change the indices of the transfers
            self._stateChanger(StoI, self.Icollect, "I", i)
            self._stateChanger(ItoR, self.Rcollect, "R", i)
            self._stateChanger(ItoD, self.Dcollect, "D", i)
            self._stateChanger(StoV, self.Vcollect, "V", i)
            self._stateChanger(RtoS, self.Scollect, "S", i)
            
            # make everyone move randomly, don't move dead people
            self._move(i, [self.Scollect, self.Icollect, self.Rcollect, self.Vcollect])
            # change the values in the arrays
            self.S[i] = self.S[i-1] - len(StoI) - len(StoV) + len(RtoS)
            self.I[i] = self.I[i-1] + len(StoI) - len(ItoR) - len(ItoD)
            self.R[i] = self.R[i-1] + len(ItoR) - len(RtoS)
            self.V[i] = self.V[i-1] + len(StoV)
            self.D[i] = self.D[i-1] + len(ItoD)
        if getDetails:
            return self.details
    
    def plot(self):
        t = np.linspace(0,self.days, self.days+1)
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_title("Random Movement SIRSDV")
        ax1.set_ylabel("# Susceptibles")
        ax2.plot(t, self.I, label="Infected", color='g')
        ax2.set_ylabel("# Active Cases")
        ax3.plot(t, self.R, label="Recovered", color='c')
        ax3.set_ylabel("# Recovered")
        ax4.plot(t, self.V, label="Vaccinated", color='b')
        ax4.set_ylabel("# Vaccinated")
        ax5.set_xlabel("Days")
        ax5.set_ylabel("# Dead")
        ax5.plot(t, self.D, label="Dead")
        plt.show()