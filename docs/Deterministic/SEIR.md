# Examples

To run the simulation with a certain number of days, you can run code like the following:

```python

from Eir import SEIR

sim = SEIR(S0=9999999, E0=10000, I0=1, R0=0, beta=1.5, rho=.25, gamma=.15)
df = sim.run(31, .1, plot=False)
```

run() takes the number of simulated as first parameter, and the differential, or step, used for the Euler approximation of the ODE. 

If a plot is wanted, simply run the following:

```python

from Eir import SEIR

sim = SEIR(S0=9999999, E0=10000, I0=1, R0=0, beta=1.5, rho=.25, gamma=.15)
df, fig = sim.run(31, .1)

```

This will display a plot of all variables, which can be further customized using the default boolean parameters that represent all of the variables within the model.