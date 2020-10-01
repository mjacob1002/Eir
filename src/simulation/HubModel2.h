#pragma once
#include <set>
#include<math.h>
// file: source/repos/Eir/Eir/HubModel2.h
struct GenRand;

struct Person;

double dist(Person* a, Person* b);
double gen_inf_prob(double r, bool super);
void s_i(std :: set<Person*> s, std :: set<Person*> i);
void i_r(std::set<Person*> inf);
void simulate();
void init(int nin, double r0in, int numSimsIn, double gammIn, double density, double alphaIn, double rStartIn);
void hub(int nin, double r0in, int numSimsIn, double gammIn, double density, double alphaIn, double rStartIn, double L);
