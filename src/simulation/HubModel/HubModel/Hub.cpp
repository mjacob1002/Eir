#include "Hub.h"
#include <iostream>
#include <stdlib.h>
#include <time.h>

// file: source/repos/Eir/Eir/HubModel2.h
// implementation of Fujie and Odagaki
Hub::Hub(int nin, double r0in, int numSimsIn, double w0In, double gammIn, double densityIn, int alphaIn, double rstartIn, double lIn) 
{
	// total number of people in population
	N = nin;
	// the r0 value
	r0 = r0in;
	// number of time periods simulated
	numSims = numSimsIn;
	// starting probability of being 0 units away from infected
	w0 = w0In;
	// the probability of going from infected to recovered
	gamm = gammIn;
	// the density of super spreaders
	density = densityIn;
	// to be used in formula for calculating probability of infection
	alpha = alphaIn;
	// the radius of infected people and where they can spread
	rstart = rstartIn;
	// size of the plane of simulation
	L = lIn;

}

/// <summary>
/// determines the distance between two people using Pythagorean theorem
/// </summary>
/// <param name="a"></param>
/// <param name="b"></param>
/// <returns></returns>
double Hub :: dist(Person* a, Person* b) {
	double deltax = pow((*a).x - (*b).x, 2);
	double deltay = pow((*a).y - (*b).y, 2);
	double distance = deltax + deltay;
	return pow(distance, 0.5);
}
 /// <summary>
 /// Generate the Infection Probability for the Hub Model assumptions
 /// </summary>
 /// <param name="r"></param>
 /// <param name="super"></param>
 /// <returns></returns>
 double Hub :: gen_inf_prob(double r, bool super) {
	double rn = rstart;
	double w;
	if (super) {
		rn = pow(6, 0.5) * rstart;
	}

	if (r < rn) {
		w = w0 * ((1.0 - pow((r / rn), alpha)));
	}

	else {
		w = 0;
	}

	return w;
}
// deals with transition from susceptibles to infected. Takes in copies of S and I sets
void Hub :: s_i(std::set<Person*> s, std::set<Person*> i) {
	for (Person* p : i) {
		for (Person* q : s) {
			double r = dist(p, q);
			//cout << "SI r: " << r << endl;
			double w = gen_inf_prob(r, p->ss);
			int event = gr.generate_inf_event(w);
			//cout << "Event: " << event << endl;
			// if there is an infection, change the sets accordingly
			if (event == 1) {
				//change the class sets
				if (susceptibles.find(q) != susceptibles.end()) {
					susceptibles.erase(q);
				}
				infected.insert(q);
			}

		}

	}
}
// transition from Infected to Removed
void Hub :: i_r(std::set<Person*> inf) {
	for (Person* p : inf) {
		int event = gr.generate_recov_event(gamm);
		if (event == 1) {
			infected.erase(p);
			removed.insert(p);
		}
	}
}
void Hub :: simulate() {
	// copy sets
	std::set<Person*> currS = susceptibles;
	std::set<Person*> currI = infected;
	s_i(currS, currI);
	i_r(currI);
	std::cout << "S, I, R: " << susceptibles.size() << " " << infected.size() << " " << removed.size() << std::endl;
	// add information to the vectors
	num_s.push_back(susceptibles.size());
	num_i.push_back(infected.size());
	num_r.push_back(removed.size());
}

/// <summary>
/// Runs a simulation of the object type. i.e for hub objects, run will perform a Hub Model Simulation
/// </summary>
void Hub :: run() {
	int pss = gr.generate_event(density);
	if (pss == 1) {
		// add to the super spreader count
		temp++;
		Person* p0 = new Person(L / 2, 0.0, true);
		infected.insert(p0);
	}
	else {
		Person* p0 = new Person(L / 2, 0.0, false);
		infected.insert(p0);
	}
	for (int i = 0; i < N - 1; i++) {
		double x = gr.rando() * L;
		double y = gr.rando() * L;
		int prob = gr.generate_event(density);
		//cout << "x: " << x << " y: " << y << " Prob " << prob << endl;
		Person* pn;
		if (prob == 1) {
			pn = new Person(x, y, true);
			temp++;
		}
		else {
			pn = new Person(x, y, false);
		}
		susceptibles.insert(pn);
	}
	std::cout << "Initial Susceptible: " << susceptibles.size() << std::endl;
	num_s.push_back(susceptibles.size()); 
	num_i.push_back(infected.size());
	num_r.push_back(removed.size());
	for (int i = 0; i < numSims; i++) {
		simulate();
	}
}
/// <summary>
/// returns the vectors that include the different amounts of S, I, and R
/// </summary>
/// <returns></returns>
std::vector<std::vector<size_t>> Hub::getVectors() {
	return { num_s, num_i, num_r };
}

void Hub :: printVector() {
	std :: cout << "Susceptibles : " << std::endl;
	for (size_t i : num_s) {
		std :: cout << i << std :: endl;
	}
	std::cout << "Infected : " << std::endl;
	for (size_t i : num_i) {
		std::cout << i << std::endl;
	}
	std::cout << "Removed: " << std::endl;
	for (size_t i : num_r) {
		std::cout << i << std::endl;
	}
}

