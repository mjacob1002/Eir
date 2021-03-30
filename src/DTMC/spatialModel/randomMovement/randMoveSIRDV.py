import numpy as np
from matplotlib import pyplot as plt   
import pandas as pd

from src.DTMC.spatialModel.randomMovement.randMoveSIRD import RandMoveSIRD
from src.utility import Person1 as Person

class RandMoveSIRDV(RandMoveSIRD):

    def __init__(self, S0, I0, R0, V0, gamma, mu, eta, planeSize, move_r:float, sigma_R:float, spread_r:float, sigma_r: float, days:int, w0=1.0, alpha=2.0, timeDelay=-4):
        self.timeDelay = timeDelay
        super(RandMoveSIRDV, self).__init__(S0=S0, I0=I0, R0=0, gamma=gamma, mu=mu, planeSize=planeSize, move_r=move_r, sigma_R=sigma_R, spread_r=spread_r, sigma_r=sigma_r,
        days=days)
        self.eta = eta
        self.Dcollect = []
        self.Scollect, self.Icollect, self.Rcollect, self.Vcollect = [], [], [], []
        spreading_r = np.random.normal(spread_r, sigma_r, S0+I0)
        # generate the random x, y locations with every position within the plane being equally likely
        loc_x = np.random.random(S0+I0) * planeSize
        loc_y = np.random.random(S0+I0) * planeSize
        # create the special objects:
        for i in range(self.popsize):
            # create the person object
            # for this model, the people will move with random radius R each timestep
            # therefore, the R component can be made 0, as that is only relevant for the 
            # periodic mobility model
            p1 = Person(loc_x[i], loc_y[i], 0, spreading_r[i])
            p2 = Person(loc_x[i], loc_y[i], 0, spreading_r[i]) 
            p3 = Person(loc_x[i], loc_y[i], 0, spreading_r[i])
            p4 = Person(loc_x[i], loc_y[i], 0, spreading_r[i])
            p5 = Person(loc_x[i], loc_y[i], 0, spreading_r[i])
            self.details.addLocation(0, (loc_x[i], loc_y[i]))       
            # if the person is in the susceptible objects created
            if i < S0:
                p1.isIncluded = True
                self.details.addStateChange(i, "S", 0)
            elif S0 <= i < S0+I0:
                p2.isIncluded = True
                self.details.addStateChange(i, "I", 0)
            elif i < S0 +I0 + R0:
                p3.isIncluded=True
                self.details.addStateChange(i, "R", 0)
            else:
                p4.isIncluded=True
                self.details.addStateChange(i, "V", 0)
            # append them to the data structure
            self.Scollect.append(p1)
            self.Icollect.append(p2)
            self.Rcollect.append(p3)
            self.Vcollect.append(p4)
            self.Dcollect.append(p5)
        self.D = np.zeros(days+1)
        self.V = np.zeros(days+1)
        self.V[0] = V0
    
    def _StoV(self):
        return self._changeHelp(self.Scollect, self.eta)
    
    def run(self, getDetails=True):
        """
        Run the actual simulation. 

        Parameters
        ----------

        getDetails: bool optional
            If getDetails=True, then run will return a Simul_Details object which will allow the user to 
            examine details of the simulation that aren't immediately obvious.
        
        Returns
        -------

        Simul_Details:
            Allows the user to take a deeper look into the dynamics of the simulation by examining transmission
            chains. User can also examine transmission history and state changes of individuals in the object
            by utilizing the Simul_Details object. 
        """

        # for all the days in the simulation
        for i in range(1, self.days+1):
            print("Day ", i)
            #print("Location: (", self.Scollect[0].x, ",", self.Scollect[0].y, ").")
            # run the state changes
            StoI = self._StoI(i)
            StoV = set()
            if i > self.timeDelay:
                StoV = self._StoV()
            ItoR = self._ItoR()
            ItoD = self._ItoD()
            # change the indices of the transfers
            self._stateChanger(StoI, self.Icollect, "I", i)
            self._stateChanger(ItoR, self.Rcollect, "R", i)
            self._stateChanger(ItoD, self.Dcollect, "D", i)
            self._stateChanger(StoV, self.Vcollect, "V", i)
            
            # make everyone move randomly, don't move dead people
            self._move(i, [self.Scollect, self.Icollect, self.Rcollect])
            # change the values in the arrays
            self.S[i] = self.S[i-1] - len(StoI) - len(StoV)
            self.I[i] = self.I[i-1] + len(StoI) - len(ItoR) - len(ItoD)
            self.R[i] = self.R[i-1] + len(ItoR)
            self.V[i] = self.V[i-1] + len(StoV)
            self.D[i] = self.D[i-1] + len(ItoD)
        if getDetails:
            return self.details
    
    def toDataFrame(self):
        """
        Gives user access to pandas dataframe with amount of people in each state on each day.

        Returns
        -------

        pd.DataFrame
            DataFrame object containing the number of susceptibles and number of infecteds on each day. 

        """
        # create the linspaced numpy array
        t = np.linspace(0, self.days, self.days + 1)
        # create a 2D array with the days and susceptible and infected arrays
        # do it over axis one so that it creates columns days, susceptible, infected
        arr = np.stack([t, self.S, self.I, self.R, self.V, self.D], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Infected", "Recovered", "Vaccinated", "Dead"])
        return df
    
    def plot(self):
        t = np.linspace(0, self.days, self.days+1)
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, sharex='all')
        ax1.plot(t, self.S, label="Susceptible", color='r')
        ax1.set_title("Random Movement SIRDV")
        ax1.set_ylabel("# Susceptibles")
        ax2.plot(t, self.I, label="Infected", color='g')
        ax2.set_ylabel("# Active Cases")
        ax3.plot(t, self.R, label="Recovered", color='c')
        ax3.set_ylabel("# Recovered")
        ax4.plot(t, self.V, label="Vaccinated", color='b')
        ax4.set_ylabel("# Vaccinated")
        ax5.set_xlabel("Days")
        ax5.set_ylabel("# Dead")
        ax5.plot(t, self.D, label="Dead")
        plt.show()
        
        
