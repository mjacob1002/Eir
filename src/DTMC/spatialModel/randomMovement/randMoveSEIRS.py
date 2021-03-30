import numpy as np

from src.utility import randEvent
from .randMoveSEIR import RandMoveSEIR

class RandMoveSEIRS(RandMoveSEIR):

    def __init__(self, S0:int, E0:int, I0:int, R0:int, rho:float, gamma:float, kappa:float, planeSize:float, move_r:float, sigma_R:float, spread_r:float, sigma_r: float, days:int, w0=1.0, alpha=2.0):
        super(RandMoveSEIRS, self).__init__(S0=S0, E0=E0, I0=I0, R0=R0, rho=rho, gamma=gamma, planeSize=planeSize, move_r=move_r, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r, days=days, w0=w0, alpha=alpha)
        self.kappa = kappa

    def _RtoS(self):
        transfers = set()
        for i, person in enumerate(self.Rcollect):
            if not person.isIncluded:
                continue
            event = randEvent(self.kappa)
            if not event:
                continue
            self.Rcollect[i].isIncluded=False
            transfers.add(i)
        return transfers
    
    def run(self, getDetails=True):
        # run the simulation for the number of days
        for i in range(1, self.days+1):
            # run the state change to determine who moves between compartments
            StoE = self._StoE(i)
            EtoI = self._EtoI()
            ItoR = self._ItoR()
            RtoS = self._RtoS()
            # actually move the people between compartments
            self._stateChanger(StoE, self.Ecollect, "E", i)
            self._stateChanger(EtoI, self.Icollect, "I", i)
            self._stateChanger(ItoR, self.Rcollect, "R", i)
            self._stateChanger(RtoS, self.Scollect, "S", i)
            # move the people in the simulation
            self._move(i, [self.Scollect, self.Ecollect, self.Icollect, self.Rcollect])
            # modify the number of people in each compartment
            self.S[i] = self.S[i-1] - len(StoE) + len(RtoS)
            self.E[i] = self.E[i-1] + len(StoE) - len(EtoI)
            self.I[i] = self.I[i-1] + len(EtoI) - len(ItoR)
            self.R[i] = self.R[i-1] + len(ItoR) - len(RtoS)
        if getDetails:
            return self.details
        