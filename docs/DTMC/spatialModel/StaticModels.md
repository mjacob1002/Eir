# Overview

These static models are ones in which the randomly generated (x,y) coordinate of each person in the simulation does not change throughout the entire simulation. Therefore, because there is no call to a _move() function, these simulations tend to run a little faster than the movement models. The two static spatial models are derived from the work of Ryo Fujie and Takashi Odagaki, whose paper proposed two different models: the Hub Model and the Strong Infectious Model. These two models attempt to make assumptions about super spreaders and how they propogate the disease differently than a normal spreader.

The default formula for a normal spreader's probability of infecting a susceptible is:

w(r) = 
    w0(1-r/r_0)^alpha, &0 <= r <= r_0,
    0, &r > r_0.

In this equation, w0 is the probability that an infectious person infects someone when they are 0 units away, alpha is a constant, r is the distance between the infectious individual and the susceptible, and r_0 is the spreading radius of the infectious individual.

In the following two models, however, the formula for a super spreader changes.
## Hub Model
The Hub Model assumes that super spreaders are those who interact with more people, and therefore have a higher a spreading radius that is a scaled by a constant, allowing them to reach more people. Therefore, if we call k the scaling factor and r_0 the spreading distance for a normal spreader, the equation for a super spreader's probability of infecting a susceptible is:
\begin{align*}
w(r) = \begin{cases}
    w0(1-r/r_n)^alpha, &0 <= r <= r_n,
    0, &r > r_n
\end{cases}
\end{align*}
, where r_n = k*r_0. 

### Parameters

These parameters of all Hub objects. don't include compartment-specific parameters, which can be found in the Compartments section of the documentation.

    pss: float
        probability someone is considered a super spreader upon generating the simulation.
    
    rstart: float
        the spreading radius of every normal spreader.
    
    side: float
        size of one side of the square plane that individuals are confined to.
    
    days: int
        The number of days that are simulated.
    
    w0: float (optional)
        The probability of infection if an infectious and susceptible individual are in the same location. Default is 1.0.
    
    hubConstant: float (optional)
        The factor k multliplied to the rstart if the person is a super spreader. Default is sqrt(6).
    
    alpha: float optional
        constant used in the P(infection) formula. Default is 2.0.


## Strong Infectious Model
The Strong Infectious Model assumes that super spreaders are intrinsically more infectious, and therefore have a fixed probability of spreading the disease over spreading radius identical to that of a normal spreader. Therefore, the formula for a super spreader's probability of propogating an infectious disease is: 
\begin{align*}
w(r) = \begin{cases}
    w0, &0 <= r <= r_0,
    0, &r > r_0.
\end{cases}
\end{align*}.

### Parameters

The parameters of the Strong Infectious Model are almost identical to that of the Hub Model, except for two differences. The first is that there is no scaling factor, k, because the radius of the super spreader hasn't increased. Secondly, the default for w0 is now 0.7 rather than 1.0.