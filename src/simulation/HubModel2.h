#pragma once
// file: source/repos/Eir/Eir/HubModel2.h
class GenRand;

struct Person;

double dist(Person* a, Person* b);
double gen_inf_prob(double r, bool super);
void s_i(set<Person*> s, set<Person*> i);
void i_r(set<Person*> inf);
void simulate();
void init(int nin, double r0in, int numSimsIn, double gammIn, double density, double alphaIn, double rStartIn);
void hub(int nin, double r0in, int numSimsIn, double gammIn, double density, double alphaIn, double rStartIn, double L);
