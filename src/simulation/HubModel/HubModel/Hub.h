#pragma once

#include <set>
#include <math.h>
#include <vector>

#include "GenRand.h"
#include "Person.h"


class Hub {
protected:
	int N;
	double r0;
	int numSims;
	double w0;
	double gamm;
	double density;
	int alpha;
	double rstart;
	double L;
	//keeps track of the total number of people per compartment each day/hour
	std::vector<size_t> num_s;
	std::vector<size_t> num_i;
	std::vector<size_t> num_r;

	int temp = 0; // will be used to keep track of the number of superspreaders generated
	GenRand gr;
	std::set<Person*> susceptibles;
	std::set<Person*> infected;
	std::set<Person*> removed;
	double dist(Person* a, Person* b);
	virtual double gen_inf_prob(double r, bool super);
	void s_i(std::set<Person*> s, std::set<Person*> i);
	void i_r(std::set<Person*> inf);
	void simulate();

public:
	Hub() {}
	~Hub() {}
	Hub(int nin, double r0in, int numSimsIn, double w0In, double gammIn, double densityIn, int alphaIn, double rstartIn, double L);
	std :: vector<std :: vector<size_t>> getVectors();
	void run();
	void printVector();
};