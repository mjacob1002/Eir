# Parameters

S0 : the number of susceptible individuals at the start of the simulation. Must be an int.
Throws ```python NotIntException``` otherwise.

I0: the number of infected individuals at the start of the simulation. Must be an int.
Throws ```python NotIntException``` otherwise.

gamma: the probability that an individuals goes from I compartment to S compartment.
Throws ```python ProbabilityException``` otherwise.