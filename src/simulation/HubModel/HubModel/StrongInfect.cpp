#include "StrongInfect.h"
// implementation of Fujie and Odagaki
StrongInfect::StrongInfect(int nin, double r0in, int numSimsIn, double w0In, double gammIn, double densityIn, int alphaIn, double rstartIn, double L) 
: Hub(nin, r0in, numSimsIn, w0In, gammIn, densityIn, alphaIn, rstartIn, L) // call superclass constructor
{
	
}


 double StrongInfect::gen_inf_prob(double r, bool ss) {
	 double rn = rstart;
	 double w;
	 // if within the radius of infection
	 if (r < rn) {
		 // if a superspreader the probability of infection
		 if (ss) {
			 return w0;
		 }
		 else {
			 w = w0 * (1 - pow(r / rn, 2));
			 return w;
		 }
	 }
	 else {
		 return 0;
	 }
}