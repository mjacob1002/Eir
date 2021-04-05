from .spatial import Spatial
from Eir.utility import Person
import Eir.utility as u

# class that operates under the hub model assumptions
class Hub(Spatial):
    """
    Hub Model Abstract Class. Implements the _infect function according to the Hub Model presumptions of 
    Fujie & Odagaki.

    Parameters
    ---------

    popsize: int

    pss: float

    rstart: float

    alpha : int

    side: float

    S0: int

    I0: int

    days: int

    w0: float optional

    hubConstant: float optional
        The constant used when expanding the spreading radius of a super spreader. 

    """
    def __init__(self, popsize: int, pss: float, rstart: float, alpha: int, side: float, S0: int, I0: int, days: int, w0=1.0,
                 hubConstant=6 ** 0.5):
        super(Hub, self).__init__(popsize, pss, rstart, alpha, side, S0=S0, I0=I0, days=days, w0=w0)
        self.hubConstant = hubConstant

    def _infect(self, inf: Person, sus: Person):
        """
        Method that generates the infection probability given an infectious person inf and a susceptible person sus.

        Parameters
        ----------

        inf: Person
            The infectious person of the two.

        sus: Person
            The susceptible person of the two. 

        Returns
        -------

        float
            Represents the probability that inf will infect sus given the distance between the two and 
            inf's spreading radius. 
        """
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
        
    def _changeHelp(self, collect:list, prob: float):
        return u.static_prob_help(collect, prob)

    # used to run the state changes
    def _stateChanger(self, values: set, collect: list, symbol: str, day:int):
        """
        Takes care of the state changes to a particular state. 

        Parameters
        ----------

        values: set
            values contains all of the indices of the people who need to be set to isIncluded=True in the collect list
        
        collect: list
            The particular list of Person objects that are going to be modified.
        
        symbol: str 
            The string representing the particular state that is going to. Used for details.
        
        day: int
            The day on which the transfer happened. Used for details.
        """
        for index in values:
            #print("Index: ", index)
            collect[index].isIncluded = True
            self.details.addStateChange(index, symbol, day)