from .spatial import Spatial
from src.utility import Person
import src.utility as u

# class that operates under the hub model assumptions
class Hub(Spatial):

    def __init__(self, popsize: int, pss: float, rstart: float, alpha: int, side: float, S0: int, I0: int, days: int, w0=1.0,
                 hubConstant=6 ** 0.5):
        super(Hub, self).__init__(popsize, pss, rstart, alpha, side, S0=S0, I0=I0, days=days, w0=w0)
        self.hubConstant = hubConstant

    def _infect(self, inf: Person, sus: Person):
        # compute the distance between two Person objects
        r = u.dist(inf, sus)
        # make variable that can potentially be changed if someone is a super spreader
        r0 = self.rstart
        # if the infectious individual is a super spreader
        if inf.ss:
            # multiply by the hub constant, which is an assumption of the hub model
            r0 *= self.hubConstant

        if r > r0:
            # if the person is outside the range
            return 0
        else:
            # use the formula: w(r) = w0 * (1-r/rn)^alpha
            return self.w0 * (1 - r / r0) ** self.alpha

