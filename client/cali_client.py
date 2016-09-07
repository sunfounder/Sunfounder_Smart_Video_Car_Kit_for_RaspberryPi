#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
from socket import *      # Import necessary modules
import os

top = Tk()   # Create a top window
top.title('Raspberry Pi Smart Video Car Calibration')

HOST = '192.168.0.159'    # Server(Raspberry Pi) IP address
PORT = 21567
BUFSIZ = 1024             # buffer size
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)   # Create a socket
tcpCliSock.connect(ADDR)                    # Connect with the server

runbtn = 'Run'

offset = 0
offset_x = 0
offset_y = 0
forward0 = 'True'
forward1 = 'True'

# =============================================================================
# Get original offset configuration.
# =============================================================================

def setup():
	pass

# =============================================================================
# The function is to send the command forward to the server, so as to make the 
# car move forward.
# ============================================================================= 
def run(event):
	global runbtn
	print 'motor ', runbtn
	if runbtn == 'Stop':
		tcpCliSock.send('motor_stop')
		runbtn = 'Run'
	elif runbtn == 'Run':
		tcpCliSock.send('motor_run')
		runbtn = 'Stop'

def confirm(event):
	tcpCliSock.send('confirm')
	
	top.quit()
	tcpCliSock.close()

#--------motor---------------------
def left_reverse(event):
	left_cmd = 'leftreverse'
	tcpCliSock.send(left_cmd)

def right_reverse(event):
	right_cmd = 'rightreverse'
	tcpCliSock.send(right_cmd)
#----------------------------------------

#---------turing---------------
def fineturn_left(event):
	print 'fineturn_left'
	cmd = 'offset-1'
	tcpCliSock.send(cmd)

def fineturn_right(event):
	print 'fineturn_right'
	cmd = 'offset+1'
	tcpCliSock.send(cmd)

def coarseturn_left(event):
	print 'coarseturn_left'
	cmd = 'offset-10'
	tcpCliSock.send(cmd)

def coarseturn_right(event):
	print 'coarseturn_right'
	cmd = 'offset+10'
	tcpCliSock.send(cmd)
#------------------------------

#-----------mount-----------------
#-------------x------------------
def finex_left(event):
	cmd = 'offsetx+1'
	print cmd
	tcpCliSock.send(cmd)

def finex_right(event):
	cmd = 'offsetx-1'
	print cmd
	tcpCliSock.send(cmd)

def coarsex_left(event):
	cmd = 'offsetx+10'
	print cmd
	tcpCliSock.send(cmd)

def coarsex_right(event):
	cmd = 'offsetx-10'
	print cmd
	tcpCliSock.send(cmd)

#---------y-----------------------
def finey_down(event):
	print 'finey_down'
	cmd = 'offsety-1'
	tcpCliSock.send(cmd)

def finey_up(event):
	print 'finey_up'
	cmd = 'offsety+1'
	tcpCliSock.send(cmd)

def coarsey_down(event):
	print 'coarsey_down'
	cmd = 'offsety-10'
	tcpCliSock.send(cmd)

def coarsey_up(event):
	print 'coarsey_up'
	cmd = 'offsety+10'
	tcpCliSock.send(cmd)
#--------------------------------

# =============================================================================
# Exit the GUI program and close the network connection between the client 
# and server.
# =============================================================================
def quit_fun(event):
	top.quit()
	tcpCliSock.send('motor_stop')
	tcpCliSock.close()

# =============================================================================
# Create buttons on motor
# =============================================================================
Btn0 = Button(top, width=5, text='Reverse')
Btn1 = Button(top, width=5, text=runbtn)
Btn2 = Button(top, width=5, text='Reverse')
# =============================================================================
# Create buttons on mount
# =============================================================================
Btn3 = Button(top, width=5, text='<==') # Fine left
Btn4 = Button(top, width=5, text='==>') # Fine right
Btn5 = Button(top, width=5, text='<==') # Coarse left
Btn6 = Button(top, width=5, text='==>')	# Coarse right
Btn7 = Button(top, width=5, text='<==')	# Fine down
Btn8 = Button(top, width=5, text='==>')	# Fine up
Btn9 = Button(top, width=5, text='<==') # Coarse down
Btn10 = Button(top, width=5, text='==>') # Coarse up
# =============================================================================
# Create buttons on turning
# =============================================================================
Btn11 = Button(top, width=5, text='<==') # fine left
Btn12 = Button(top, width=5, text='==>') # fine right
Btn13 = Button(top, width=5, text='<==') # Coarse left
Btn14 = Button(top, width=5, text='==>') # Coarse right
# =============================================================================
# Create buttons on top
# =============================================================================
Btn15 = Button(top, width=5, text='Cancel')	# cancle
Btn16 = Button(top, width=5, text='Confirm') # confirm

# =============================================================================
# Buttons layout
# =============================================================================
Btn0.grid(row=2,column=0)
Btn1.grid(row=2,column=1)
Btn2.grid(row=2,column=2)

