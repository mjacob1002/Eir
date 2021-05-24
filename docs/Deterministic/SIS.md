# Examples

If one wanted to get a plot of a particular SIS model, the run function would be used. run() takes the number of simulated as first parameter, and the differential, or step, used for the Euler approximation of the ODE. A way to run it would be as follows:

```python 

from Eir import SIS

sim = SIS(S0=9999999, I0=1, beta=1.5, gamma=.15)
df = sim.run(31, .1, plot=False)

```

When printing the dataframe, the output will be the following:

```
>>> print(df)
     Days   Susceptible      Infected
0     0.0  9.999999e+06  1.000000e+00
1     0.1  9.999999e+06  1.135000e+00
2     0.2  9.999999e+06  1.288225e+00
3     0.3  9.999999e+06  1.462135e+00
4     0.4  9.999998e+06  1.659524e+00
..    ...           ...           ...
306  30.6  1.000000e+06  9.000000e+06
307  30.7  1.000000e+06  9.000000e+06
308  30.8  1.000000e+06  9.000000e+06
309  30.9  1.000000e+06  9.000000e+06
310  31.0  1.000000e+06  9.000000e+06

[311 rows x 3 columns]
>>> 
```

However, if plot=True in the run method, then a pyplot figure object will be returned with the dataframe in a tuple, with element 0 being the dataframe and element 1 being the figure object. A plot will also be displayed that represent all of the variables within the model.

