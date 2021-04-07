# Eir: Simulate Epidemics Using Spatial Models in Python

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

To understand the variables and their meaning, the documentation can be found in the docs folder in this repository, or looking at the docstrings in python. Additionally, if more detailed information about transmission chains and state histories was required, the methods from the Simul_Details class would allow the user to get a more in-depth look at the dynamics of the simulation.

## Contributers
The author welcomes and encourages new contributers to help test ``` Eir``` and add new functionality. If one wishes to contact the author, they may do so by emailing mjacob1002@gmail.com. Response times may vary.



