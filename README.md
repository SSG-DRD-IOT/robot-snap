Robot-Snap
==========

Robotic slapping game using Intel Edison and showcasing the use of different programming languages to achieve the same result: Node.js and C++.

Game Description
================

* We can trigger the beginning of a game using a button.

* Every player will get 5 tries. They will place their hand on the table on top of the touch sensor. The goal is to avoid getting slapped by the swatter.

* There will be 3 Scenarios:
** Bluff - when the user takes his hand while robot-snap is bluffing.
** Win - when the user takes his hand while robot–snap is going to hit. (Green LED will light up)
** Lose - when the user does not take his hand while robot–snap is going to hit. (Red LED will Light up + buzzer sound)

* We will use an LED bar to keep score. The LED bar has 10 light indicators. After every win, we will light up 2 of the indicators.

* We will calculate the average response time (how fast a user removes his/her hand). After a user finishes, we will display the info on the LCD screen along with the ranking compared to other users.

* Per user, we will also upload the response time to the cloud per try. This way, the users can see a graph with how their response time is “improving” or “degrading” after each try.

Hardware Requirements
---------------------

* Intel Edison Board + Arduino breakout
* Stepper Motor
* Touch Sensor
* LED - Red, Green
* Swatter
* Buzzer
* Button to start playing
* Grove LED bar
* LCD Display.

Assembly
--------
Assembly instructions to come.

Algorithm Outline
-----------------

Initialize all sensors

Initialize X to 5
Initialize D to some large steps to cover slapping
Initialize B to small number of steps to cover bluffing

Initialize count to zero

* If Touch sensor is pressed
        * Loop until count reaches X
                * generate a random number (p) between 0 and 1
                * if p is 0 (corresponds to slaps)
                        * Move swatter D degrees (slapping) Clockwise
                        * Move swatter D degrees (slapping) Counter Clockwise
                        * if swatter hits the user.
                                * Turn red led on and buzzer
                        * else
                                * Turn green led on and light 2 more slots of Led bar.
                        * increment count
                * else (corresponds to bluff)
                        * Move swatter B degrees clockwise
                        * Move swatter B degrees counter clockwise

Installation
------------
Node.js:
No installation or dependencies needed...yet 

Credits
-------
-Martin Kronberg

-Sisinty Sasmita Patra

