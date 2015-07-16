#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
from socket import *      # Import necessary modules
import os

top = Tk()   # Create a top window
top.title('Raspberry Pi Smart Video Car Calibration')

HOST = '192.168.0.134'    # Server(Raspberry Pi) IP address
PORT = 21567
BUFSIZ = 1024             # buffer size
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)   # Create a socket
tcpCliSock.connect(ADDR)                    # Connect with the server

motorCal = Tk()
motorCal.title('Motor Calibration')

directionCal = Tk()
directionCal.title('Direction Calibration')

mountCal = Tk()
mountCal.title('Mount Calibration')

# =============================================================================
# Get original offset configuration.
# =============================================================================

def setup():
	global offset_x, offset_y, offset, forward0, forward1
	offset = 0
	offset_x = 0
	offset_y = 0
	forward0 = 'True'
	forward1 = 'True'
	os.system('scp pi@%s:/home/Sunfounder_Smart_Video_Car_Kit_for_RaspberryPi/server/config ./' % HOST)
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

# =============================================================================
# The function is to send the command forward to the server, so as to make the 
# car move forward.
# ============================================================================= 
def motor_test(event):
	print 'motor_test'
	tcpCliSock.send('motor_run')
	motorCal.mainloop()

def main_menu(event):
	print 'main menu'
	tcpCliSock.send('motor_stop')
	top.mainloop()

def direction_test(event):
	print 'direction_test'
	offset_cmd = 'offset%d' % offset
	tcpCliSock.send(offset_cmd)
	directionCal.mainloop()

def mount_test(event):
	print 'mount test'
	offsetx_cmd = 'offsetx%d' % offset_x
	offsety_cmd = 'offsety%d' % offset_y
	tcpCliSock.send(offsetx_cmd)
	tcpCliSock.send(offsety_cmd)
	mountCal.mainloop()

def setok(event):
	print 'rewrite conig file'
	config = 'offset_x = %s\noffset_y = %s\noffset = %s\nforward0 = %s\nforward1 = %s\n' % (offset_x, offset_y, offset, forward0, forward1)
	fd = open('config', 'w')
	fd.write(config)
	fd.close()

def confirm(event):
	print 'confirm and send to Raspberry Pi'
	os.system('sudo scp ./config pi@%s:/home/Sunfounder_Smart_Video_Car_Kit_for_RaspberryPi/server/' % HOST)

#--------motor---------------------
def left_reverse(event):
	print 'left_reverse'
	if forward0 == 'True':
		forward0 = 'False'
	elif forward0 == 'False'
		forward0 = 'True'
	left_cmd = 'leftmotor%s' % forward0
	tcpCliSock.send(left_cmd)

def right_reverse(event):
	print 'right_reverse'
	if forward1 == 'True':
		forward1 = 'False'
	elif forward1 == 'False'
		forward1 = 'True'
	right_cmd = 'rightmotor%s' % forward1
	tcpCliSock.send(right_cmd)
#----------------------------------------

#---------turing---------------
def fineturn_left(event):
	print 'fineturn_left'
	offset -= 1
	cmd = 'offset%s' % offset
	tcpCliSock.send(cmd)

def fineturn_right(event):
	print 'fineturn_right'
	offset += 1
	cmd = 'offset%s' % offset
	tcpCliSock.send(cmd)

def coarseturn_left(event):
	print 'coarseturn_left'
	offset -= 10
	cmd = 'offset%s' % offset
	tcpCliSock.send(cmd)

def coarseturn_right(event):
	print 'coarseturn_right'
	offset += 10
	cmd = 'offset%s' % offset
	tcpCliSock.send(cmd)
#------------------------------

#-----------mount-----------------
#-------------x------------------
def finex_left(event):
	print 'finex_left'
	offset_x -= 1
	cmd = 'offsetx%s' % offset_x
	tcpCliSock.send(cmd)

def finex_right(event):
	print 'finex_right'
	offset_x += 1
	cmd = 'offsetx%s' % offset_x
	tcpCliSock.send(cmd)

def coarsex_left(event):
	print 'coarsex_left'
	offset_x -= 10
	cmd = 'offsetx%s' % offset_x
	tcpCliSock.send(cmd)

def coarsex_right(event):
	print 'coarsex_right'
	offset_x += 10
	cmd = 'offsetx%s' % offset_x
	tcpCliSock.send(cmd)

#---------y-----------------------
def finey_down(event):
	print 'finey_down'
	offset_y -= 1
	cmd = 'offsety%s' % offset_y
	tcpCliSock.send(cmd)

def finey_up(event):
	print 'finey_up'
	offset_y += 1
	cmd = 'offsety%s' % offset_y
	tcpCliSock.send(cmd)

def coarsey_down(event):
	print 'coarsey_down'
	offset_y -= 10
	cmd = 'offsety%s' % offset_y
	tcpCliSock.send(cmd)

def coarsey_up(event):
	print 'coarsey_up'
	offset_y += 10
	cmd = 'offsety%s' % offset_y
	tcpCliSock.send(cmd)
#--------------------------------

# =============================================================================
# Exit the GUI program and close the network connection between the client 
# and server.
# =============================================================================
def quit_fun(event):
	top.quit()
	tcpCliSock.send('stop')
	tcpCliSock.close()

