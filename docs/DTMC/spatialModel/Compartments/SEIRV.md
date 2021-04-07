# Parameters

S0 : the number of susceptible individuals at the start of the simulation. Must be an int. Throws ```python NotIntException``` otherwise.

E0: the number of exposed individuals at the start of the simulation. Must be an itn. Throws ```python NotIntException``` otherwise.

I0: the number of infected individuals at the start of the simulation. Must be an int. Throws ```python NotIntException``` otherwise.

R0: the number of removed individuals at the start of the simulation. Must be an int. Throws ```python NotIntException``` otherwise.

V0: the number of vaccinated individuals at the start of the simulation. Must be an int. Throws ```python NotIntException``` otherwise.

rho: the probability that an individuals goes from E compartment to I compartment. Must be a value that belongs to [0,1]. Throws ```python ProbabilityException``` or ```python NotFloatException``` otherwise. 

gamma: the probability that an individuals goes from I compartment to R compartment. Must be a value that belongs to [0,1]. Throws ```python ProbabilityException``` or ```python NotFloatException``` otherwise. 

eta: the probability that an individual goes from S compartment to V compartment, given that the person didn't go from S to E. Must be a value that belongs to [0,1]. Throws ```python ProbabilityException``` or ```python NotFloatException``` otherwise. 

timeDelay: float
    The number of days that vaccine rollout is delayed. If negative or 0, then there is no delay in vaccine rollout. Default value is -1. If not float, will throw ```python NotFloatException```. 