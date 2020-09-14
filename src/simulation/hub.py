'''
hub model based on Fujie&Odagaki, 2007
'''
import random


#adjust parameters here
N = 150 #150-900
r0 = 2.0
#L = 10 * r0
w0 = 1.0 
γ = 0.0
λ = 0.3 #ss density


Infected = set()
Susceptible = set()
Removed = set()

class Person():
	def __init__(self, x, y, ss):
		self.x = x
		self.y = y
		self.ss = ss #boolean
		#can add more variables for icu etc. 

def dist(p1: Person, p2: Person):
	return ((p1.x-p2.x)**2 + (p1.y-p2.y)**2)**0.5

def generate_random_event(p):
	u = random.random() #float, [0.0, 1.0)
	#print(p, u)
	if u >= 0 and u < p:
		return 1 #u:[0,p)-->event 1
	elif u>= p and u<1:
		return 0 #u: [p,1)-->event 2

#hub model: infection probability
def generate_infection_prob(r:float, alpha:float):
	#mofidy this function for the strong infectiousness model
	if alpha == 2.0:
		rn = r0 #normal
	elif alpha == 0.0:
		rn = (6.0**0.5)*r0 #ss
		alpha = 2.0 #FIXME: better way for signaling ss
	if r <= rn:
		w = w0 * ((1.0-(r/rn))**alpha)
	elif r > rn:
		w = 0
	return w

def simulate():
	#infection
	curr_S = Susceptible.copy()
	curr_I = Infected.copy()
	curr_R = Removed.copy()
	for p in curr_I: #for every infected individual
		for q in curr_S: #infect ppl in the susceptible group
			r = dist(p,q)
			if p.ss == True:
				alpha = 0.0 #ss
			else:
				alpha = 2.0 #normal
			w = generate_infection_prob(r, alpha)
			event = generate_random_event(w)
			if event == 1: #infection
				#move from S to I
				if q in Susceptible:
					Susceptible.remove(q)
				Infected.add(q)

	#recovery
	for p in curr_I:
		event = generate_random_event(γ)
		if event == 1: #recovery/death
			Infected.remove(p)
			Removed.add(p)

	print("S, I, R: ", len(Susceptible), len(Infected), len(Removed)) #SIR


#hub model
#def hub(N:int, r0:float, w0:float, γ:float, λ:float):
def hub():
	L = 10 * r0

	#initialize
	pss = generate_random_event(λ)
	if pss == 1:
		p0 = Person(L/2.0, 0.0, True) #ss
	elif pss == 0:
		p0 = Person(L/2.0, 0.0, False) #normal

	Infected.add(p0)
	for i in range(N-1): #N-1 ppl
		x = random.random()*L
		y = random.random()*L
		pss = generate_random_event(λ)
		if pss == 1:
			pn = Person(x, y, True) #ss
		elif pss == 0:
			pn = Person(x, y, False) #normal
		Susceptible.add(pn)

		#FIXME: assert that N=100 since using sets, e.g. when p1==pn-->N-1

	for i in range(40): #simulate for 40 days
		simulate() 

	#visualization to be added


#hub(N = 150, r0=2.0, w0 = 1.0, γ=0.0, λ=0.9)
hub()