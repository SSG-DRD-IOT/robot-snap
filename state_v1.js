//set up start button and touch sensor
var groveSensor = require('jsupm_grove');
var button = new groveSensor.GroveButton(4); // start button on gpio 4
var touch = new groveSensor.GroveButton(3); // touch sensor on gpio 3

//set up stepper, forward and reverse functions

var Uln200xa_lib = require('jsupm_uln200xa');
var myUln200xa_obj = new Uln200xa_lib.ULN200XA(4096, 8, 9, 10, 11); //stepper pins in 1-4 to gpio 8-11

myUln200xa_obj.forward = function()
{
    myUln200xa_obj.setSpeed(5); // 5 RPMs
    myUln200xa_obj.setDirection(Uln200xa_lib.ULN200XA.DIR_CW);
    console.log("Rotating 1/4 revolution clockwise.");
    myUln200xa_obj.stepperSteps(1000);
};

myUln200xa_obj.reverse = function()
{
        console.log("Rotating 1/4 revolution counter clockwise.");
        myUln200xa_obj.setDirection(Uln200xa_lib.ULN200XA.DIR_CCW);
        myUln200xa_obj.stepperSteps(1000);
};


//set up LCD
var LCD = require('jsupm_i2clcd'); //LCD on any I2C
var myLcd = new LCD.Jhd1313m1(0);

//set initial states

var button_state = 0;
var previous = 0;
var num_pressed = 0;
var game_state =false;
var touch_val = 0;


while (1){

	//set game state to true or false (switches on each button press)
if ( previous==0 && button.value()!=button_state){
        button_state = button.value();
        previous = 1;
        game_state ^= true;
        console.log(game_state); //print game state to console
        }

else if ( previous ==1 && button.value()!=button_state){
        button_state = button.value();
        previous = 0;
        
}

//4 states of game:

if (game_state == true && touch.value() == 0){ //if game started and no touch
        myLcd.setCursor(0,1)
        myLcd.write('Touch me!     ')
        //console.log('g1 t0') //monitor states
}

else if (game_state == false && touch.value() == 0){ //if game not started and no touch
        myLcd.setCursor(0,1)
        myLcd.write('Press Start!     ')
        //console.log('g0 t0') //monitor states
}

else if (game_state == true && touch.value() == 1){ //if game started and touch
        myLcd.setCursor(0,1)
        myLcd.write('Ready??     ')
        myUln200xa_obj.forward(); //start to slap
        if (touch.value() == 1) //if touching at end of slap: Gotchya!
                {
                myLcd.setCursor(0,1);
                myLcd.write('Gotchya!');
                }
        myUln200xa_obj.reverse(); //bring back to starting position

       //console.log('g1 t1') //monitor states
}

else if (game_state == false && touch.value() == 1){ //if game not started and touch
        myLcd.setCursor(0,1)
        myLcd.write('Press Start!     ')
        //console.log('g0 t1') //monitor states
} 

}

