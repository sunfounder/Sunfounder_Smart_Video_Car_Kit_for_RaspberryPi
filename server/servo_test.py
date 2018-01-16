#!/usr/bin/env python
import PCA9685 as servo
import time                  # Import necessary modules

MinPulse = 200
MaxPulse = 700

def setup():
    global pwm
    pwm = servo.PWM()

def servo_test():
    for value in range(MinPulse, MaxPulse):
        pwm.write(0, 0, value)
        pwm.write(14, 0, value)
        pwm.write(15, 0, value)
        time.sleep(0.002)

if __name__ == '__main__':
    setup()
    servo_test()
