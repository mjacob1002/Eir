# Eir: Simulate Epidemics Using Spatial Models in Python

[![DOI](https://joss.theoj.org/papers/10.21105/joss.03247/status.svg)](https://doi.org/10.21105/joss.03247)

Eir, named after the Norse valkyrie with great medical skill, is an API that allows the user to conduct stochastic simulations of epidemics, primarily using spatial models. With this software, one can simulate not only how epidemics relate to the distances between an infectious and susceptible indivdual, but also how the movement on infectious individuals plays a role in the spread of a disease. Eir also offers a lot of variety to the user, containing many more compartmental models that is present in any of the existing packages similar to Eir, including hospitalizations and vaccinations. Eir's usefulness can clearly be seen in modern day, where simulations and models are constantly used to form policy to combat COVID-19.
## Dependencies
Eir depends on ```numpy```, ```pandas```, ```matplotlib```, and ```multipledispatch```.
## Installation

One can install Eir via PyPI by running the following command via the command line:

```pip install Eir ```
The dependencies will automatically be installed as well.
## Notable Features
Eir offers countless different compartmental models, including:
- SIS
- SIR
- SIRS
- SIRD
- SIRV
- SIRSD
- SIRSV
- SIRDV
- SIRSDV
- SEIR
- SEIRS
- SEIRD
- SEIRV
- SEIRSD
- SEIRSV
- SEIRDV
- SEIRSDV
- ICU models. 

Eir also offers these models in different spatial models, some with mobility and some static.

## Examples

If one were to model the ICU hospitalizations using the Hub Model, the code could look as follows:

```python
from Eir import PeriodicICUV

test = PeriodicICUV(S0=999, E0=0, I0=1, R0=0, V0=0, rho=.3, ioda=.3, gamma=.25, mu=0.007, omega=.14, phi = .42, chi=.15, kappa=.05, eta=.02, spread_r=2, sigma_r=.25, move_R=4, sigma_R=.75, side=33, days=31)       
test.run()
test.plot()
```
In the above code segment:
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
        
        spread_r: the mean of the normal distribution of spreading radii that is use to generate spreading radii for each individual in the simulation.

        sigma_r: the standard deviation of the normal distribution of spreading radii that is used to generate spreading raddi for each individual in the simulation.

        move_R: the mean of the normal distribution of spreading radii that is use to generate movement radii for each individual's periodic movement in the simulation.

        sigma_R: the standard deviation of the normal distribution of spreading radii that is use to generate movement radii for each individual's periodic movement in the simulation.

        side: the length of the side of the square plane that individuals are confined to during the simulation.

        days: the number of days being simulated. 


To understand the variables and their meaning for different models, the documentation can be found in the docs folder in this repository, or looking at the docstrings in python. Additionally, if more detailed information about transmission chains and state histories was required, the methods from the Simul_Details class would allow the user to get a more in-depth look at the dynamics of the simulation.

## Contributors
The author welcomes and encourages new contributors to help test ``` Eir``` and add new functionality. If one wishes to contact the author, they may do so by emailing mjacob1002@gmail.com. Response times may vary.



