arduino-qt-toogle-led
=====================

This is a very simple example of how to build an instrument that communicates via
exchanging text messages using arduino and lantz.

Requirements
------------

- Install the latest version of lantz

- Install arduino-cli
  https://github.com/arduino/arduino-cli
  
- Copy all the content of this folder to your computer

If you do not have the NI-VISA installed, you need to install `pyvisa-py`
(the pure python backend for pyvisa) and tell lantz to use it by default

In the command line:

    pip install pyvisa-py
    pip install pyserial
    lantz config core.visa_backend '@py'


Step 1: Create arduino sketch template
--------------------------------------

In the console, go to the folder containing this project and execute the following
command:

    lantz ino new run:TemperatureSensor
    
This will generate an arduino sketch template for the class `LEDDriver`
located in the `run` module. You will find it in the LEDDriver just created directory.
It additionally creates a "packfile" named `LEDDriver.pack.yaml` that
contains information to compile and upload the project.


Step 2: Add your own code to the arduino sketch
-----------------------------------------------

You can customize the arduino code by editing `inodriver_user.cpp` and 
`inodriver_user.h` within the sketch directory created in step 1. 

You will find the following functions:

- user_setup: this will be executed during the setup of the arduino just before starting
  the communication with the serial command.
  
- user_loop: this will be executed every time the main loop is executed

- ... and one function for each getter/setter you have in your lantz code.

In order to get the onboard LED turned on an off, we need to modify the 
`inodriver_user.cpp` file in the following manner:
```
... stuff ...
void user_setup() {
   pinMode(13, OUTPUT);
}
... stuff ...
int set_LED(int value) {
   if (value>0)
      digitalWrite(13, HIGH);
   else
      digitalWrite(13, LOW);
   return 0;
};
... stuff ...
```


Step 3: Run it
--------------
 
In the console, go to the directory containing this project and execute the following
command:

    python run.py

This should open the graphical interface with two buttons, one to turn the LED on
and the other to turn the LED off. 

<p align="center">
  <img width="460" src="https://raw.githubusercontent.com/SengerM/examples/master/arduino-qt-toogle-led/img/1.png">
</p>
