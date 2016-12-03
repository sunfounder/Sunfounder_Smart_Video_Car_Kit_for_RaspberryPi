from django.http import HttpResponse
from django.shortcuts import render
import video_dir
import car_dir
import motor
import os


# Run camera
LD_LIBRARY_PATH = "/home/pi/Sunfounder_Smart_Video_Car_Kit_for_RaspberryPi/mjpg-streamer/mjpg-streamer/"

MJPG_STREAMER_PATH = "mjpg_streamer"
MJPG_STREAMER_PATH = LD_LIBRARY_PATH + MJPG_STREAMER_PATH
INPUT_PATH = "input_uvc.so"
INPUT_PATH = LD_LIBRARY_PATH + INPUT_PATH
OUTPUT_PATH = "output_http.so -w ./www"
OUTPUT_PATH = LD_LIBRARY_PATH + OUTPUT_PATH

command = MJPG_STREAMER_PATH + ' -i \"' + INPUT_PATH + '" -o "' + OUTPUT_PATH + '" &'
os.system(command)

video_dir.setup()
car_dir.setup()
motor.setup()     # Initialize the Raspberry Pi GPIO connected to the DC motor. 
video_dir.home_x_y()
car_dir.home()

# Read config file
FILE_CONFIG = "/home/pi/Sunfounder_Smart_Video_Car_Kit_for_RaspberryPi/server/config"
offset = "0"
offset_x = "0"
offset_y = "0"
forward0 = "True"
forward1 = "True"

for line in open(FILE_CONFIG):
	if line[0:8] == 'offset_x':
		offset_x = int(line[11:-1])
	if line[0:8] == 'offset_y':
		offset_y = int(line[11:-1])
	if line[0:8] == 'offset =':
		offset = int(line[9:-1])
	if line[0:8] == "forward0":
		forward0 = line[11:-1]
	if line[0:8] == "forward1":
		forward1 = line[11:-1]

def motor_forward(request):
	motor.forward()
	return HttpResponse("Motor forward")

def motor_backward(request):
	motor.backward()
	return HttpResponse("Motor backward")

def motor_stop(request):
	motor.ctrl(0)
	return HttpResponse("Motor stop")

def motor_set_speed(request, speed):
	speed = int(speed)
	if speed < 24:
		speed = 24
	if speed > 100:
		speed = 100
	motor.setSpeed(speed)
	text = "Speed set to", speed
	return HttpResponse(text)

def turning(request, angle):
	angle = int(angle)
	car_dir.turn(angle)
	text = "Turing angle", angle
	return HttpResponse(text)

def camera_increase_y(request):
	video_dir.move_increase_y()
	return HttpResponse("Camera y+")

def camera_decrease_y(request):
	video_dir.move_decrease_y()
	return HttpResponse("Camera y-")

def camera_increase_x(request):
	video_dir.move_increase_x()
	return HttpResponse("Camera x+")

def camera_decrease_x(request):
	video_dir.move_decrease_x()
	return HttpResponse("Camera x-")

def camera_home(request):
	video_dir.home_x_y()
	return HttpResponse("Camera back to defaultrequest")

def run_mode(request):
	video_dir.setup()
	car_dir.setup()
	motor.setup()
	video_dir.home_x_y()
	car_dir.home()
	motor.setSpeed(50)
	return HttpResponse("Run mode start")

def calibration_mode(request):
	video_dir.calibrate(offset_x, offset_y)
	car_dir.calibrate(offset)
	return HttpResponse("Calibration mode start")

def calibrate_get_config(request):
	text = "%s\n%s\n%s" % (offset, offset_x, offset_y)
	return HttpResponse(text)

def calibrate_turning(request, direction, in_offset):
	global offset
	offset = int(in_offset)
	if direction == '-':
		offset = 0 - offset
	car_dir.calibrate(offset)
	text = "offset:", offset
	return HttpResponse(text)

def calibrate_motor_run(request):
	motor.setSpeed(50)
	motor.motor0(forward0)
	motor.motor1(forward1)
	return HttpResponse('Motors Runing')

def calibrate_motor_stop(request):
	motor.stop()
	return HttpResponse('Motors stop')

def calibrate_motor_left_reverse(request):
	global forward0
	if forward0 == "True":
		forward0 = "False"
	else:
		forward0 = "True"
	motor.motor0(forward0)
	text = 'left motor reverse to ', forward0
	return HttpResponse(text)

def calibrate_motor_right_reverse(request):
	global forward1
	if forward1 == "True":
		forward1 = "False"
	else:
		forward1 = "True"
	motor.motor1(forward1)
	text = 'Right motor reverse to ', forward1
	return HttpResponse(text)

def calibrate_pan(request, direction, in_offset_x):
	global offset_x, offset_y
	offset_x = int(in_offset_x)
	if direction == '-':
		offset_x = - offset_x
	video_dir.calibrate(offset_x, offset_y)
	text = 'Pan offset set to: ', offset_x
	return HttpResponse(text)

def calibrate_tile(request, direction, in_offset_y):
	global offset_x, offset_y
	offset_y = int(in_offset_y)
	if direction == '-':
		offset_y = - offset_y
	video_dir.calibrate(offset_x, offset_y)
	text = 'Tile offset set to: ', offset_y
	return HttpResponse(text)

def calibrate_confirm(request):
	global offset, offset_x, offset_y, forward0, forward1
	config = 'offset_x = %s\noffset_y = %s\noffset = %s\nforward0 = %s\nforward1 = %s\n ' % (offset_x, offset_y, offset, forward0, forward1)

	fd = open(FILE_CONFIG, 'w')
	fd.write(config)
	fd.close()
	return HttpResponse(config)

def test(request, direction, text):
	text = direction + str(text)
	return HttpResponse(text)

def client(request):
    	return render(request, 'client.html')
