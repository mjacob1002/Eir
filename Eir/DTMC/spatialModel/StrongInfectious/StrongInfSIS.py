from ..Hub.HubSIS import HubSIS
from Eir.utility import Person
from Eir.utility import dist


class StrongInfSIS(HubSIS):
    def __init__(self, pss: float, rstart: float, side: float, S0: int, I0: int, days: int,
                 gamma: float, w0=1.0, alpha=2.0):
        # error checking
        self.intCheck([S0, I0, days])
        self.floatCheck([pss, rstart, side, gamma, w0, alpha])
        self.negValCheck([S0, I0, pss, rstart, side, days, gamma, w0, alpha])
        self.probValCheck([pss, gamma, w0])
        # call the super constructor
        super(StrongInfSIS, self).__init__(pss=pss, rstart=rstart, alpha=alpha, side=side, S0=S0, I0=I0, days=days,
                                           gamma=gamma, w0=w0,
                                           hubConstant=0)

    # the only assumption that changes in the strong infectious model is the formula for infection probability
    def _infect(self, inf: Person, sus: Person):
        # compute the distance between two Person objects
        r = dist(inf, sus)
        # make variable that can potentially be changed if someone is a super spreader
        r0 = self.rstart
        # if the susceptible is too far away from the infectious person
        if r > r0:
            return 0
        # in range of the infected person
        if inf.ss:
            return self.w0
        # return using the normal probability function if not a super spreader
        return self.w0 * (1 - r / r0) ** self.alpha
