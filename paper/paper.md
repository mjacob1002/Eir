---
title: 'Eir: A Python Package for Epidemic Simulation'
tags:
  - Python
  - epidemiology
  - super spreaders
  - spatial models
  - stochastic
  - Python
authors:
  - name: Mathew Jacob
    orcid: 0000-0001-5513-432X
    affiliation: "1" # (Multiple affiliations must be quoted)

affiliations:
 - name: RxCovea, New York University, New York, USA
   index: 1

date: 8 April 2021

bibliography: paper.bib

---

# Summary

` Eir ` is a Python package that simulates epidemics with various assumptions and compartmental models. By mainly using spatial models, ` Eir ` allows for better modeling of the spread of an epidemic in smaller communities and localities. There are four different spatial models used: the Strong Infectious Model [@Fujie&Odagaki], Hub Model [@Fujie&Odagaki], the Random Movement Model, and the Periodic Mobility Model. While the Strong Infectious Model and Hub Model are static models, where no movement pattern is simulated, the Random Movement and Periodic Mobility Model simulates the movement pattern of people using different assumptions. The Random Movement Model assumes that an individual is equally likely to move in any direction for a random distance, generated from a user-defined normal distribution. The Periodic Mobility Model assumes that individuals move in a circle to capture the routine nature of people's movements. Therefore, after randomly generating locations, the model calculates a center of a circle and individuals move along that circle. With all of these spatial models, researchers can use the `Simul_Details` objects to interact with the simulation data and get a deeper understanding of the simulation's dynamics, such as transmission chains, state histories, etc. The data from these simulations can be plotted using Matplotlib or be returned in the form of a pandas DataFrame. It is important to note that these models are stochastic and are discrete-time Markov chains. 

` Eir ` leverages many different compartmental models in addtition to different spatial models in order to give researchers flexibility and robustness when simulating the spread of an epidemic. The models include but are not limited to: Susceptible-Infected-Recovered (SIR), Susceptible-Infected-Recovered-Dead (SIRD), Susceptible-Exposed-Infected-Recovered (SEIR), Susceptible-Exposed-Infected-Recovered-Vaccinated (SEIRV), Susceptible-Infected-Recovered-Susceptible-Vaccinated (SIRSV), and ICU models. The ICU models, in particular, are based on the work of Mühlpfordt et al [@ICU]. Additionally, for any model that includes vaccinations, there is a timeDelay variable that allows the user to delay vaccine distribution by a particular amount of days. 

While not the primary focus of the Python package, `Eir` also allows for researchers to use determinstic models to simulate basic compartmental models, including SIR, SEIR, SIRV, and more. 

`Eir` is currently being used for a publication involving simulating hospitalizations and studying vaccinations strategies. It is intended to be used by epidemiologists and researchers who are interested in understanding the dynamics of epidemics when operating under different modelling assumptions, such as periodic movement or random movement, which can be evaluated by using different models in Eir.

# Statement of Need

When modelling the spread of diseases, epidemiologists often use compartmental models, which classify people into states, the most common one being the SIR Model [@SIR]. There are certain rules that govern these compartmental models, such as that an individual can only exist in one compartment at any given time. With these models, epidemiologists are able to understand the dynamics of how an epidemic spreads. However, a lot of these models often use ODEs to approximate parameters for large populations and make assumptions to simplify calculations, which don't capture the complexities of smaller communities, where national averages may not be accurate. Then, researchers often use discrete-time Markov chains [@Allen], which generate stochastic events at certain time steps, such as every day or every hour. Additionally, in these smaller localities, spatial models are often deployed to get more accurate transmission probabilities. The sheer number of spatial models in Eir, as well as Eir's inclusion of models with movement, will make the process of modelling local disease transmission far easier. These spatial models are known as the Hub model [@Fujie&Odagaki], Strong Infectious Model [@Fujie&Odagaki], Random Movement Model, and Periodic Mobility Model. The Random Movement Model assumes that an individual is equally likely to move in every direction. The Periodic Mobility Model assumes that each person moves along a circle with a normally distributed radius. These models offer different structure to the spatial models, which can be used by epidemiologists. 


# Dependencies
NumPy, Matplotlib, multipledispatch, pandas

# Related Packages
There are different software package that enable users to simulate epidemics in different ways. A couple of such packages are:

### Epidemics on Networks

 Epidemics on Networks [@Miller2019], abbreviated EoN, is a Python package that allows users to simulate SIS and SIR epidemics on networks. It handles many different simulation types, as well. More can be found by reading the documentation at https://epidemicsonnetworks.readthedocs.io/en/latest/. Eir allows for a wider variety of models than EoN, which only includes SIS and SIR. Additionally, another difference is that Eir allows for the movement of individuals within the simulation, while the structure in EoN does not. 

### EpiModel

 EpiModel [@EpiModel] is an R package that allows the user to simulate models such as SIS and SIR. The details of this model can be found at https://www.epimodel.org/. EpiModel offers network based transmission, which is a feature that is not included in Eir. However, similar to EoN, there is no clear way to incorporate the movement of individuals within the simulation. Additionally, Eir offers a more detailed look at the simulation through the Simul_Details object, which can include information about individual state history, transmission chains, and more. 

# Acknowledgements
The author would like to acknowledge the contributions of Xueyao Guo to the models. Additionally, the author would like to acknowledge and thank Dr. Ernest Battifarano, Dr. Jantine Broek, and Professor Shirshendu Chatterjee for their mentorship and guidance through the author's research. Finally, the author would like to thank Professor Bud Mishra and the RxCovea group for guiding the author through his research. 

This project received no funding. 

# References

