import numpy as np

from src.utility import randEvent
from .randMoveSEIR import RandMoveSEIR

class RandMoveSEIRS(RandMoveSEIR):
    """
    Class that simulates the random movement model with an SEIR model. People in the Exposed compartment are presumed to not be able to propogate infection.

    Parameters
    ----------

    Parameters:
    ----------

    S0: int
        The starting number of susceptible individuals in the simulation.
    
    E0: int
        The starting number of exposed individuals in the simulation.
    
    I0: int
        The starting number of infectious individuals in the simulation. 
    
    R0: int
        The starting number of recovered individuals in the simulation.
    
    rho: float
        The probability of someone going from the E compartment to the I compartment.

    gamma: float
        The recovery probability of an individual going from I -> R.
    
    planeSize : float
        The length of each side of the square plane in which the individuals are confined to. For example,
        if planeSize=50, then the region which people in the simulation are confined to is the square with
        vertices (0,0), (50,0), (50,50), and (0,50).
    
    move_r: float
        The mean of the movement radius of each person in the simulation. Will be used as mean along with 
        sigma_R as the standard deviation to pull from a normal distribution movement radii each time 
        _move(day) function is called.
    
    sigma_R: float
        The standard deviation of the movement radius of each person in the simulation. Will be used along with 
        move_R as the mean to pull from a normal distribution movement radii each time _move(day) function is 
        called.

    spread_r: float
        The mean of the spreading radius of each person in the simulation. Will be used along with sigma_r 
        as the standard deviation to pull from an normal distribution spreading radii for each individaul person
        when the RandMoveSIS object is initialized. 
    
    sigma_r: float
        The standard deviation of the spreading radius of each person in the simulation. 
        Will be used along with spread_r as the mean to pull from an normal distribution spreading radii 
        for each individaul person when the RandMoveSIS object is initialized. 
    
    days: int
        The number of days that was simulated.
    
    w0: float optional
        The probability of infection if the distance between an infectious person and susceptible person is 0.
    
    alpha: float optional
        A constant used in the _infect() method. The greater the constant, the greater the infection probability.

    Attributes
    ----------

    S: ndarray
        A numpy array that stores the number of people in the susceptible state on each given day of the simulation.
    
    E: ndarray
        A numpy array that stores the number of people in the exposed state on each given day of the simulation.
    
    I: ndarray
        A numpy array that stores the number of people in the infected state on each given day of the simulation.
    
    R: ndarray
        A numpy array that stores the number of people in the recovered state on each given day of the simulation.
    
    popsize: int
        The total size of the population in the simulation. Given by S0 + I0
        
    Scollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is SUSCEPTIBLE. Has a total of popsize Person objects,
        with numbers [0, popsize). 
    
    Ecollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is EXPOSED. Has a total of popsize Person objects,
        with numbers [0, popsize). 
    
    Icollect: list
         Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is INFECTED. Has a total of popsize Person objects,
        with numbers [0, popsize).
    
    Rcollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is RECOVERED. Has a total of popsize Person objects,
        with numbers [0, popsize).


    details: Simul_Details 
        An object that can be returned to give a more in-depth look into the simulation. With this object,
        one can see transmission chains, state changes, the movement history of each individaul, the state
        history of each person, and more.
    


    """
    def __init__(self, S0:int, E0:int, I0:int, R0:int, rho:float, gamma:float, kappa:float, planeSize:float, move_r:float, sigma_R:float, spread_r:float, sigma_r: float, days:int, w0=1.0, alpha=2.0):
        super(RandMoveSEIRS, self).__init__(S0=S0, E0=E0, I0=I0, R0=R0, rho=rho, gamma=gamma, planeSize=planeSize, move_r=move_r, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r, days=days, w0=w0, alpha=alpha)
        self.kappa = kappa

    def _RtoS(self):
        """
        Deals with the transfers from R to S. 

        Returns
        -------

        set:
            set of all indices that represent the people going from R to S.
        """
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
        