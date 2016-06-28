# SunFounder Smart Video Car Kit for Raspberry Pi
## Html Server APIs

### 111
This is a very simple API. No data upload, No Json format.
Just use "Get" with host:'http://<raspberry pi ip address>:8000/' and the API.
like, to control the car (at 192.168.0.101) forward:

	<Get>	http://192.168.0.101:8000/motor/forward

You can even control the car with a browser!
Just type in the host with a command API in the Web browser, the car will get the command!
like, to control the car (at 192.168.0.101) backward:
visit "http://192.168.0.101:8000/motor/backward" on your browser.

### Special APIs detials:
In an API, `[]` means it's a veriable.
for example:
To Set the motor speed to 60:
<Get>	http://192.168.0.101:8000/motor/set/speed/60

### APIs:

|**Motor control**|                 |
|:----------------------------------|:--------------------------|
|`motor/forward`					|Control the motor forward.|
|`motor/backward`					|Control the motor backward.|
|`motor/stop`						|Control the motor stop.|
|`motor/set/speed/[speed]`			|Set motor speed to [speed], speed ranges (0, 100)|
|**Camera control**|
|`camera/increase/y`				|Increase Y axis (move tilt up)|
|`camera/decrease/y`				|Decrease Y axis (move tilt down)|
|`camera/increase/x`				|Increase X axis (move pan right)|
|`camera/decrease/x`				|Increase X axis (move pan right)|
|`camera/home`						|Set camera position back to "Home"|
|**Steering control**|
|`turning/[angle]`					|Turn the turning wheels to [angle], angle ranges (0, 255) (left, right)|
|**Calibrations**|
|`calibrate/getconfig`				|Get calibration config from server|
|`calibrate/motor/run`				|Set the motor run forward in calibration mode|
|`calibrate/motor/stop`				|Set motor stop in calibration mode|
|`calibrate/motor/left/reverse`		|Reverse left motor|
|`calibrate/motor/right/reverse`	|Reverse right motor|
|`calibrate/pan/[+/-]/[value]`		|Set pan offset to [+/-] [value], [+/-] only accept "+", or "-", value ranges (0, 999)|
|`calibrate/tile/[+/-]/[value]`		|Set tilt (that "tile" is an typo) offset to [+/-] [value], [+/-] only accept "+", or "-", value ranges (0, 999)|
|`calibrate/turning/[+/-]/[value]`	|Set turning offset to [+/-] [value], [+/-] only accept "+", or "-", value ranges (0, 999)|
|`calibrate/confirm`				|Confirm and save the calibration config|
|**Others**							|
|`runmode`							|Set camera and turning wheels to run mode|
|`calibrationmode`					|Set camera and turning wheels to calibration mode|


