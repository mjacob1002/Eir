from .spatial import Spatial
from Eir.src.simulation.utility import Person
from Eir.src.simulation.utility import dist


class StrongInfect(Spatial):
    def __init__(self, popsize: int, pss: float, rstart: float, alpha: int, side: float, S0:int, I0:int, w0: float):
        super(StrongInfect, self).__init__(popsize, pss, rstart, alpha, side, S0, I0, w0)

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

    