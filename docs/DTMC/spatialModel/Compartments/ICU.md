# Overview

In the ICU model, there are many compartments. There are the standard compartments that were seen before, namely S, E, I, R and V. However, there is now two new compartments: L and ICU. The L compartment, or "Lag compartment", represents those who, after leaving E compartment, will be destined to eventually go to the ICU, but aren't there yet. It is assumed those in L can still propogate the infection. The ICU compartment represents those who are hospitalized and will either go to the D compartment or R compartment. 

# Parameters

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
        
        timeDelay: float
            The number of days that vaccine rollout is delayed. If negative or 0, then there is no delay in vaccine rollout. Default value is -1. 
        