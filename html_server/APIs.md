# SunFounder Smart Video Car Kit for Raspberry Pi
## Html Server APIs

### Premise
This is a very simple API. No data upload, no JSON format.
Just use "Get" with the host: `http://[Raspberry Pi IP address]:8000/` and the API.   
   
For example, control the car (at 192.168.0.101) to forward:

	<Get>	http://192.168.0.101:8000/motor/forward

You can even control the car with a web browser!
Just type in the host with an API in the web browser, and the car will get the command!   
   
For example, control the car (at 192.168.0.101) to go backward: </br>
At the address bar of a browser,
type in [http://192.168.0.101:8000/motor/backward](http://192.168.0.101:8000/motor/backward).

### APIs with Variables
In an API, `[]` means it's a variable.   
For example, set the motor speed to 60:

	<Get>	http://192.168.0.101:8000/motor/set/speed/60

### APIs

|**Initialization**              |Description|
|:----------------------------------|:--------------------------|
|`runmode`							|Initialize the camera and turning wheels to start the run mode|
|`calibrationmode`					|Initialize the camera and turning wheels to start the calibration mode|   

|**Motor Control**               |Description|
|:----------------------------------|:--------------------------|
|`motor/forward`					|Control the motor to forward.|
|`motor/backward`					|Control the motor to go backward.|
|`motor/stop`						|Control the motor to stop.|
|`motor/set/speed/[speed]`			|Set the motor speed to [speed]; speed ranges (0, 100)|    

|**Camera Control**              |Description|
|:----------------------------------|:--------------------------|
|`camera/increase/y`				|Increase in the Y axis (move the tilt servo up)|
|`camera/decrease/y`				|Decrease in the Y axis (move the tilt servo down)|
|`camera/increase/x`				|Increase in the X axis (move the pan servo right)|
|`camera/decrease/x`				|Increase in the X axis (move the pan servo left)|
|`camera/home`						|Set the camera position back to "Home"|  

|**Steering Control**            |Description|
|:----------------------------------|:--------------------------|
|`turning/[angle]`					|Turn the turning wheels to [angle]; angle ranges (0, 255) (left, right)|  

|**Calibration**				  |Description|
|:----------------------------------|:--------------------------|
|`calibrate/getconfig`				|Get the calibration config from server|
|`calibrate/motor/run`				|Set the motor run forward in calibration mode|
|`calibrate/motor/stop`				|Set the motor stop in calibration mode|
|`calibrate/motor/left/reverse`		|Reverse the left motor|
|`calibrate/motor/right/reverse`	|Reverse the right motor|
|`calibrate/pan/[+/-]/[value]`		|Set the pan servo offset to [+/-] [value]; [+/-] only accept "+" or "-"; value ranges (0, 999)|
|`calibrate/tile/[+/-]/[value]`		|Set the tilt (sorry about the typo "tile") servo offset to [+/-] [value]; [+/-] only accept "+" or "-"; value ranges (0, 999)|
|`calibrate/turning/[+/-]/[value]`	|Set the turning offset to [+/-] [value]; [+/-] only accept "+", or "-"; value ranges (0, 999)|
|`calibrate/confirm`				|Confirm and save the calibration config|


