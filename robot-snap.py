import time, signal, sys, atexit
import random

import pyupm_grove as grove

import pyupm_uln200xa as upmULN200XA

import pyupm_my9221 as upmMy9221

import pyupm_ttp223 as ttp223

import pyupm_buzzer as upmBuzzer

import pyupm_i2clcd as lcd

# Initialize Jhd1313m1 at 0x3E (LCD_ADDRESS) and 0x62 (RGB_ADDRESS) 
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

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

	global wincount;
	global count;
	global bar_index;

	myUln200xa.setSpeed(7) 
	myUln200xa.setDirection(upmULN200XA.ULN200XA.DIR_CW)
	myUln200xa.stepperSteps(S)

	if (touch.isPressed() == 0):
		wincount += 1
		greenLed.on()
		time.sleep(2)
		greenLed.off()

		myLEDBar.setBarLevel(bar_index + 2)
		bar_index = bar_index + 2;

	else:
		redLed.on()
		buzzer.playSound(upmBuzzer.RE, 1000000)

		time.sleep(2)
		
		redLed.off()
		buzzer.stopSound()
	
	myUln200xa.setDirection(upmULN200XA.ULN200XA.DIR_CCW)
	myUln200xa.stepperSteps(S)
	
	count += 1
	
def reset():

	global wincount;
	global count;
	global bar_index;

	count = 0
	wincount = 0
	bar_index = 0

	greenLed.off()
	redLed.off()
	myLEDBar.setBarLevel(0)
	buzzer.stopSound()
	myLcd.clear()

def teardown():
	global touch, buzzer, greenLed, redLed, myLEDBar, button
	del touch
	del buzzer
	del greenLed
	del redLed
	del myLEDBar
	del button

def main():
	while(1):
		reset()

		myLcd.write("Press Button") 

		while(1):
			if(button.value() != 0):
				break
			time.sleep(1)
		
		myLcd.clear()
		myLcd.write("Total chances: 5")

		time.sleep(3);
		myLcd.clear();

		myLcd.write("Place finger on");
		myLcd.setCursor(1, 0);
		myLcd.write("touch sensor");

		while(count < numChances):
			if (touch.isPressed() == 1):
				rand = random.randint(0,2) # generates random number from 0 and 2
				if(rand == 0):
					slap()
				else:
					bluff()

				myLcd.clear()
				myLcd.write("#Chances left:" + str(numChances - count))
			time.sleep(2)
		
		myLcd.clear()
		myLcd.write("Your score: " + str(wincount) + "/" + str(numChances))	

		time.sleep(2)
		myLcd.clear()

		if(wincount == numChances):
			myLcd.write("Hurray!!");
		else:
			myLcd.write("Better luck");
			myLcd.setCursor(1,0);
			myLcd.write("Next time");

		time.sleep(3);
		myLcd.clear();

	teardown()

main()


