import time, signal, sys, atexit
import random

import pyupm_grove as grove

import pyupm_uln200xa as upmULN200XA

import pyupm_my9221 as upmMy9221

import pyupm_ttp223 as ttp223

import pyupm_buzzer as upmBuzzer

# Create the buzzer object using GPIO pin 5
buzzer = upmBuzzer.Buzzer(5)

# Create the TTP223 touch sensor object using GPIO pin 0
touch = ttp223.TTP223(4)

# Create the button object using GPIO pin 0
button = grove.GroveButton(6)

# Instantiate a ULN2003XA stepper object
myUln200xa = upmULN200XA.ULN200XA(4096, 8, 9, 10, 11)

# Instantiate a MY9221, we use D2 for the data, and D3 for the data clock
myLEDBar = upmMy9221.MY9221(8, 9)

# Create the Grove LED object using GPIO pin 2
greenLed = grove.GroveLed(2)
redLed = grove.GroveLed(7)

count = 0 	# counts the no. of times swatter slaps, each user gets only 5 chances
wincount = 0    #counts the no. of times user wins

numChances = 5; # total no. of chances user gets

S = 675;
B = 256;

bar_index = 0;

def bluff():
	myUln200xa.setSpeed(7) 
	myUln200xa.setDirection(upmULN200XA.ULN200XA.DIR_CW)
	myUln200xa.stepperSteps(B)

	myUln200xa.setDirection(upmULN200XA.ULN200XA.DIR_CCW)
	myUln200xa.stepperSteps(B)

	time.sleep(2);

def slap():
	global wincount
	global bar_index
	global count

	myUln200xa.setSpeed(7) 
	myUln200xa.setDirection(upmULN200XA.ULN200XA.DIR_CW)
	myUln200xa.stepperSteps(S)

	if (touch.isPressed() == 0):
		wincount += 1
		print "Turning green led on \n"
		greenLed.on()
		time.sleep(2)
		greenLed.off()

		print "Lighting 2 more slots of ledbar \n"
		myLEDBar.setBarLevel(bar_index + 2)
		bar_index = bar_index + 2;

	else:
		print "Turning red led on \n"
		redLed.on()
		#buzzer.playSound(upmBuzzer.RE, 1000000)

		time.sleep(2)
		
		redLed.off()
		print "stopping buzzer sound \n"
		#buzzer.stopSound()
	
	myUln200xa.setDirection(upmULN200XA.ULN200XA.DIR_CCW)
	myUln200xa.stepperSteps(S)
	
	count += 1
	
def init():
	greenLed.off()
	redLed.off()
	myLEDBar.setBarLevel(0)
	buzzer.stopSound()

def teardown():
	global touch, buzzer, greenLed, redLed, myLEDBar, button
	del touch
	del buzzer
	del greenLed
	del redLed
	del myLEDBar
	del button

def main():
	init()
	while(count < numChances):
		if (touch.isPressed() == 1):
			rand = random.randint(0,2) # generates random number from 0 and 2
			if(rand == 0):
				slap()
			else:
				bluff()
			print "# of chances used: %d" %count
		else:
			print "place finger on touch sensor"
			print "# of remaining chances %d" % (numChances - count)
	
	print "your score is: %d / %d " % (wincount, numChances)

	teardown()

main()


