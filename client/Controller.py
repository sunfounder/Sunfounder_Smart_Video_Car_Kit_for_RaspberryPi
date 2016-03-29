#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
from socket import *      # Import necessary modules
from SunFounder_PiPlus import *

ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']

HOST = '192.168.0.139'    # Server(Raspberry Pi) IP address
PORT = 21567
BUFSIZ = 1024             # buffer size
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)   # Create a socket
tcpCliSock.connect(ADDR) 

# =============================================================================
# The function is to send the command forward to the server, so as to make the 
# car move forward.
# ============================================================================= 
def forward_fun(spd = 50):
	print 'forward:', spd
	cmd = 'forward=' + str(spd)
	tcpCliSock.send(cmd)

def backward_fun(spd = 50):
	print 'backward:', spd
	cmd = 'backward=' + str(spd)
	tcpCliSock.send(cmd)

def turn_fun(angle = 128):
	print 'turing angle =', angle
	cmd = 'turn=' + str(angle)
	print 'cmd=', cmd
	tcpCliSock.send(cmd)

def stop_fun():
	print 'stop'
	tcpCliSock.send('stop')

def home_fun():
	print 'home'
	tcpCliSock.send('home')

def dis_fun():
	print 'Measuring distance...'
	tcpCliSock.send('distance')
	data = tcpCliSock.recv(BUFSIZ)
	print data

def x_increase():
	print 'x+'
	tcpCliSock.send('x+')

def x_decrease():
	print 'x-'
	tcpCliSock.send('x-')

def y_increase():
	print 'y+'
	tcpCliSock.send('y+')

def y_decrease():
	print 'y-'
	tcpCliSock.send('y-')

def xy_home():
	print 'xy_home'
	tcpCliSock.send('xy_home')

xStick = DB1
yStick = DB2
homeBtn = DB3

def setup():
	global Joystick, Btn
	Joystick = Joystick()
	Btn = Buttons(port='B')

def main():
	
	while True:
		x, y, btn = Joystick.read()
		#print x, y, btn
		
		turn_fun(Map(255-x, 0, 255, 50, 205))
		if y > 133:
			forward_fun(Map(y, 133, 255, 0, 60))
		elif y >= 123 and y <= 133:
			stop_fun()
		elif y < 123:
			backward_fun(Map(123-y, 0, 123, 0, 60))
		time.sleep(0.3)
		up = GPIO.input(Btn.UP)
		down = GPIO.input(Btn.DOWN)
		left = GPIO.input(Btn.LEFT)
		right = GPIO.input(Btn.RIGHT)
		if up == 0 and down == 0:
			xy_home()
		else:
			if up == 0 and down == 1:
				y_increase()
			elif down == 0 and up == 1:
				y_decrease()
			if left == 0 and right == 1:
				x_decrease()
			elif right == 0 and left == 1:
				x_increase()
		time.sleep(0.3)
			
		
def destroy():
	Joystick.destroy()
	Buttons.destroy()
	tcpCliSock.send('stop')
	tcpCliSock.close()
	GPIO.cleanup()
	
if __name__ == "__main__":
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()
