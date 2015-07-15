#!/usr/bin/env python
import Sunfounder_PWM_Servo_Driver.Servo_init as servo
import time                # Import necessary modules

offset = 0

homepwm = 550 + offset
leftpwm = 300 + offset
rightpwm = 700 + offset

pwm = servo.init()         # Initialize the servo controller.

# ==========================================================================================
# Control the servo connected to channel 0 of the servo control board, so as to make the 
# car turn left.
# ==========================================================================================
def turn_left():
	pwm.setPWM(0, 0, leftpwm)  # CH0

# ==========================================================================================
# Make the car turn right.
# ==========================================================================================
def turn_right():
	pwm.setPWM(0, 0, rightpwm)

# ==========================================================================================
# Make the car turn back.
# ==========================================================================================
def home():
	pwm.setPWM(0, 0, homepwm)

def test():
	while True:
		turn_left()
		time.sleep(1)
		home()
		time.sleep(1)
		turn_right()
		time.sleep(1)

if __name__ == '__main__':
	test()

