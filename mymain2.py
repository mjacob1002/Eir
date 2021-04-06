#from Eir import SIR

#sim = SIR(S0=9999999, I0=1, Ro=0, beta=1.5, gamma=.15)
#df = sim.run(31, .1, plot=False)
from Eir import HubSIS

test = HubSIS(S0=999, I0=1, pss=.2, side=25, days=31, gamma=.3, rstart=3)
d = test.run()
#a = d.personHistory(9, True)[1]
#print(a)
#b = d.personTransmissionHistory(9)
#print(b)

c = d.sortedTransmissions()
print(c)
