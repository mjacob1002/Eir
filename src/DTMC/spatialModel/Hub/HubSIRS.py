from .HubSIR import HubSIR
import numpy as np
import src.utility as u


class HubSIRS(HubSIR):

    def __init__(self, popsize: int, pss: float, rstart: float, alpha: int, side: float, S0: int, I0: int, R0: int,
                 days: int,
                 gamma: float, kappa: float, w0=1.0,
                 hubConstant=6 ** 0.5):
        self.kappa = kappa
        super(HubSIRS, self).__init__(popsize, pss, rstart, alpha, side, S0, I0, R0, days, gamma, w0, hubConstant)

    # run transfers from R to S
    def _RS(self):
        # set that keeps track of the indices of people that changed states
        transfers = set()
        for count, inf in enumerate(self.Rcollect):
            if not inf.isIncluded:
                continue
            event = u.randEvent(self.gamma)
            if not event:
                continue
            self.Rcollect[count].isIncluded = False
            transfers.add(count)
        return transfers

    def run(self):
        # for the days 1 to day
        for i in range(1, self.days + 1):
            # run the transfers from different compartments
            transferSI = self._StoI()
            transferIr = self._ItoR()
            transferRS = self._RS()
            # go after and change the indices in the collection data structure thing
            # S to I
            for index in transferSI:
                self.Icollect[index].isIncluded = True
            # I to R
            for index in transferIr:
                self.Rcollect[index].isIncluded = True
            # R to S
            for index in transferRS:
                self.Scollect[index].isIncluded = True
            # change the number of people in each state on the day i by adjusting the previous day's count
            self.S[i] = self.S[i - 1] - len(transferSI) + len(transferRS)
            self.I[i] = self.I[i - 1] + len(transferSI) - len(transferIr)
            self.R[i] = self.R[i - 1] + len(transferIr) - len(transferRS)
