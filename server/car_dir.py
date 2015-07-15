#!/usr/bin/env python
import Sunfounder_PWM_Servo_Driver.Servo_init as servo
import time                # Import necessary modules

leftPWM = 375
homePWM = 450
rightPWM = 575

def setup():
	global leftPWM, rightPWM, homePWM, pwm
	offset =0
	for line in open('config'):
		if line[0:10] == 'dir_offset':
			offset = int(line[13:-2])
	leftPWM += offset
	homePWM += offset
	rightPWM += offset
	pwm = servo.init()         # Initialize the servo controller.

# ==========================================================================================
# Control the servo connected to channel 0 of the servo control board, so as to make the 
# car turn left.
# ==========================================================================================
def turn_left():
	pwm.setPWM(0, 0, leftPWM)  # CH0

# ==========================================================================================
# Make the car turn right.
# ==========================================================================================
def turn_right():
	pwm.setPWM(0, 0, rightPWM)

# ==========================================================================================
# Make the car turn back.
# ==========================================================================================
def home():
	pwm.setPWM(0, 0, homePWM)

def test():
	while True:
		turn_left()
		time.sleep(1)
		home()
		time.sleep(1)
		turn_right()
		time.sleep(1)
		home()

if __name__ == '__main__':
	setup()
	home()

