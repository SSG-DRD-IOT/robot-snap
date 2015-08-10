Robot-Snap
==========

Robotic slapping game using Intel Edison and showcasing the use of different programming languages to achieve the same result: Node.js and C++.

Game Description
----------------

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
[Robot-snap algorithm](/algorithm.txt)

Installation
------------
Node.js:
No installation or dependencies needed...yet 

Credits
-------
-Martin Kronberg

-Sisinty Sasmita Patra