Btn3.grid(row=2,column=4)
Btn4.grid(row=2,column=6)
Btn5.grid(row=3,column=4)
Btn6.grid(row=3,column=6)
Btn7.grid(row=5,column=4)
Btn8.grid(row=5,column=6)
Btn9.grid(row=6,column=4)
Btn10.grid(row=6,column=6)

Btn11.grid(row=5,column=0)
Btn12.grid(row=5,column=2)
Btn13.grid(row=6,column=0)
Btn14.grid(row=6,column=2)

Btn15.grid(row=8,column=5)
Btn16.grid(row=8,column=6)

# =============================================================================
# Bind the buttons with the corresponding callback function.
# =============================================================================
Btn0.bind('<ButtonRelease-1>', left_reverse)
Btn1.bind('<ButtonRelease-1>', run)
Btn2.bind('<ButtonRelease-1>', right_reverse)

Btn3.bind('<ButtonRelease-1>', finex_left)
Btn4.bind('<ButtonRelease-1>', finex_right)
Btn5.bind('<ButtonRelease-1>', coarsex_left)
Btn6.bind('<ButtonRelease-1>', coarsex_right)
Btn7.bind('<ButtonRelease-1>', finey_down)
Btn8.bind('<ButtonRelease-1>', finey_up)
Btn9.bind('<ButtonRelease-1>', coarsey_down)
Btn10.bind('<ButtonRelease-1>', coarsey_up)

Btn11.bind('<ButtonRelease-1>', fineturn_left)
Btn12.bind('<ButtonRelease-1>', fineturn_right)
Btn13.bind('<ButtonRelease-1>', coarseturn_left)
Btn14.bind('<ButtonRelease-1>', coarseturn_right)

Btn15.bind('<ButtonRelease-1>', quit_fun)
Btn16.bind('<ButtonRelease-1>', confirm)

# =============================================================================
# Bind buttons on the keyboard with the corresponding callback function to 
# control the car remotely with the keyboard.
# =============================================================================

spd = 50

hori = '========='
label0 = Label(top, text='||', fg='red')
label1 = Label(top, text='||', fg='red')
label2 = Label(top, text='||', fg='red')
label3 = Label(top, text='||', fg='red')
label4 = Label(top, text='||', fg='red')
label5 = Label(top, text='||', fg='red')
label6 = Label(top, text='||', fg='red')

label7 = Label(top, text=hori, fg='red')
label8 = Label(top, text=hori, fg='red')
label9 = Label(top, text=hori, fg='red')
label10 = Label(top, text=hori, fg='red')
label11 = Label(top, text=hori, fg='red')
label12 = Label(top, text=hori, fg='red')
label13 = Label(top, text='||', fg='red')
label14 = Label(top, text=hori, fg='red')
label15 = Label(top, text=hori, fg='red')
label16 = Label(top, text=hori, fg='red')

label17 = Label(top, text='Motor', fg='red')
label18 = Label(top, text='Left', fg='red')
#label19 = Label(top, text='Forward', fg='red')
label20 = Label(top, text='Right', fg='red')
label21 = Label(top, text='Mount', fg='red')
label22 = Label(top, text='Pan:', fg='red')
#label23 = Label(top, text='Front', fg='red')
label24 = Label(top, text='=== Fine ===', fg='red')
label25 = Label(top, text='== Coarse ==', fg='red')
label26 = Label(top, text='Tilt:', fg='red')
#label27 = Label(top, text='Up', fg='red')
label28 = Label(top, text='=== Fine ===', fg='red')
label29 = Label(top, text='== Coarse ==', fg='red')
label30 = Label(top, text='Turning', fg='red')
label31 = Label(top, text='=== Fine ===', fg='red')
label32 = Label(top, text='== Coarse ==', fg='red')

label0.grid(row=0,column=3)
label1.grid(row=1,column=3)
label2.grid(row=2,column=3)
label3.grid(row=3,column=3)
label4.grid(row=4,column=3)
label5.grid(row=5,column=3)
label6.grid(row=6,column=3)
label7.grid(row=3,column=0)
label8.grid(row=3,column=1)
label9.grid(row=3,column=2)
label10.grid(row=7,column=0)
label11.grid(row=7,column=1)
label12.grid(row=7,column=2)
label13.grid(row=7,column=3)
label14.grid(row=7,column=4)
label15.grid(row=7,column=5)
label16.grid(row=7,column=6)
label17.grid(row=0,column=1)
label18.grid(row=1,column=0)
#label19.grid(row=1,column=1)
label20.grid(row=1,column=2)
label21.grid(row=0,column=5)
label22.grid(row=1,column=4)
#label23.grid(row=1,column=5)
label24.grid(row=2,column=5)
label25.grid(row=3,column=5)
label26.grid(row=4,column=4)
#label27.grid(row=4,column=5)
label28.grid(row=5,column=5)
label29.grid(row=6,column=5)
label30.grid(row=4,column=1)
label31.grid(row=5,column=1)
label32.grid(row=6,column=1)

def main():
	top.mainloop()

if __name__ == '__main__':
	setup()
	main()

