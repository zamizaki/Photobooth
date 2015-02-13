#!/usb/bin/env python

import os
import glob
import time
from time import sleep
import RPi.GPIO as GPIO
import picamera
import atexit
import sys
import smtplib
import socket
import pygame
from signal import alarm, signal, SIGALRM, SIGKILL
import subprocess


#Variables Config

led1 = 15
led2 = 19
led3 = 21
led4 = 23
button1 = 22
button2 = 18
button3 = 16

total_pics = 4
capture_delay = 3
prep_delay = 4
file_path = '/home/pi/photobooth/pics/'

offset_x = 80
offset_y = 0
replay_delay = 1
replay_cycles = 4

#GPIO Setup

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led1_pin,GPIO.OUT) # LED 1
GPIO.setup(led2_pin,GPIO.OUT) # LED 2
GPIO.setup(led3_pin,GPIO.OUT) # LED 3
GPIO.setup(led4_pin,GPIO.OUT) # LED 4
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # falling edge detection on button 1
GPIO.setup(button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # falling edge detection on button 2
GPIO.setup(button3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # falling edge detection on button 3
GPIO.output(led1_pin,False);
GPIO.output(led2_pin,False);
GPIO.output(led3_pin,False);
GPIO.output(led4_pin,False);


#Functions

def exit_photobooth():
    sys.exit()
    #os.system("sudo reboot")
    


def start_photobooth():
    #Step 1#
    print "Get Ready..."
    camera = picamera.PiCamera()
    camera.resolution = (500, 375)
    camera.vflip = True
    camera.hflip = True
    camera.start_preview()
    i=1
    while i < prep_delay :
        #GPIO.output(led1,True); sleep(.5)
        #GPIO.output(led1,False); sleep(.5);
        i+=1
    #Step 2#
    print "Taking Picture..."
    now = time.strftime("%Y%m%d%H%M%S")
    try: #take the photos
	for i, filename in enumerate(camera.capture_continuous(file_path + now + '-' + '{counter:02d}.jpg')):
    	    #GPIO.output(led2_pin,True) #turn on the LED
    	    print(filename)
                #sleep(0.25) #pause the LED on for just a bit
                #GPIO.output(led2_pin,False) #turn off the LED
                sleep(capture_delay) # pause in-between shots
		if i == total_pics-1:
                    break
    finally:
        camera.stop_preview()
	camera.close()
	exit_photobooth()
