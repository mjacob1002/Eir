import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from Eir.utility import Person, randEvent
from ..HubModel import Hub
from Eir.DTMC.spatialModel.simul_details import Simul_Details


class Hub_ICUV(Hub):
    """
        Runs a simulation using the Hub Model for an ICU Compartmental Model.

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
            The probability of a susceptible being infected by an infectious individual if they are 0 units apart. Default is 1.0.
        
        hubConstant: float, optional
            The scaling factor of the spreading radius for super spreaders. Default is sqrt(6), as per Fujie & Odagaki's paper.
        
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
        pss: float, side: float, days: int, alpha=2.3, w0=1.0, hubConstant=6**0.5, timeDelay=-1):
        # error checks
        self.intCheck([S0, E0, I0, R0, V0, days])
        self.floatCheck([rho, ioda, gamma, mu, phi, chi, omega, kappa, eta, rstart, pss, side, alpha, w0, hubConstant, timeDelay])
        self.negValCheck([S0, E0, I0, R0, V0, rstart, side, days, alpha, hubConstant])
        self.probValCheck([rho, ioda, gamma, mu, phi, chi, omega, kappa, eta, w0])

        super().__init__(popsize=S0+I0+R0, pss=pss, rstart=rstart, alpha=alpha, side=side, S0=S0, I0=I0, days=days, w0=w0, hubConstant=hubConstant)
        # initialize the numpy arrays
        self.timeDelay = timeDelay
        self.S, self.E, self.I, self.L , self.ICU, self.R, self.D, self.V = np.zeros(self.days+1), np.zeros(self.days+1), np.zeros(self.days+1), np.zeros(self.days+1), np.zeros(self.days+1), np.zeros(self.days+1), np.zeros(self.days+1), np.zeros(self.days+1)
        self.S[0], self.E[0], self.I[0], self.R[0], self.V[0] = S0, E0, I0, R0, V0
        self.L[0], self.ICU[0], self.D[0] = 0, 0, 0
        # is basically I + L
        self.infectious = np.zeros(days+1)
        self.infectious[0] = I0
        # initialize popsize
        self.popsize = S0 + E0 + I0 + R0 +V0
        # create the Siml_Details object
        self.details = Simul_Details(days=self.days, popsize=self.popsize, static=True)
        # create the data structures
        self.Scollect = []
        self.Ecollect = []
        self.Icollect = []
        self.Lcollect = []
        self.ICUcollect = []
        self.Rcollect = []
        self.Dcollect = []
        self.Vcollect = []
        # reinitialize the probabilites
        self.rho = rho
        self.ioda = ioda
        self.mu = mu
        self.phi = phi
        self.omega = omega
        self.chi = chi
        self.kappa = kappa
        self.eta = eta
        self.gamma = gamma
        # generate random locaitons in the plane
        locx, locy= np.random.random(self.popsize) * side, np.random.random(self.popsize) * side
        for i in range(self.popsize):
            event = randEvent(self.pss)
            # S copy
            p1 = Person(locx[i], locy[i], event)
            # I copy
            p2 = Person(locx[i], locy[i], event)
            # R copy
            p3 = Person(locx[i], locy[i], event)
            # D copy
            p4 = Person(locx[i], locy[i], event)
            # Ecopy
            p5 = Person(locx[i], locy[i], event)
            # Lcopy
            p6 = Person(locx[i], locy[i], event)
            # ICU copy
            p7 = Person(locx[i], locy[i], event)
            # Vaccine copy
            p8 = Person(locx[i], locy[i], event)
            # determine what state each person is in at the beginning of the simulation
            if i < S0:
                p1.isIncluded=True
                self.details.addStateChange(i, "S", 0)
            elif i < S0 + E0:
                p5.isIncluded=True
                self.details.addStateChange(i, "E", 0)
            elif i< S0 + E0 + I0:
                p2.isIncluded=True
                self.details.addStateChange(i, "I", 0)
            elif  i< S0 + E0 + I0 + R0:
                p3.isIncluded=True
                self.details.addStateChange(i, "R", 0)
            else:
                p8.isIncluded=True
                self.details.addStateChange(i, "V", 0)
            # Susceptible collect
            self.Scollect.append(p1)
            # Exposed collect
            self.Ecollect.append(p5)
            # Infected collected
            self.Icollect.append(p2)
            # Lag compartment collected
            self.Lcollect.append(p6)
            # Removed compartment collected
            self.Rcollect.append(p3)
            # ICU compartment collect
            self.ICUcollect.append(p7)
            # Death compartment collect
            self.Dcollect.append(p4)
            # Vaccinated compartment collect
            self.Vcollect.append(p8)
    
    def _StoE(self, day: int):
        """
        Takes care of the transfer from S compartment to E compartment.

        Parameters
        ----------

        day: int
            The day that the state change is taking place. Used for Simul_Details object
        
        Returns
        -------

        set:
            Contains the people who need to switch states.
        """
       # cycle through all of the person objects in Icollect and Scollect and determine who goes to E
        transferStoE = set()
        for i, inf in enumerate(self.Icollect):
            if inf.isIncluded == False:
                continue
            for j, sus in enumerate(self.Scollect):
                if sus.isIncluded==False:
                    continue
                w = self._infect(inf, sus)
                event = randEvent(w)
                if not event:
                    continue
                self.Scollect[j].isIncluded = False
                self.details.addTransmission(day, i, j)
                transferStoE.add(j)
        # same loop for L compartment, as they can also propogate the disease
        for i, inf in enumerate(self.Lcollect):
            if inf.isIncluded == False:
                continue
            for j, sus in enumerate(self.Scollect):
                if sus.isIncluded==False:
                    continue
                w = self._infect(inf, sus)
                event = randEvent(w)
                if not event:
                    continue
                self.Scollect[j].isIncluded = False
                self.details.addTransmission(day, i, j)
                transferStoE.add(j)
        return transferStoE
    
    def _EtoL(self):
        """
        Takes care of transfers from E to L compartment.
        
        Returns
        -------

        set:
            Contains the people who need to switch states.
        """
        
        return self._changeHelp(self.Ecollect, self.rho * self.ioda)
    
    def _EtoI(self):
        """
        Takes care of transfers from E to I compartment.
        
        Returns
        -------
        
        set:
            Contains the people who need to switch states.
        """
        return self._changeHelp(self.Ecollect, self.rho * (1-self.ioda))
    
    def _LtoICU(self):
        """
        Takes care of transfers from L to ICU compartment.
        
        Returns
        -------
        
        set:
            Contains the people who need to switch states.
        """
        return self._changeHelp(self.Lcollect, self.phi)
    
    def _ICUtoR(self):
        """
        Takes care of transfers from ICU to R compartment.
        
        Returns
        -------
        
        set:
            Contains the people who need to switch states.
        """
        return self._changeHelp(self.ICUcollect, self.chi)
    
    def _ICUtoD(self):
        """
        Takes care of transfers from ICU to D compartment. Run after _ICUtoR function because of conditional probabilities.
        
        Returns
        -------
        
        set:
            Contains the people who need to switch states.
        """
        return self._changeHelp(self.ICUcollect, self.omega)
    
    def _ItoR(self):
        """
        Takes care of transfers from I to R compartment.
        
        Returns
        -------
        
        set:
            Contains the people who need to switch states.
        """
        return self._changeHelp(self.Icollect, self.gamma)
    
    def _ItoD(self):
        """
        Takes care of transfers from I to D compartment. Run after _ItoR function because of conditional probabilities.
        
        Returns
        -------
        
        set:
            Contains the people who need to switch states.
        """
        return self._changeHelp(self.Icollect, self.mu)
    
    def _RtoS(self):
        """
        Takes care of transfers from R to S compartment.
        
        Returns
        -------
        
        set:
            Contains the people who need to switch states.
        """
        return self._changeHelp(self.Rcollect, self.kappa)
    
    def _StoV(self):
        """
        Takes care of transfers from S to V compartment. Only run after the _StoE function because of conditional probabilities.
        
        Returns
        -------
        
        set:
            Contains the people who need to switch states.
        """
        return self._changeHelp(self.Scollect, self.eta)
    
    
    def run(self, getDetails=True):
        """
        Runs the simulation using the parameters defined at the object's construction. 

        Parameters
        ----------

        getDetails: bool, optional
            Default is True. Determines whether the Simul_Details is returned.
        
        Returns
        -------

        Simul_Details:
            Allows the user to get a more detailed look at the simulation. Only is returned if getDetails is True.
        """
        for i in range(1, self.days+1):
            # S to E transmission
            transferSE = self._StoE(i)
            transferSV = set()
            # if the vaccination rollout is ongoing 
            if i > self.timeDelay:
                transferSV = self._StoV()
            # do L first because of how the conditional probabilities are defined
            transferEL = self._EtoL()
            transferEI = self._EtoI()
            transferLICU = self._LtoICU()
            # do R first because of how the conditional probabilities are defined
            transferICUR = self._ICUtoR()
            transferICUD = self._ICUtoD()
            # do R first because of how conditional probabilities work
            transferIR = self._ItoR()
            transferID = self._ItoD()
            # R to S
            transferRS = self._RtoS()

            # run the state changes of the people in the sets
            self._stateChanger(transferSE, self.Ecollect, "E", i)
            self._stateChanger(transferEL, self.Lcollect, "L", i)
            self._stateChanger(transferEI, self.Icollect, "I", i)
            self._stateChanger(transferLICU, self.ICUcollect, "ICU", i)
            self._stateChanger(transferICUR, self.Rcollect, "R", i)
            self._stateChanger(transferICUD, self.Dcollect, "D", i)
            self._stateChanger(transferIR, self.Rcollect, "R", i)
            self._stateChanger(transferID, self.Dcollect, "D", i)
            self._stateChanger(transferRS, self.Scollect, "S", i)
            self._stateChanger(transferSV, self.Vcollect, 'V', i)
            # adjust the numpy arrays
            self.S[i] = self.S[i-1] + len(transferRS) - len(transferSE) - len(transferSV)
            self.E[i] = self.E[i-1] + len(transferSE) - len(transferEL) - len(transferEI)
            self.I[i] = self.I[i-1] + len(transferEI) - len(transferIR) - len(transferID)
            self.L[i] = self.L[i-1] + len(transferEL) - len(transferLICU)
            self.ICU[i] = self.ICU[i-1] + len(transferLICU) - len(transferICUD) - len(transferICUR)
            self.R[i] = self.R[i-1] + len(transferICUR) - len(transferRS) + len(transferIR)
            self.D[i] = self.D[i-1] + len(transferID) + len(transferICUD)
            self.V[i] = self.V[i-1] + len(transferSV)
            self.infectious[i] = self.I[i] + self.L[i]
        
        if getDetails:
            return self.details
        
    def toDataFrame(self):
        """
        Converts the data to a pandas DataFrame.

        Returns
        -------

        pd.DataFrame:
            Contains the data on number of people in each state and the days it occured.
        """
        t = np.linspace(0, self.days, self.days+1)
        arr = np.stack([t, self.S, self.E, self.I, self.L, self.infectious, self.ICU, self.R, self.D, self.V], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Exposed", "Infectious", "Lag", "Total Infectious", "ICU", "Recovered", "Dead", "Vaccinated"])
        return df
    
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
        ax1.set_title("ICU Hub Model")
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        ax5.legend()
        ax6.legend()
        ax7.legend()
        plt.show()


    

        
