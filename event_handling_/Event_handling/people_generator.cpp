#include "people_generator.h"



float people_generator::waiting_generation()
{
	float randNum = 1;
	while (randNum == 1)
	 randNum = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
	
	float waiting_time = log(1 - randNum) / (-1 / this->mean_waiting);
	return waiting_time;
}

void  people_generator::generate()
{
	float counter = 0.0f;
	while (counter <360 )
	{
		float randNum =1;
	while(randNum == 1)
	 randNum = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
	float time_after = log(1 - randNum) / (-1 / this->mean_people);
	//cout << time_after<<endl;
	people generated ;
	generated.time_arrieved = counter + time_after;
	
	float waiting_generated = this->waiting_generation();
	generated.waiting_time = waiting_generated;

	generated.busy = false;
	generated.privleage = ((static_cast <float> (rand()) / static_cast <float> (RAND_MAX)) >= 0.5) ? true : false;
		queue.push(generated);
		counter += time_after;
	}
}

people_generator::people_generator(float mean_people , float mean_time)
{
	this->mean_people = mean_people;
	this->mean_waiting = mean_time;
}


people_generator::~people_generator()
{
}
