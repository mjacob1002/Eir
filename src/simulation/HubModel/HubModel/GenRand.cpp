#include "GenRand.h"
#include <cstdlib>
#include <ctime>

GenRand::GenRand()
{
	srand((unsigned int)time(NULL));
}

GenRand::~GenRand()
{}
/// <summary>
/// generates a random decimal from [0,1)
/// </summary>
/// <returns></returns>
double GenRand::rando() {
	double x = 1.0 * rand() / RAND_MAX;
	return x;
}
/// <summary>
/// generates a random event
/// </summary>
/// <param name="p"></param>
/// <returns></returns>
int GenRand::generate_event(double p)
{
	double x = rando();
	if (0 <= x && x < p)
	{
		return 1;
	}
	return 0;
}
/// <summary>
/// generates a random infection event
/// </summary>
/// <param name="p"></param>
/// <returns></returns>
int GenRand::generate_inf_event(double w) {
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
/// <summary>
/// generates a random recover event
/// </summary>
/// <param name="p"></param>
/// <returns></returns>
int GenRand::generate_recov_event(double p) {
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