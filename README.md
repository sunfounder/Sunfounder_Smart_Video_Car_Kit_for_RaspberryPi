## Sunfounder Smart Video Car Kit for Raspberry Pi

### About this kit:
The SunFounder Smart Video Car Kit for Raspberry Pi is composed of Raspberry Pi, DC-DC Step-down Voltage Module, USB camera, DC motor driver, and PCA9685-based Servo Controller. From the perspective of software, the smart car is of client/server (C/S) structure. The TCP server program is run on Raspberry Pi for direct control of the car. And the video data are acquired and delivered via the open source software MGPJ-streamer in a real-time manner. The TCP client program is run on PC to send the control command. Both the client and server programs are developed in Python language. The smart car is developed based on the open-source hardware Raspberry Pi and integrates the knowledge of mechanics, electronics, and computer, thus having profound educational significance. 

#### Notice:
Before you run the client routine, you must first run the server routine.

### Update：

2016/05/16:
 - add i2cHelper.py
 	- For those who gets IOERROR: `[Errno 2] No Such File Or Directory`, Try run the i2cHelper.py:
 	
		sudo python i2cHelper.py

2016/05/09:
 - add android app control. (Details in html_server/README.md)
 - add windows calibration support
 	- download and install python 2.7 first at: https://www.python.org/downloads/release/python-2711/
 	- run client/cali_client_win.py on windows.
 	- client_app.py also can run on windows.

2016/03/29:
 - fixed speed control
 - fixed turning angle
 - removed useless button

2016/03/22:
 - fixed Raspberry Pi 3 compatibility.

2015/xx/xx:
 - improve i2c number getting, 
solved *IOError: "[Errno 2] No such file or directory"* problem for some Pi.

----------------------------------------------
### About SunFounder:
SunFounder is a technology company focused on Raspberry Pi and Arduino open source community development. Committed to the promotion of open source culture, we strives to bring the fun of electronics making to people all around the world and enable everyone to be a maker. Our products include learning kits, development boards, robots, sensor modules and development tools. In addition to high quality products, SunFounder also offers video tutorials to help you make your own project. If you have interest in open source or making something cool, welcome to join us!

----------------------------------------------
### Contact us:
website:
	www.sunfounder.com

E-mail:
	support@sunfounder.com
