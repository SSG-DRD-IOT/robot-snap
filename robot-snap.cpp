/*
 *  Author: Sisinty Sasmita Patra <sisinty.s.patra@intel.com>
 *  Robot-snap game
 *  Copyright (c) 2015 Intel Corporation.
 *  
 *  Permission is hereby granted, free of charge, to any person obtaining
 *  a copy of this software and associated documentation files (the
 *  "Software"), to deal in the Software without restriction, including
 *  without limitation the rights to use, copy, modify, merge, publish,
 *  distribute, sublicense, and/or sell copies of the Software, and to
 *  permit persons to whom the Software is furnished to do so, subject to
 *  the following conditions:
 *  
 *  The above copyright notice and this permission notice shall be
 *  included in all copies or substantial portions of the Software.
 * 
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 *  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 *  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 *  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 *  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 *  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 *  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *                       
 */

#include <iostream>
#include <sstream>
#include <unistd.h>
#include <time.h>

#include "uln200xa.h"
#include "ttp223.h"
#include "jhd1313m1.h"
#include "my9221.h"
#include <signal.h>
#include "grove.h"
#include <buzzer.h>

using namespace std;

upm::GroveButton* button = new upm::GroveButton(6);

upm::TTP223* touch = new upm::TTP223(4);

upm::ULN200XA* uln200xa = new upm::ULN200XA(4096, 8, 9, 10, 11);

upm::GroveLed* greenled = new upm::GroveLed(2);

upm::GroveLed* redled = new upm::GroveLed(7);

upm::Buzzer* sound = new upm::Buzzer(5);

//upm::Jhd1313m1 *lcd = new upm::Jhd1313m1(0, 0x3E, 0x62);

upm::MY9221* bar = new upm::MY9221(8, 9);

int count = 0; // counts the no. of times swatter slaps, each user gets only 5 chances
int wincount = 0;

int numChances = 5;

int S = 675;
int B = 256;

int bar_index = 0;

void bluff()
{

	uln200xa->setSpeed(7);
	uln200xa->setDirection(upm::ULN200XA::DIR_CW);
	uln200xa->stepperSteps(B);

	uln200xa->setDirection(upm::ULN200XA::DIR_CCW);
	uln200xa->stepperSteps(B);

	sleep(2); //think of making sleep time also random
}

void slap()
{
	// Slapping
	uln200xa->setSpeed(7);
	uln200xa->setDirection(upm::ULN200XA::DIR_CW);
	uln200xa->stepperSteps(S);

	// While slapping if user is not touching then player wins
	if(touch->isPressed() == 0)
	{
		wincount++;
		cout << "turning green led on" << endl;
		greenled->on();
		sleep(2);
		// Turning off for the next chance
		greenled->off();

		cout << "lighting 2 more slots of led bar " << endl;
		bar->setBarLevel (bar_index + 2);
		bar_index = bar_index + 2;
	}
	else
	{
		cout << "turning red led on" << endl;
		redled->on();
		cout << "buzzer sounds " << endl;
		sound->playSound(RE, 1000000);

		sleep(2);

		// Turning off for the next chance
		redled->off();
		// Stop the buzzer sound
		sound->stopSound();
	}

	// Turning swatter to original position
	uln200xa->setDirection(upm::ULN200XA::DIR_CCW);
	uln200xa->stepperSteps(S);

	// Increase count to represent user chances
	count++;
}

void init()
{
	greenled->off();
	redled->off();
	bar->setBarLevel(0);
	sound->stopSound();

	srand(time(0));
}

void teardown()
{
	delete uln200xa;
	delete button;
	delete touch;
	delete greenled;
	delete redled;
	delete bar;
}

int main()
{
	init();

	// numChances for each game
	while(count < numChances)
	{
		if(touch->isPressed() == 1)
		{
			// randomly either bluffs or slaps
			switch(rand()%2)
			{
				case 0: slap(); break;
				case 1: bluff(); break;
			}
			cout << "# of chances used: " << count << endl;

		}
		else
		{
			cout << "place your finger on touch sensor" << endl;
			cout << "Number of remaining chances: " << numChances - count << endl;
		}
	}

	cout << "Your score is : " << wincount << "/" << numChances << endl;

	teardown();

	return 0;
}
