# Eir: Simulate Epidemics Using Spatial Models in Python!

Eir is an API that allows the user to conduct stochastic simulations of epidemics, primarily using spatial models. With this software, one can simulate not only how epidemics relate to the distances between an infectious and susceptible indivdual, but also how the movement on infectious individuals plays a role in the spread of a disease. Eir also offers a lot of variety to the user, containing many more compartmental models that is present in any of the existing packages similar to Eir. 

## Installation

One can install Eir by running the following command via the command line:

```pip install Eir ```

## Examples

If one were to model the ICU hospitalizations using the Hub Model, the code could look as follows:

```python
from Eir.DTMC.spatialModel.periodicICUV import PeriodicICUV

  test = PeriodicICUV(S0=999, E0=0, I0=1, R0=0, V0=0, rho=.3, ioda=.3, gamma=.25, mu=0.007, omega=.14, phi = .42, chi=.15, kappa=.05, eta=.02, spread_r=2, sigma_r=.25, move_R=4, sigma_R=.75, side=33, days=31)       
  test.run()
  test.plot()
```

To understand the variables and their meaning, the documentation can be found in the code by doing the standard ```__doc__``` in Python. Additionally, if more detailed information about transmission chains and state histories was required, the methods from the Simul_Details class would allow the user to get a more in-depth look at the dynamics of the simulation.


