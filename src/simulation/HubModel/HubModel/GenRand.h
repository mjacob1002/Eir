#pragma once

struct GenRand {
	GenRand();
	~GenRand();

	double rando();
	int generate_event(double p);
	int generate_inf_event(double w);
	int generate_recov_event(double p);

};