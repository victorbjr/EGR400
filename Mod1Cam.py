#from picamera.array import PiRGBARRAY
from picamera import PiCamera
import time
from time import sleep
import cv2

camera = PiCamera()

camera.resolution = (320, 192)
camera.framerate = 30
#rawCapture=PiRGBARRAY(camera,size=(640,480))
#time.sleep(0.1)
camera.start_preview()
sleep(100)
camera.stop_preview()

#Taking a picture
#camera.start_preview()
#sleep(5)
#camera.capture('/home/pi/Desktop/image.jpg')
#camera.stop_preview()

#Taking a video
#camera.start_preview()
#camera.start_recording('/home/pi/Desktop/video.h264')
#sleep(5)
#camera.stop_recording()
#camera.stop_preview()