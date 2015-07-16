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

video_dir.setup()
car_dir.setup()
motor.setup()     # Initialize the Raspberry Pi GPIO connected to the DC motor. 
video_dir.home_x_y()
car_dir.home()

def REVERSE(x):
	if x == 'True':
		return = 'False'
	elif x == 'False':
		return = 'True'

def loop():
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
			#--------Motor calibration----------
			if data == 'motor_run':
				print 'motor moving forward'
				motor.speed(50)
				motor.motor0(forward0)
				motor.motor1(forward1)
			elif data[0:9] == 'leftmotor':
				forward0 = data[9:]
				motor.motor0(forward0)
			elif data[0:10] == 'rightmotor':
				forward1 = data[10:]
				motor.motor1(forward1)
			elif data == 'motor_stop':
				print 'motor stop'
				motor.stop()
			#---------------------------------

			#-------Turing calibration------
			elif data[0:6] == 'offset':
				offset = int(date[6:])
				car_dir.calbrate(offset)
			#--------------------------------

			#----------Mount calibration---------
			elif data[0:7] = 'offsetx':
				offset_x = int(date[7:])
				print 'Mount offset x', offsetx
				video_dir.calibration(offset_x)
			elif data[0:7] = 'offsety':
				offset_x = int(date[7:])
				print 'Mount offset y', offset_y
				video_dir.calibration(offset_x)
			#----------------------------------------

			else:
				print 'cmd error !'

if __name__ == "__main__":
	try:
		loop()
	except KeyboardInterrupt:
		tcpSerSock.close()

