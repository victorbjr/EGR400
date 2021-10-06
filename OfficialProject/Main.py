import serial
import time
from Constants import *
from Motor1Serial import *
from Motor2Serial import *
from Calibrate import *
from pygame.math import Vector2
import PySimpleGUI as sg

if __name__ == "__main__":
    #set up objects
    puck = Calibrate()
    pusher = Calibrate()
    camera = Calibrate()
    Motor1= Motor1Serial()
    Motor2 = Motor2Serial()
    x, y, h, w = 80, 80, 400, 400;

    puck.Calibration("Puck Trackbar")
    pusher.Calibration("Pusher Trackbar")
    #puck.lower=(100,110,30)
    #puck.upper=(179,255,255)
    #pusher.lower=(0,90,237)
    #pusher.upper=(145,255,255)
    camera.multipleDetection("Puck", "Pusher", puck.lower, puck.upper, pusher.lower, pusher.upper, x, y, w, h)

    Motor1.start()
    Motor2.start()
    while True:
        # Start camera
        webcam = cv2.VideoCapture(0)
        while True:
            print("test")
            _, Frame = webcam.read()
            #imageFrame = Frame[y:y+h, x:x+w]
            # detect puck
            puck.detection(Frame)
            # detect pusher
            pusher.detection(Frame)
            # send coordinate to arduino function write
            Motor1.writeCenterData(puck.centerX, puck.centerY,pusher.centerX, pusher.centerY)
            Motor2.writeCenterData(puck.centerX, puck.centerY, pusher.centerX, pusher.centerY)
            # send arduino Time
            key = cv2.waitKey(1)
            if key == 32:  # space key
                webcam.release()
                cv2.destroyAllWindows()
                break
        break
    Motor1.stop()
    Motor2.stop()

