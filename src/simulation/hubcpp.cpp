#include <iostream>
#include<math.h>
#include<set>
#include<stdlib.h>
#include<time.h>
#include "HubModel2.h"

// file: source/repos/Eir/Eir/HubModel2.cpp

using namespace std;
// class to generate random numbers and events
struct GenRand {
public:
	GenRand() {
		srand((unsigned int)time(NULL));
	}

	double rando() {
		double x = 1.0 * rand() / RAND_MAX;
		return x;
	}

	int generate_event(double p) {
		double x = rando();
		if (0 <= x && x < p) {
			return 1;
		}
		return 0;
	}

	int generate_inf_event(double w) {
		double x = rando();
		if (w == 0) {
			return 0;
		}
		else if (x < w) {
			return 1;
		}
		else {
			return 0;
		}
	}

	int generate_recov_event(double p) {
		double x = rando();
		if (p == 0) {
			return 0;
		}
		else if (x < p) {
			return 1;
		}
		else {
			return 0;
		}
	}
};
// houses all the data for a simulated person, incluing (x,y) position and bool to determine whether a superspreader
struct Person {
	double x, y;
	bool ss;
	
	Person(double xin, double yin, bool ssin) {
		x = xin;
		y = yin;
		ss = ssin;
	}
};

int N = 17899;
double r0 = 2.0;
int numSims = 80;
double w0 = 1.0;
double gamm = 0.2;
double density = 0.1;
int alpha = 4;
double rstart = 40;

int temp = 0;
GenRand gr = GenRand();
set<Person*> susceptibles;
set<Person*> infected;
set<Person*> removed;

double dist(Person* a, Person* b) {
	double deltax = pow((*a).x - (*b).x, 2);
	double deltay = pow((*a).y - (*b).y, 2);
	double distance = deltax + deltay;
	return pow(distance, 0.5);
}

double gen_inf_prob(double r, bool super) {
	double rn = rstart;
	double w;
	if (super) {
		rn = pow(6, 0.5) * rstart;
	}
	//cout << "R: " << r;
	//cout << " Rn: " << rn;
	if (r < rn) {
		w = w0 * ((1.0 - pow((r / rn), alpha)));
	}

	else {
		w = 0;
	}
	//cout << " P(Infection) = " << w << endl;
	return w;
}
// deals with transition from susceptibles to infected
void s_i(set<Person*> s, set<Person*> i) {
	for (Person* p : i) {
		for (Person* q : s) {
			double r = dist(p, q);
			//cout << "SI r: " << r << endl;
			double w = gen_inf_prob(r, p->ss);
			int event = gr.generate_inf_event(w);
			//cout << "Event: " << event << endl;
			// if there is an infection, change the sets accordingly
			if (event == 1) {
				if (susceptibles.find(q) != susceptibles.end()) {
					susceptibles.erase(q);
				}
				infected.insert(q);
			}

		}

	}
}
// transition from Infected to Removed
void i_r(set<Person*> inf) {
	for (Person* p : inf) {
		int event = gr.generate_recov_event(gamm);
		if (event == 1) {
			infected.erase(p);
			removed.insert(p);
		}
	}
}
void simulate() {
	set<Person*> currS = susceptibles;
	set<Person*> currI = infected;
	s_i(currS, currI);
	i_r(currI);
	cout << "S, I, R: " << susceptibles.size() << " " << infected.size() << " " << removed.size() << endl;
}

void init(int nin, double r0in, int numSimsIn, double gammIn, double density, int alphaIn, double rStartIn) {
	N = nin;
	r0 = r0in;
	numSims = numSimsIn;
	gamm = gammIn;
	density = density;
	alpha = alphaIn;
	rstart = rStartIn;
}

void hub(int nin, double r0in, int numSimsIn, double gammIn, double density, int alphaIn, double rStartIn, double L) {
	init(nin, r0in, numSimsIn, gammIn, density, alphaIn, rStartIn);
	int pss = gr.generate_event(density);
	if (pss == 1) {
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
		cout << "x: " << x << " y: " << y << " Prob " << prob << endl;
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
	cout << "Initial Susceptible: " << susceptibles.size() << endl;
	for (int i = 0; i < numSims; i++) {
		simulate();
	}
}

int main() {
	cout << "Starting Program: " << endl;
	hub(17899, 2.0, 80, 0.2, 0.1,4, 40, 2500);
	cout << "Number of Super Spreaders: " << temp << endl;
	cout << "Ending Program" << endl;
}
