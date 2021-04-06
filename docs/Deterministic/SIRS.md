# Examples

To run the simulation with a certain number of days, you can run code like the following:

```python

from Eir import SIRS

sim = SIR(S0=9999999, I0=1, R0=0, beta=1.5, gamma=.15, kappa=.05)
df = sim.run(31, .1, plot=False)
```

If a plot is wanted, simply run the following:

```python

from Eir import SIRS

sim = SIRS(S0=9999999, I0=1, R0=0, beta=1.5, gamma=.15, kappa=.15)
df, fig = sim.run(31, .1)

```

This will display a plot of all variables, which can be further customized using the default boolean parameters.