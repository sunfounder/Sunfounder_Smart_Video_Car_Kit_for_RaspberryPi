#!/usr/bin/env python
import Sunfounder_PWM_Servo_Driver.Servo_init as servo
import time                  # Import necessary modules

MinPluse  = 150
MaxPluse  = 600

Current_x = 375
Current_y = 375

pwm = servo.init()           # Initialize the servo controller. 

# ==========================================================================================
# Control the servo connected to channel 14 of the servo control board to make the camera 
# turning towards the positive direction of the x axis.
# ==========================================================================================
def move_increase_x():
	global Current_x
	Current_x += 25
	if Current_x > MaxPluse:
		Current_x = MaxPluse
        pwm.setPWM(14, 0, Current_x)   # CH14 <---> X axis
# ==========================================================================================
# Control the servo connected to channel 14 of the servo control board to make the camera 
# turning towards the negative direction of the x axis.
# ==========================================================================================
def move_decrease_x():
	global Current_x
	Current_x -= 25
	if Current_x <= MinPluse:
		Current_x = MinPluse
        pwm.setPWM(14, 0, Current_x)
# ==========================================================================================
# Control the servo connected to channel 15 of the servo control board to make the camera 
# turning towards the positive direction of the y axis. 
# ==========================================================================================
def move_increase_y():
	global Current_y
	Current_y += 25
	if Current_y > MaxPluse:
		Current_y = MaxPluse
        pwm.setPWM(15, 0, Current_y)   # CH15 <---> Y axis
# ==========================================================================================
# Control the servo connected to channel 15 of the servo control board to make the camera 
# turning towards the negative direction of the y axis. 
# ==========================================================================================		
def move_decrease_y():
	global Current_y
	Current_y -= 25
	if Current_y <= MinPluse:
		Current_y = MinPluse
        pwm.setPWM(15, 0, Current_y)
# ==========================================================================================		
# Control the servos connected with channel 14 and 15 at the same time to make the camera 
# move forward.
# ==========================================================================================
def home_x_y():
	pwm.setPWM(14, 0, 375)
	pwm.setPWM(15, 0, 375)

def test():
	while True:
		home_x_y()
		time.sleep(0.5)
		for i in range(0, 9):
			move_increase_x()
			move_increase_y()
			time.sleep(0.5)
		for i in range(0, 20):
			move_decrease_x()
			move_decrease_y()
			time.sleep(0.5)

if __name__ == '__main__':
	test()




'''
if __name__ == '__main__':
	while True:
#		move_increase_x()
		move_decrease_x()
#		move_decrease_y()
		move_increase_y()
		time.sleep(0.5)
'''
