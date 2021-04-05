import numpy as np
import matplotlib.pyplot as plt

from ..Hub.Hub_ICUV import Hub_ICUV
from Eir.utility import Person, dist

class StrongInf_ICUV(Hub_ICUV):
    """
        Runs a simulation using the Strong Infectious Model for an ICU Compartmental Model.

        Parameters
        ----------
        S0 : int
            The starting number of susceptible individuals in the simulation.
        
        E0: int
            The starting number of exposed individuals in the simulation.
        
        I0: int
            The starting number of infected individuals in the simulation.

        R0: int
            The starting number of recovered individuals in the simulation.
        
        V0: int
            The starting number of vaccinated individuals in the simulation.
        
        rho: float
            The probability of an individual leaving the E compartment.
        
        ioda: float
            The probability that, given an individual is leaving the E compartment, he goes to L compartment. The probability of that person going to I compartment is (1-ioda).
        
        gamma: float
            The probability of a person in I compartment going to the R compartment
        
        mu: float
            The probability of going from I to D, given that the person didn't go from I to R.
        
        phi: float
            The probability of going from L compartment to ICU compartment.
        
        chi: float
            The probability of going from ICU compartment to R compartment.
        
        omega: float
            The probability of going from ICU compartment to D compartment, given that individual didn't go from ICU compartment to R compartment.
        
        kappa: float
            The probability of going from R compartment to S compartment.
        
        eta: float 
            The probability of going from S compartment to V compartment, given that the individual didn't go from S compartment to E compartment. 
        
        rstart: float
            The spreading radius of a normal spreader. 
        
        pss: float
            The probability that, at the beginning of the simulation, the randomly generated individual is a super spreader.
        
        side: float
            The length of one side of the square plane that the individuals are confined to.
        
        days: int
            The number of days that the simulations lasts for.
        
        alpha: float, optional
            A constant used in the formula for calculating probability of infection between infectious person and susceptible person. Default is 2.0.
        
        w0: float, optional
            The probability of a susceptible being infected by an infectious individual if they are 0 units apart. Default is 0.7.

        
        timeDelay: float, optional
            The amount of days for which the vaccine rollout is delayed. Checks the day and makes sure that the day > timeDelay before simulating vaccine distribution. Default is -1.

        Attributes
        ----------

        Scollect, Ecollect, Icollect, Lcollect, ICUcollect, Rcollect, Dcollect, Vcollect: list
            Lists that contains copies of the Person objects and are used to determine what state each Person is currently in.
        
        S, E, I, L, ICU, R, D, V, infectious: ndarray
            Numpy arrays that contain the total number of people in each state on each given day. Infectious people are classified as those in compartment I + those in compartments L.
        
        run(getDetails=True): method
            Has parameter getDetails set to True by default. Actually runs the simulation after the object is constructed. If getDetails=True, then the method
            returns a Simul_Details object that will allow user to get more details about the simulation, such as transmissions, state transfers, etc.
        
        toDataFrame(): method
            After running the 'run' method, toDataFrame will convert the numpy arrays to a pandas DataFrame and return it.


        """
    def __init__(self, S0:int, E0:int, I0:int, R0:int, V0:int, rho: float, ioda: float,  gamma: float, mu: float, phi: float, chi: float, omega: float, kappa: float, eta: float, rstart: float, 
        pss: float, side: float, days: int, alpha=2.3, w0=.70, timeDelay=-1):
        # error checks
        self.intCheck([S0, E0, I0, R0, V0, days])
        self.floatCheck([rho, ioda, gamma, mu, phi, chi, omega, kappa, eta, rstart, pss, side, alpha, w0, timeDelay])
        self.negValCheck([S0, E0, I0, R0, V0, rstart, side, days, alpha])
        self.probValCheck([rho, ioda, gamma, mu, phi, chi, omega, kappa, eta, w0])
        # call the super constructor
        super().__init__(S0=S0, E0=E0, I0=I0, R0=R0, V0=V0, rho=rho, ioda=ioda, gamma=gamma, mu=mu, omega=omega, phi =phi, chi=chi, kappa=kappa, eta=eta, rstart=rstart, pss=pss, side=side, days=days, w0=w0, hubConstant=1, timeDelay=timeDelay)

    def _infect(self, inf: Person, sus: Person):
        """
        Computes the probability of infection between an infectious persona and susceptible based on Strong Infectious Model assumptions
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
    
    def plot(self):
        """ Plots the number of people in each compartment except for L and I, as those are plotted as "infectious". """
        t= np.linspace(0, self.days, self.days+1)
        fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7) = plt.subplots(nrows=7, sharex='all')
        ax1.set_ylabel("# Susceptibles")
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax2.set_ylabel("# Exposed")
        ax2.plot(t, self.E, label="Exposed", color='b')
        ax3.set_ylabel("# Infectious")
        ax3.plot(t, self.infectious, label="Infectious", color='limegreen')
        ax4.plot(t, self.ICU, label='Hospitalizations', color='g')
        ax4.set_ylabel("# Hospitalizations")
        ax5.set_ylabel("# Total Deaths")
        ax5.plot(t, self.D, label="Total Dead", color='c')
        ax6.plot(t, self.R, label="Recovered")
        ax6.set_ylabel("# Recovered")
        ax7.set_ylabel("# Vaccinated")
        ax7.plot(t, self.V, label="Vaccinated", color='indigo')
        ax7.set_xlabel("Days")
        ax1.set_title("ICU Strong Infectious Model")
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        ax5.legend()
        ax6.legend()
        ax7.legend()
        plt.show()
