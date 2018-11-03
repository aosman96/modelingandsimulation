#pragma once
#include "people.h"
#include <time.h> // So we can use time() function
#include <iostream> // To output results to console
#include <math.h> 
#include <queue> 
#include <random>
#include <chrono>
using namespace std;
class people_generator
{
public:
	queue <people> queue;
	float mean_people;
	float mean_waiting;
	float waiting_generation();
	int profit;
	void  generate();
	people_generator( float mean, float mean_waiting);
	~people_generator();
};

