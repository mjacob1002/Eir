# Overview

Unlike the two static spatial models, the Random Movement and Periodic Mobility models change the (x,y) coordinates of each individual at every time step according to the rules for that model. 

The same formula used for normal spreaders in static spatial models is the same for all individuals in the movement models. However, the spreading radii and movement radii for everyone in the simulation is picked from normal disributions generated from user input. However, what they do with these parameters depends on the model.

## Random Movement

In the Random Movement model, at each time step, the new (x,y) coordiante is picked by randomly picking a distance from a normal distribution and then randomly picking an angle from a uniform distribution because we assume that people in this model are equally likely to move in any direction. 

## Periodic Mobility

In the Periodic Mobility Model, at each step, the new (x,y) coordiante is picked by randomly picking an angle to move from a normal distribution, and then using the individual's movement radius R, move along the individual's circular motion, calculated upon generating the individual. This is aimed to capture the routine nature of people's movements. 

## Parameters

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

There are also special parameters for the Periodic Mobility Model:

k: float
    Determines the mean of the distribution of thetas. The mean of that distribution is 2π/k.

std: float
    The standard deviation of the normal distribution of thetas. 