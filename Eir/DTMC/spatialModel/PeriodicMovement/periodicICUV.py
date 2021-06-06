import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from math import cos, sin, pi

from Eir.DTMC.spatialModel.simul_details import Simul_Details
from Eir.DTMC.spatialModel.randomMovement.randMove import RandMove
import Eir.exceptions as e
from Eir.utility import Person2 as Person
from Eir.utility import randEvent, dist

class PeriodicICUV(RandMove):
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
        
        move_R: float
            The mean of the distribution of movement radii of a a person in the simulation. Used when genereating the movement radius of each individual in the simulation.
        
        sigma_R: float
            The standard deviation of the distribution of movement radii of a a person in the simulation. Used when genereating the movement radius of each individual in the simulation.

        spread_r: float
            The mean of the distribution of spreading radii of a person in simulation. Used when generating the spreading radius of each individaul in the simultion. 
        
        sigma_r: float
            The standard deviation of the distribution of spreading radii of a normal spreader.
        
        
        side: float
            The length of one side of the square plane that the individuals are confined to.
        
        days: int
            The number of days that the simulations lasts for.
        
        alpha: float, optional
            A constant used in the formula for calculating probability of infection between infectious person and susceptible person. Default is 2.0.
        
        w0: float, optional
            The probability of a susceptible being infected by an infectious individual if they are 0 units apart. Default is 1.0.
        
        timeDelay: float, optional
            The amount of days for which the vaccine rollout is delayed. Checks the day and makes sure that the day > timeDelay before simulating vaccine distribution. Default is -1.
        
        k: float optional
            Default is 5.0. The number which divides 2*pi in order to determine the mean of the distribution of thetas when movement occurs. For example, if k=5, then the mean of the normal distribution from which thetas are picked is 2*pi/5.0.
        
        std: float optional
            Default is pi/2. The standard deviation which is used for the distribution of thetas when movement occurs.

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

    
    def __init__(self, S0:int, E0:int, I0:int, R0:int, V0:int, rho: float, ioda: float,  gamma: float, mu: float, phi: float, chi: float, omega: float, kappa: float, eta: float, move_R: float, sigma_R: float, spread_r: float, 
        sigma_r: float, side: float, days: int, alpha=2.3, w0=1.0, timeDelay=-1, k=5, std=pi/2):
        # error checks
        
        self.intCheck([S0, E0, I0, R0, V0, days])
        self.floatCheck(rho, ioda, gamma, mu, phi, chi, omega, kappa, eta, spread_r, sigma_r, move_R, sigma_R, side, alpha, w0, timeDelay)
        self.negValCheck(S0, E0, I0, R0, V0, spread_r, sigma_r, move_R, sigma_R, side, days, alpha)
        self.probValCheck([rho, ioda, gamma, mu, phi, chi, omega, kappa, eta, w0])
        # map the mean period factor and std dev
        self.k=k; self.std = std
        # call super constructor
        super().__init__(planeSize=side, move_r=move_R, spread_r=spread_r, w0=w0)
        # initialize class varaibles and arrays
        self.days = days
        self.S, self.E, self.I, self.L, self.ICU, self.R, self.D, self.V = np.zeros(days+1), np.zeros(days+1), np.zeros(days+1), np.zeros(days+1), np.zeros(days+1), np.zeros(days+1), np.zeros(days+1), np.zeros(days+1)
        self.S[0]=S0; self.E[0]=E0; self.I[0]=I0; self.R[0]=R0; self.V[0]=V0
        self.infectious = np.zeros(self.days+1)
        self.timeDelay = timeDelay
        self.popsize = S0 + E0 + I0 + R0 + V0
        self.details = Simul_Details(days=self.days, popsize=self.popsize)
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
        spreading_r = np.random.normal(spread_r, sigma_r, self.popsize)
        mvnt = np.random.normal(move_R, sigma_R, self.popsize)
        theta = np.random.normal(2*pi/k, std, self.popsize)
        for i in range(self.popsize):
            # person objects are stored in order [S, E, I, L, ICU, R, D, V]
            person = []
            for j in range(8):
                p = Person(locx[i], locy[i], mvnt[i], spreading_r[i], theta[i])
                person.append(p)
                self.details.addLocation(0, (p.x, p.y))
            if i < S0:
                person[0].isIncluded=True
                self.details.addStateChange(i, "S", 0)
            elif i < S0 + E0:
                person[1].isIncluded=True
                self.details.addStateChange(i, "E", 0)
            elif i < S0 + E0 + I0:
                person[2].isIncluded=True
                self.details.addStateChange(i, "I", 0)
            else:
                person[5].isIncluded=True
                self.details.addStateChange(i, "R", 0)
            # add the Person objects to the collections
            self.Scollect.append(person[0])
            self.Ecollect.append(person[1])
            self.Icollect.append(person[2])
            self.Lcollect.append(person[3])
            self.ICUcollect.append(person[4])
            self.Rcollect.append(person[5])
            self.Dcollect.append(person[6])
            self.Vcollect.append(person[7])
    
    
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

    # eventually do it for every person in each collection array; will be implemented in the sublcasses
    def _move(self, day: int, collects: list):
        """
        Responsible for moving the locations of each Person in the simulation. Does it in place.

        Parameters
        ----------
        day: int
            The current day that the move is taking place on. Is important for the Simul_Details() object in order to keep track of the movement patterns each day.
        
        collect: list
            Contains all of the collection data structures that will be cycled through for the moves. This allows for easy object-oriented design.
        """
        # generate the random thetas from a normal distribution
        thetas = np.random.normal(2*pi/self.k, self.std, self.popsize)

        for index, person in enumerate(collects[0]):
            # adjust the theta current theta values in the object
            collects[0][index].theta += thetas[index]
            # adjust the x,y coordinate using polar coordinates
            # conduct the boundary check at the same time
            x = self._boundaryCheck(person.h + person.R * cos(collects[0][index].theta))
            y = self._boundaryCheck(person.k + person.R * sin(collects[0][index].theta))
            # add the new location to the Simul_Details object
            self.details.addLocation(day, (x,y))
            # change the x, y coordinates of every copy of person index in the other collections
            for j, collect in enumerate(collects):
                collects[j][index].x = x
                collects[j][index].y = y
                collects[j][index].theta += thetas[index]
    
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

            self._move(i, [self.Scollect, self.Ecollect, self.Icollect, self.Lcollect, self.ICUcollect, self.Rcollect, self.Dcollect, self.Vcollect])
        
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
        ax1.set_title("ICU Periodic Mobility Model")
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        ax5.legend()
        ax6.legend()
        ax7.legend()
        plt.show()
