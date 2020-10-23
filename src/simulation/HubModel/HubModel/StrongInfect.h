#include "Hub.h"

class StrongInfect : public Hub {
public:
	StrongInfect() {}
	StrongInfect(int nin, double r0in, int numSimsIn, double w0In, double gammIn, double densityIn, int alphaIn, double rstartIn, double L);
	~StrongInfect(){}
	double gen_inf_prob(double r, bool ss) override;
};