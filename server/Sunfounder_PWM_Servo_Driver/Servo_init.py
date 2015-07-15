#!/usr/bin/python
from Sunfounder_PWM_Servo_Driver import PWM
import time

def setServoPulse(channel, pulse):
	pulseLength = 1000000                   # 1,000,000 us per second
	pulseLength /= 60                       # 60 Hz
	print "%d us per period" % pulseLength
	pulseLength /= 4096                     # 12 bits of resolution
	print "%d us per bit" % pulseLength
	pulse *= 1000
	pulse /= pulseLength
	pwm.setPWM(channel, 0, pulse)

def init():
	#servoMin = 150  # Min pulse length out of 4096
	#servoMax = 600  # Max pulse length out of 4096
	pwm = PWM(0x40)
	#pwm = PWM(0x40, debug=True)
	pwm.setPWMFreq(60)                      # Set frequency to 60 Hz
	#pwm.setPWM(0, 0, 450)   #medium
	return pwm


if __name__ == '__main__':
	pwm_smp = init()
	while True:
		pwm_smp.setPWM(0, 0, 375)
		time.sleep(1)
		pwm_smp.setPWM(0, 0, 450)
		time.sleep(1)
		pwm_smp.setPWM(0, 0, 525)
		time.sleep(1)
		pwm_smp.setPWM(0, 0, 450)
		time.sleep(1)

