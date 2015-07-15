#!/usr/bin/env python
import RPi.GPIO as GPIO
import video_dir
import car_dir
import motor
from socket import *
from time import ctime          # Import necessary modules   

HOST = ''           # The variable of HOST is null, so the function bind( ) can be bound to all valid addresses.
PORT = 21567
BUFSIZ = 1024       # Size of the buffer
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)    # Create a socket.
tcpSerSock.bind(ADDR)    # Bind the IP address and port number of the server. 
tcpSerSock.listen(5)     # The parameter of listen() defines the number of connections permitted at one time. Once the 
                         # connections are full, others will be rejected. 

for line in open('config'):
	if line[0:8] == 'offset_x'
		offset_x = int(line[11:-2])
	if line[0:8] == 'offset_y':
		offset_y = int(line[11:-2])
	if line[0:10] == 'dir_offset':
		offset = int(line[13:-2])
	if line[0:8] == "forward0":
		forward0 = line[11:-2]
	if line[0:8] == "forward1":
		forward1 = line[11:-2]
if forward0 == 'True':
	backward0 = 'False'
elif forward0 == 'False':
	backward0 = 'True'
if forward1 == 'True':
	backward1 = 'False'
elif forward1 == 'False':
	backward1 = 'True'

video_dir.setup()
car_dir.setup()
motor.setup()     # Initialize the Raspberry Pi GPIO connected to the DC motor. 
video_dir.home_x_y()
car_dir.home()

while True:
	print 'Waiting for connection...'
	# Waiting for connection. Once receiving a connection, the function accept() returns a separate 
	# client socket for the subsequent communication. By default, the function accept() is a blocking 
	# one, which means it is suspended before the connection comes.
	tcpCliSock, addr = tcpSerSock.accept() 
	print '...connected from :', addr     # Print the IP address of the client connected with the server.

	while True:
		data = tcpCliSock.recv(BUFSIZ)    # Receive data sent from the client. 
		# Analyze the command received and control the car accordingly.
		if not data:
			break
		if data == 'motor_test':
			print 'motor moving forward'
			motor.motor0(forward0)
		elif data == 'left_motor_reverse':
			print 'left motor reversed'
			
		elif data == ctrl_cmd[2]:
			print 'recv left cmd'
			car_dir.turn_left()
		elif data == ctrl_cmd[3]:
			print 'recv right cmd'
			car_dir.turn_right()
		elif data == ctrl_cmd[6]:
			print 'recv home cmd'
			car_dir.home()
		elif data == ctrl_cmd[4]:
			print 'recv stop cmd'
			motor.ctrl(0)
		elif data == ctrl_cmd[5]:
			print 'read cpu temp...'
			temp = cpu_temp.read()
			tcpCliSock.send('[%s] %0.2f' % (ctime(), temp))
		elif data == ctrl_cmd[8]:
			print 'recv x+ cmd'
			video_dir.move_increase_x()
		elif data == ctrl_cmd[9]:
			print 'recv x- cmd'
			video_dir.move_decrease_x()
		elif data == ctrl_cmd[10]:
			print 'recv y+ cmd'
			video_dir.move_increase_y()
		elif data == ctrl_cmd[11]:
			print 'recv y- cmd'
			video_dir.move_decrease_y()
		elif data == ctrl_cmd[12]:
			print 'home_x_y'
			video_dir.home_x_y()
		elif data[0:5] == 'speed':     # Change the speed
			print data
			numLen = len(data) - len('speed')
			if numLen == 1 or numLen == 2 or numLen == 3:
				tmp = data[-numLen:]
				print 'tmp(str) = %s' % tmp
				spd = int(tmp)
				print 'spd(int) = %d' % spd
				if spd < 24:
					spd = 24
				motor.setSpeed(spd)
		else:
			print 'cmd error !'
tcpSerSock.close()

