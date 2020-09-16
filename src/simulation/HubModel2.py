# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 14:28:01 2020

@author: mjaco
"""
import random
from matplotlib import pyplot as plt
import numpy as np

N = 899  # 150-900
r0 = 2.0
# L = 10 * r0
w0 = 1.0
γ = .32
λ = 0.4  # ss density
icu = 0.04
gamma_icu = .16
time = 40
Infected = set()  # infected but not icu
Susceptible = set()  # susceptible
Removed = set()  # removed from infectious cycle
ICU = set()  # infected and in icu

S, I, intense_care, R = np.zeros(time + 1), np.zeros(time + 1), np.zeros(time + 1), np.zeros(time + 1)
S[0], I[0], intense_care[0], R[0] = len(Susceptible), len(Infected), len(ICU), len(Removed)

t = np.zeros(time + 1)
for i in range(time + 1):
	t[i] = i


class Person:
	def __init__(self, x: float, y: float, ss: bool):
		self.x = x
		self.y = y
		self.ss = ss


# can add more variables for icu etc.


def dist(p1: Person, p2: Person):
	return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


def generate_random_event(p):
	u = random.random()  # float, [0.0, 1.0)
	# print(p, u)
	if 0 <= u < p:
		return 1  # u:[0,p)-->event 1
	elif p <= u < 1:
		return 0  # u: [p,1)-->event 2


# hub model: infection probability
def generate_infection_prob(r: float, alpha: float):
	# modify this function for the strong infectiousness model
	if alpha == 2.0:
		rn = r0  # normal
	elif alpha == 0.0:
		rn = (6.0 ** 0.5) * r0  # ss
		alpha = 2.0  # FIXME: better way for signaling ss
	if r <= rn:
		w = w0 * ((1.0 - (r / rn)) ** alpha)
	elif r > rn:
		w = 0
	return w


def simulate(location: int):
	# infection
	curr_S = Susceptible.copy()
	curr_I = Infected.copy()
	curr_icu = ICU.copy()
	# from S to I
	for p in curr_I:  # for every infected individual
		for q in curr_S:  # infect ppl in the susceptible group
			r = dist(p, q)
			if p.ss:
				alpha = 0.0  # ss
			else:
				alpha = 2.0  # normal
			w = generate_infection_prob(r, alpha)
			event = generate_random_event(w)
			if event == 1:  # infection
				# move from S to I
				if q in Susceptible:
					Susceptible.remove(q)
				Infected.add(q)
	# people going from infected to ICU
	for p in curr_I:
		event = generate_random_event(icu)
		# you go to the icu
		if event == 1:
			Infected.remove(p)
			ICU.add(p)

	# recovery
	for p in curr_I:
		event = generate_random_event(γ)
		if event == 1:  # recovery/death
			if p in Infected:
				Infected.remove(p)
			Removed.add(p)

	for p in curr_icu:
		event = generate_random_event(gamma_icu)
		if event == 1:
			ICU.remove(p)
			Removed.add(p)

	print("S, I, ICU, R: ", len(Susceptible), len(Infected), len(ICU), len(Removed))  # SIR
	S[location], I[location], intense_care[location], R[location] = len(Susceptible), len(Infected), len(
		ICU), len(Removed)


# hub model
# def hub(N:int, r0:float, w0:float, γ:float, λ:float):
def hub():
	L = 10 * r0

	# initialize
	pss = generate_random_event(λ)
	if pss == 1:
		p0 = Person(L / 2.0, 0.0, True)  # ss
	elif pss == 0:
		p0 = Person(L / 2.0, 0.0, False)  # normal

	Infected.add(p0)
	for i in range(N - 1):  # N-1 ppl
		x = random.random() * L
		y = random.random() * L
		pss = generate_random_event(λ)
		if pss == 1:
			pn = Person(x, y, True)  # ss
		elif pss == 0:
			pn = Person(x, y, False)  # normal
		Susceptible.add(pn)

	# FIXME: assert that N=100 since using sets, e.g. when p1==pn-->N-1

	for i in range(1, time + 1):  # simulate for 40 days
		simulate(i)
		print(i)
	plotting()


# visualization to be added

def plotting():
	plt.plot(t, intense_care, label="ICU")
	plt.plot(t, I, label="Infected")
	plt.plot(t, R, label="Removed")
	plt.plot(t, S, label="Susceptible")
	plt.legend()
	plt.show()


# hub(N = 150, r0=2.0, w0 = 1.0, γ=0.0, λ=0.9, icu = 0.04)
hub()
