### Html server
----------
This app is builds base on Django.
This server runs on Raspberry Pi, and could be control by Android app.

####Setup:
at `Sunfounder_Smart_Video_Car_Kit_for_RaspberryPi/http_server/` run:

	sudo python manage.py runserver 0.0.0.0:8000

open the app on your phone, and type in your raspberry pi's ip address, and click FORWARD(the right arrow) then you might see the pictures of your Video Cars camera.

####Calibration:
Begin calibration by click on the dot in a circle. Notice: calibration adjust step are small. Click more times or type in values for great effort.

####Control:
 - Control the car direction by rotate your phone, like a steering wheel.
 - Control the car forward/backward by the up/down arrow on the left.
 - Control the camera pan/tile by the up/down/left/right arrow on the right. and set the camera back to default position by the middle dot.
 - Change the motor speed by the bar under the camera view
