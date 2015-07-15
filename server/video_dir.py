#!/usr/bin/env python
import Sunfounder_PWM_Servo_Driver.Servo_init as servo
import time                  # Import necessary modules

x_offset = 0
y_offset = 0
MinPulse = 200
MaxPulse = 700 

home_x = (MaxPulse - MinPulse) / 2 + x_offset
home_y = (MaxPulse - MinPulse) / 2 + y_offset
Current_x = 0
Current_y = 0

pwm = servo.init()           # Initialize the servo controller. 

# ==========================================================================================
# Control the servo connected to channel 14 of the servo control board to make the camera 
# turning towards the positive direction of the x axis.
# ==========================================================================================
def move_decrease_x():
	global Current_x
	Current_x += 25
	if Current_x > MaxPulse + x_offset:
		Current_x = MaxPulse + x_offset
        pwm.setPWM(14, 0, Current_x)   # CH14 <---> X axis
# ==========================================================================================
# Control the servo connected to channel 14 of the servo control board to make the camera 
# turning towards the negative direction of the x axis.
# ==========================================================================================
def move_increase_x():
	global Current_x
	Current_x -= 25
	if Current_x <= MinPulse + x_offset:
		Current_x = MinPulse + x_offset
        pwm.setPWM(14, 0, Current_x)
# ==========================================================================================
# Control the servo connected to channel 15 of the servo control board to make the camera 
# turning towards the positive direction of the y axis. 
# ==========================================================================================
def move_increase_y():
	global Current_y
	Current_y += 25
	if Current_y > MaxPulse + y_offset:
		Current_y = MaxPluse + y_offset
        pwm.setPWM(15, 0, Current_y)   # CH15 <---> Y axis
# ==========================================================================================
# Control the servo connected to channel 15 of the servo control board to make the camera 
# turning towards the negative direction of the y axis. 
# ==========================================================================================		
def move_decrease_y():
	global Current_y
	Current_y -= 25
	if Current_y <= MinPluse + y_offset:
		Current_y = MinPluse + y_offset
        pwm.setPWM(15, 0, Current_y)
# ==========================================================================================		
# Control the servos connected with channel 14 and 15 at the same time to make the camera 
# move forward.
# ==========================================================================================
def home_x_y():
	global Current_y
	global Current_x
	Current_y = home_x
	Current_x = home_y
	pwm.setPWM(14, 0, Current_x)
	pwm.setPWM(15, 0, Current_y)

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
	home_x_y()




'''
if __name__ == '__main__':
	while True:
#		move_increase_x()
		move_decrease_x()
#		move_decrease_y()
		move_increase_y()
		time.sleep(0.5)
'''
