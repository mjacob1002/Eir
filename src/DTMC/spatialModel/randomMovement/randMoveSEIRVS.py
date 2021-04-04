import numpy as np
from matplotlib import pyplot as plt

from .randMoveSEIRV import RandMoveSEIRV

class RandMoveSEIRVS(RandMoveSEIRV):
    """
    Class that simulates the random movement model with an SEIRV model. People in the Exposed compartment are presumed to not be able to propogate infection.

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
    
    eta: float
        The probability of going S->V if person hasn't gone S->E in that same time step.
    
    kappa: float
        The probability of going from R->S.
    
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
        The probability of infection if the distance between an infectious person and susceptible person is 0. Default is 1.0.
    
    alpha: float optional
        A constant used in the _infect() method. The greater the constant, the greater the infection probability. Default is 2.0.
    
    timeDelay: int optional
        Default is -1. Represents the number of days that vaccine rollout should be delayed. If <=0, there is no vaccine rollout delay.

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
    
    V: ndarray
        A numpy array that stores the number of people in the vaccinated state on each given day of the simulation.
    
    popsize: int
        The total size of the population in the simulation. Given by S0 + E0 + I0 + R0 + V0
        
    Scollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is SUSCEPTIBLE. Has a total of popsize Person objects,
        with integers [0, popsize). 
    
    Ecollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is EXPOSED. Has a total of popsize Person objects,
        with integers [0, popsize). 
    
    Icollect: list
         Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is INFECTED. Has a total of popsize Person objects,
        with integers [0, popsize).
    
    Rcollect: list
        Used to keep track of the states each Person object is in. If the copy of a Person object has 
        isIncluded == True, then the person is RECOVERED. Has a total of popsize Person objects,
        with integers [0, popsize).
    
    Vcollect: list
        Used to keep track of the states each Person object is in. If copy of Person object has isIncluded==True, the the person is VACCINATED. 
        Has a total of popsize Person objects, with integers [0,popsize).


    details: Simul_Details 
        An object that can be returned to give a more in-depth look into the simulation. With this object,
        one can see transmission chains, state changes, the movement history of each individaul, the state
        history of each person, and more.
    """

    def __init__(self, S0:int, E0:int, I0:int, R0:int, V0: int, rho: float, gamma: float, eta:float, kappa:float, planeSize: float, move_r: float, sigma_R: float, 
        spread_r: float, sigma_r: float, days:int, w0=1.0, alpha=2.0, timeDelay=-1):
        # error checks
        self.intCheck([S0, E0, I0, R0, V0, days])
        self.floatCheck(rho, gamma, eta, kappa, planeSize, move_r, sigma_R, spread_r, sigma_r, w0, alpha, timeDelay)
        self.negValCheck(S0, E0, I0, R0, rho, gamma, eta, kappa, planeSize, move_r, sigma_R, spread_r, sigma_r, days, w0, alpha)
        self.probValCheck([rho, gamma, eta, kappa, w0])
        super(RandMoveSEIRVS, self).__init__(S0=S0, E0=E0, I0=I0, R0=R0, V0=V0, gamma=gamma, rho=rho, eta=eta, planeSize=planeSize, move_r=move_r, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r, days=days, timeDelay=timeDelay)
        self.kappa = kappa
    
    def _RtoS(self):
        return self._changeHelp(self.Rcollect, self.kappa)
    
    def run(self, getDetails=True):
        for i in range(1, self.days+1):
            StoE = self._StoE(i)
            StoV = set()
            if i > self.timeDelay:
                StoV = self._StoV()
            EtoI = self._EtoI()
            ItoR = self._ItoR()
            RtoS = self._RtoS() 
            self._stateChanger(StoE, self.Ecollect, "E", i)
            self._stateChanger(EtoI, self.Icollect, "I", i)
            self._stateChanger(ItoR, self.Rcollect, "R", i)
            self._stateChanger(StoV, self.Vcollect, "V", i)
            self._stateChanger(RtoS, self.Scollect, "S", i)
            self._move(i, [self.Scollect, self.Ecollect, self.Icollect, self.Rcollect, self.Vcollect])
            self.S[i] = self.S[i-1] - len(StoE) - len(StoV) + len(RtoS)
            self.E[i] = self.E[i-1] + len(StoE) - len(EtoI)
            self.I[i] = self.I[i-1] + len(EtoI) - len(ItoR)
            self.R[i] = self.R[i-1] + len(ItoR) - len(RtoS)
            self.V[i] = self.V[i-1] + len(StoV)
        if getDetails:
            return self.details
    
    def plot(self):
        "Plots the number of susceptible, exposed, infected, and recovered individuals on the y-axis and the number of days on the x-axis."
        t = np.linspace(0, self.days, self.days + 1)
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_ylabel("# Susceptibles")
        ax1.set_title("Random Movement SEIRVS Simulation")
        ax2.plot(t, self.E, label="Exposed", color='g')
        ax2.set_ylabel("# Exposed")
        ax3.plot(t, self.I, label="Active Cases", color='b')
        ax3.set_ylabel("# Active Infections")
        ax5.set_xlabel("Days")
        ax4.set_ylabel("# Recovered")
        ax4.plot(t, self.R, label="Removed")
        ax5.plot(t, self.V, label="Vaccinated", color='c')
        ax5.set_ylabel("# Vaccinated")
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        ax5.legend()
        plt.show()