// HubModel.cpp : Defines the entry point for the application.
//
#include <iostream>
#include <stdio.h>
#include "Hub.h"
#include "StrongInfect.h"


// file: source/repos/Eir/Eir/HubModel2.cpp
using namespace std;



int main() {
	std::cout << "Starting Program: " << std::endl;
	Hub x = Hub(9999, 2.0, 40, 1, 0.2, 0.1, 4, 40, 2500);
	x.run();
	StrongInfect y = StrongInfect(5999, 2.0, 20, 1, 0.2, 0.1, 4, 40, 2500);
	cout << endl;
	y.run();
	
	// std::cout << "Number of Super Spreaders: " << temp << std::endl;
	std::cout << "Vectors Content" << std::endl;
	y.printVector();
	// std::cout << "Susceptibles: " << std::endl;
	//for (int i :  num_s) {
	//	std::cout << i << std::endl;
	//}
	//std::cout << "Infected" << std::endl;
	//for (int i : num_i) {
	//	std::cout << i << std::endl;
	//}
	std::cout << "Ending Program" << std::endl;
}
