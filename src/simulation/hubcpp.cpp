#include <iostream>
#include<set>
#include<math.h>
#include<stdlib.h>
#include<time.h>


using namespace std;

int N = 899;
double r0 = 2.0;
double w0 = 1.0;
double gamm = .63;
double density = 0.4;


struct Person {
    // point coordinates x and y
    double x, y;
    // boolean value of whether the person is a superspreader
    bool ss;

    Person(double x, double y, bool ss) {
        this->x = x;
        this->y = y;
        this->ss = ss;
    }
};

set<Person*> infected;
set<Person*> susceptibles;
set<Person*> removed;


double dist(Person* p1, Person* p2);
double dist(Person* p1, Person* p2) {
    double deltax = pow((*p1).x - (*p2).x, 2);
    double deltay = pow((*p1).y - (*p2).y, 2.0);
    double sum = deltax + deltay;
    return pow(sum, 0.5);
}

int generate_random_event(double p);
int generate_random_event(double p) {
    // initial seed random number generator
    srand((unsigned)time(NULL));
    // generate a random number
    double u = (float) rand()/RAND_MAX;
    // [0,p) --> event 1
    if (u >= 0 && u < p) {
        return 1;
    }
    // [p,1) --> event 2
    else {
        return 0;
    }
}

double generate_inf_prob(double r, double alpha);
double generate_inf_prob(double r, double alpha) {
    double rn;
    if (alpha == 2.0) {
        // normal person
        rn = r0;
    }
    else if (alpha == 0.0) {
        // superspreader
        rn = pow(6.0, 0.5) * r0;
    }
    double w;
    if (r <= rn) {
        w = w0 * ((1.0 - pow((r / rn), alpha)));
    }
    else {
        w = 0;
    }
    return w;
}

void simulate();

void simulate() {
    set<Person*> curr_S = susceptibles;
    set<Person*> curr_I = infected;
    set<Person*> curr_R = removed;

    for (Person* p : curr_I) {
        for (Person* q : curr_S) {
            double r = dist(p, q);
            double alpha;
            if (p->ss == true) {
                // super spreaders
                alpha = 0.0;
            }
            else {
                // normal person
                alpha = 2.0;
            }
            double w = generate_inf_prob(r, alpha);
            int event = generate_random_event(gamm);
            if (event == 1) {
                if (susceptibles.find(q) != susceptibles.end()) {
                    susceptibles.erase(q);
                }
                infected.insert(q);
            }
        }
    }

    for (Person* p : infected) {
        int event = generate_random_event(gamm);
        if (event == 1) {
            infected.erase(p);
            removed.insert(p);
        }
    }

    cout << "S, I, R: " << susceptibles.size() << " " << infected.size() << " " << removed.size() << endl;
}
void hub();
void hub() {
    double L = 10 * r0;
    // initialize 
    int pss = generate_random_event(density);
    if (pss == 1) {
        // superspreader
        Person* p0 = new Person(L / 2.0, 0.0, true);
        infected.insert(p0);
    }
    else {
        Person* p0 = new Person(L / 2.0, 0.0, false);
        infected.insert(p0);
    }

    for (int i = 0; i < N - 1; i++) {
        double x = L * rand();
        double y = L * rand();
        pss = generate_random_event(density);
        Person* pn;
        if (pss == 1) {
            pn = new Person(x, y, true);
        }
        else {
            pn = new Person(x, y, false);
        }
        susceptibles.insert(pn);
    }
    // FIXME: assert that N=100 since using sets, e.g. when p1==pn-->N-1
    for (int i = 0; i < 40; i++) {
        simulate();
    }
}

int main() {
    hub();
}
