#pragma once 
#include "people_generator.h"
#include <iostream>
using namespace std;

int main()
{
	queue<float> vipwaiting;
	queue<float> normalwaiting;
	float a;
		float b;
	long N;
	cout << "Please enter the number of iterations" << endl;
	cin >> N;
	cout << "Please enter the mean of people" << endl;
	cin >> a;
	cout << "Please enter the mean of waiting Time" << endl;
	cin >> b;
	//the N loop will be here 
	for (int n = 0; n < N; n++)
	{

		people_generator generator = people_generator(a, b);
		generator.generate();
	
		
		float timer = 0.0f;
		queue<people> vip;
		queue<people> normal;

		people * assigned = NULL;
		while (!generator.queue.empty() || !normal.empty() || !vip.empty() )
		{
			if (timer > 360)
				break;
			
			timer += 0.1;
			while (!generator.queue.empty() && generator.queue.front().time_arrieved <= timer)
			{
				if (!normal.empty() && generator.queue.front().privleage)
					vip.push(generator.queue.front());
				else
					normal.push(generator.queue.front());
				generator.queue.pop();
			}

			if (assigned == NULL || (assigned->starttime + assigned->waiting_time) <= timer)
			{
				if(assigned !=NULL){

					if (assigned->privleage)
					vipwaiting.push(assigned->starttime - assigned->time_arrieved);
				else
					normalwaiting.push(assigned->starttime - assigned->time_arrieved);
					assigned = NULL;
				}
				if (!vip.empty())
				{
					//if(n==70)
					//cout << "got it" << endl;
					people temp ;
					temp.privleage = vip.front().privleage;
					temp.waiting_time = vip.front().waiting_time;
					temp.time_arrieved = vip.front().time_arrieved;
					temp.starttime = timer;
				//	cout << timer << endl;
				//	cout << temp.waiting_time << endl;
					vip.pop();
					assigned = &temp;
				}
				else if (!normal.empty())
				{

					people temp;
					temp.privleage = normal.front().privleage;
					temp.starttime = timer;
					temp.waiting_time = normal.front().waiting_time;
					temp.time_arrieved = normal.front().time_arrieved;
					//cout << timer << endl;
					//cout << temp.starttime << endl;
					normal.pop();
					assigned = &temp;

				}
			}
		}	
	//cout <<n << endl;
	}
	//the end of n loop
	int profit = vipwaiting.size()*30;
	int vipsize = vipwaiting.size();
	int normalsize = normalwaiting.size();
	float vipsum = 0.0f;
	float normalsum =0.0f;
	while (!vipwaiting.empty())
	{
		vipsum += vipwaiting.front();
		vipwaiting.pop();
	}
	while (!normalwaiting.empty())
	{
		normalsum += normalwaiting.front();
		normalwaiting.pop();
	}
	//the end of n loop
	float vipavg = vipsum / vipsize;
	float normalavg = normalsum / normalsize;
	float  totalavg = (vipsum + normalsum) / (vipsize + normalsize);
	cout << "vipavg = " << vipavg <<endl;
	cout << "normalavg = " << normalavg << endl;
	cout << "totalavg = " << totalavg << endl;
	cout << " the profit is = " << profit <<endl;
	system("pause");
	return 0;
}