# =============================================================================
# Create buttons on top
# =============================================================================
Btn0 = Button(top, width=5, text='Motor')
Btn1 = Button(top, width=5, text='Turing')
Btn2 = Button(top, width=5, text='Mount')
Btn3 = Button(top, width=5, text='Comfirm')
Btn4 = Button(top, width=5, text='Quit')
# =============================================================================
# Create buttons on mount calibration
# =============================================================================
Btn5 = Button(mountCal, width=5, text='<==')	# Fine left
Btn6 = Button(mountCal, width=5, text='==>')	# Fine right
Btn7 = Button(mountCal, width=5, text='<==')	# Coarse left
Btn8 = Button(mountCal, width=5, text='==>')	# Coarse right
Btn9 = Button(mountCal, width=5, text='<==')	# Fine down
Btn10 = Button(mountCal, width=5, text='==>')	# Fine up
Btn11 = Button(mountCal, width=5, text='<==')	# Coarse down
Btn12 = Button(mountCal, width=5, text='==>')	# Coarse up
Btn13 = Button(mountCal, width=5, text='Back')
Btn14 = Button(mountCal, width=5, text='Set')
# =============================================================================
# Create buttons on direction calibration
# =============================================================================
Btn15 = Button(directionCal, width=5, text='<==')	# Fine left
Btn16 = Button(directionCal, width=5, text='==>')	# Fine right
Btn17 = Button(directionCal, width=5, text='<==')	# Coarse left
Btn18 = Button(directionCal, width=5, text='==>')	# Coarse right
Btn19 = Button(directionCal, width=5, text='Back')
Btn20 = Button(directionCal, width=5, text='Set')
# =============================================================================
# Create buttons on motor calibration
# =============================================================================
Btn21 = Button(motorCal, width=5, text='Left Reverse')
Btn22 = Button(motorCal, width=5, text='Right Reverse')
Btn23 = Button(motorCal, width=5, text='Back')
Btn24 = Button(motorCal, width=5, text='Set')
# =============================================================================
# Buttons layout
# =============================================================================

Btn0.grid(row=1,column=1)
Btn1.grid(row=2,column=1)
Btn2.grid(row=3,column=1)
Btn3.grid(row=4,column=0)
Btn4.grid(row=4,column=2)
Btn5.grid(row=1,column=0)
Btn6.grid(row=1,column=2)
Btn7.grid(row=2,column=0)
Btn8.grid(row=2,column=2)
Btn9.grid(row=3,column=0)
Btn10.grid(row=3,column=2)
Btn11.grid(row=4,column=0)
Btn12.grid(row=4,column=2)
Btn13.grid(row=6,column=0)
Btn14.grid(row=6,column=2)
Btn15.grid(row=1,column=0)
Btn16.grid(row=1,column=2)
Btn17.grid(row=2,column=0)
Btn18.grid(row=2,column=2)
Btn19.grid(row=4,column=0)
Btn20.grid(row=4,column=2)
Btn21.grid(row=1,column=0)
Btn22.grid(row=1,column=2)
Btn23.grid(row=3,column=0)
Btn24.grid(row=3,column=2)

# =============================================================================
# Bind the buttons with the corresponding callback function.
# =============================================================================
Btn0.bind('<ButtonRelease-1>', motor_test)
Btn1.bind('<ButtonRelease-1>', direction_test)
Btn2.bind('<ButtonRelease-1>', mount_test)
Btn3.bind('<ButtonRelease-1>', confirm)
Btn4.bind('<ButtonRelease-1>', quit_fun)
Btn5.bind('<ButtonRelease-1>', finex_left)
Btn6.bind('<ButtonRelease-1>', finex_right)
Btn7.bind('<ButtonRelease-1>', coarsex_left)
Btn8.bind('<ButtonRelease-1>', coarsex_right)
Btn9.bind('<ButtonRelease-1>', finey_down)
Btn10.bind('<ButtonRelease-1>', finey_up)
Btn11.bind('<ButtonRelease-1>', coarsey_down)
Btn12.bind('<ButtonRelease-1>', coarsey_up)
Btn13.bind('<ButtonRelease-1>', main_menu)
Btn14.bind('<ButtonRelease-1>', setok)
Btn15.bind('<ButtonRelease-1>', fineturn_left)
Btn16.bind('<ButtonRelease-1>', fineturn_right)
Btn17.bind('<ButtonRelease-1>', coarseturn_left)
Btn18.bind('<ButtonRelease-1>', coarseturn_right)
Btn19.bind('<ButtonRelease-1>', main_menu)
Btn20.bind('<ButtonRelease-1>', setok)
Btn21.bind('<ButtonRelease-1>', left_reverse)
Btn22.bind('<ButtonRelease-1>', right_reverse)
Btn23.bind('<ButtonRelease-1>', main_menu)
Btn24.bind('<ButtonRelease-1>', setok)


# =============================================================================
# Bind buttons on the keyboard with the corresponding callback function to 
# control the car remotely with the keyboard.
# =============================================================================

spd = 50

xfine = Label(motorCal, text='Fine X', fg='red')
xfine.grid(row=1, column=1)
xcoarse = Label(motorCal, text='Coarse X', fg='red')
xcoarse.grid(row=2, column=1)
yfine = Label(motorCal, text='Fine Y', fg='red')
yfine.grid(row=3, column=1)
ycoarse = Label(motorCal, text='Coarse Y', fg='red')
ycoarse.grid(row=4, column=1)
tfine = Label(motorCal, text='Fine turing', fg='red')
tfine.grid(row=1, column=1)
tcoarse = Label(motorCal, text='Coarse turning', fg='red')
tcoarse.grid(row=2, column=1)

def main():
	top.mainloop()

if __name__ == '__main__':
	main()

