from .spatial import Spatial
from Eir.utility import Person
from Eir.utility import dist


class StrongInfect(Spatial):
    """
    Contains the same attributes as the Spatial base class. The only difference is in the _infect function,
    where implementation is different according to the Strong Infectious model presumptions. One difference is
    the w0 variable is defaulted to 0.5 if no value is passed in. This model assumes that super spreaders are
    intrinsically more infectious and therefore have a constant probability of infection within their spreading
    radius.
    """
    def __init__(self, popsize: int, pss: float, rstart: float, alpha: int, side: float, S0:int, I0:int, w0: float):
        super(StrongInfect, self).__init__(popsize, pss, rstart, alpha, side, S0, I0, w0=0.5)

    def _infect(self, inf: Person, sus: Person):
        """
        Implementation of _infect method. Assumes that super spreders have constant probability of infection
        while the susceptible is within their spreading radius. If infectious person is normal spreader,

        Parameters
        ---------

        inf: Person
            infectious person.

        sus: Person
            susceptible person
        
        Returns
        -------
        
        float:
            probability that infectious person infects the susceptible person. 
        """
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

    