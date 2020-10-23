#pragma once

struct Person
{
	Person() = default;
	Person(double xin, double yin, bool ssin);
	~Person();

	double x, y;
	bool ss;
};
