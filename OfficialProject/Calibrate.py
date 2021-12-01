import cv2
import numpy as np
import serial
from threading import Thread

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    from PiVideoStream import PiVideoStream
except:
    pass
#from UniTools import Filter, FPSCounter, Repeater
from pygame.math import Vector2
#from Constants import *
from Settings import Settings
#import imutils
import time
#import random

class Calibrate():

    def __init__(self, settings=None):
        if settings is None:
            settings = Settings('AirHockey_settings.obj')
            self.settings = settings.camera
        else:
            self.settings = settings

        self.piVideo = None
        self.camera = None

        self.lower=0
        self.upper=0

        self.center = (0, 0)
        self.centerX=0
        self.centerY=0
        self.x=0
        self.y=0
        self.h=0
        self.w=0
        #self.detectionStopped = True
        #self.analyzingStopped = True

        #self.Calibration=None
        self.startCamera = True
        self.analyzeColor=True
        #self.multipleDetection=True
        #self.frame = None
        self.callback = self._nothing
        #serial identifications
        self._ser = None
        self._baudRate = 115200


    def _nothing(self, *args):
        pass

    def pixeltoUnits(self):
        self.centerX = int(self.center[0]) / 8.365;  # pixels/inches=8.365
        self.centerY = int(self.center[1]) / 8.365;
        return self

    #def unitsToPixels(self, unitPos):


    def Calibration(self, Title):
        cap = cv2.VideoCapture(0)
        cv2.namedWindow(Title)

        cv2.createTrackbar("L-H", Title, 0, 179, self._nothing)
        cv2.createTrackbar("L-S", Title, 0, 255, self._nothing)
        cv2.createTrackbar("L-V", Title, 0, 255, self._nothing)
        cv2.createTrackbar("U-H", Title, 179, 179, self._nothing)
        cv2.createTrackbar("U-S", Title, 255, 255, self._nothing)
        cv2.createTrackbar("U-V", Title, 255, 255, self._nothing)

        while True:
            _, frame = cap.read()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            l_h = cv2.getTrackbarPos("L-H", Title)
            l_s = cv2.getTrackbarPos("L-S", Title)
            l_v = cv2.getTrackbarPos("L-V", Title)
            u_h = cv2.getTrackbarPos("U-H", Title)
            u_s = cv2.getTrackbarPos("U-S", Title)
            u_v = cv2.getTrackbarPos("U-V", Title)

            self.lower = np.array([l_h, l_s, l_v])
            self.upper = np.array([u_h, u_s, u_v])
            mask = cv2.inRange(hsv, self.lower, self.upper)
            result = cv2.bitwise_and(frame, frame, mask=mask)

            #cv2.imshow("frame", frame)
            #cv2.imshow("mask", mask)
            cv2.imshow("result", result)

            key = cv2.waitKey(1)
            if key == 32:  # space key
                cap.release()
                cv2.destroyAllWindows()
                break

        #return lower, upper, mask, result

    #def startCamera(self):
        #if self.piVideo is None:
          #  self.piVideo = PiVideoStream(self.settings["resolution"], self.settings["fps"],
         #                                self.settings["whiteBalance"])
          #  self.camera = self.piVideo.camera

        #self.piVideo.start()


    #def analyzeColor(self):
        #while True:
            #if self.piVideo.newFrame:

    def multipleDetection(self, title1, title2,lower_puck,upper_puck,lower_pusher, upper_pusher, x, y,h,w):
        while True:
            webcam = cv2.VideoCapture(0)
            while (1):
                # Reading the video from the
                # webcam in image frames
                x, y, h, w = 80, 80, 400, 400;
                _, Frame = webcam.read()
                imageFrame = Frame[y:y+h, x:x+w]
                kernal = np.ones((5, 5), "uint8")

                hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

                mask_puck = cv2.inRange(hsvFrame, lower_puck, upper_puck)
                mask_pusher = cv2.inRange(hsvFrame, lower_pusher, upper_pusher)

                mask = cv2.dilate(mask_puck, kernal)
                result = cv2.bitwise_and(imageFrame, imageFrame,
                                         mask=mask)

                # Creating contour
                contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                for pic, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    if (area > 300):
                        (x, y), radius = cv2.minEnclosingCircle(contour)
                        center = (int(x), int(y))
                        radius = int(radius)
                        imageFrame = cv2.circle(imageFrame, center, radius,
                                                (255, 0, 0), 2)
                        cv2.putText(imageFrame, title1, center,
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1.0, (255, 0, 0))

                #pusher
                mask_pusher = cv2.dilate(mask_pusher, kernal)
                result = cv2.bitwise_and(imageFrame, imageFrame,
                                         mask=mask_pusher)

                contours, hierarchy = cv2.findContours(mask_pusher, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                for pic, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    if (area > 300):
                        (x, y), radius = cv2.minEnclosingCircle(contour)
                        center = (int(x), int(y))
                        radius = int(radius)
                        imageFrame = cv2.circle(imageFrame, center, radius,
                                                (0, 255, 255), 2)
                        cv2.putText(imageFrame, title2, center,
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1.0, (0, 255, 255))


                cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)
                #cv2.imshow("frame", Frame)

                key = cv2.waitKey(1)
                if key == 32:  # space key
                    webcam.release()
                    cv2.destroyAllWindows()
                    break
            break


    def detection(self,Frame):
        #Read puck or Pusher lower and upper bounds, Convert to Units, send to Arduino
        #while (1):
        # Reading the video from the
        # webcam in image frames
        x, y, h, w = 80, 80, 400, 600;
        #_, Frame = webcam.read()
        imageFrame = Frame[y:y + h, x:x + w]
        kernal = np.ones((5, 5), "uint8")

        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsvFrame, self.lower, self.upper)

        mask = cv2.dilate(mask, kernal)
        result = cv2.bitwise_and(imageFrame, imageFrame,
                                 mask=mask)

        # Creating contour
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                (x, y), radius = cv2.minEnclosingCircle(contour)
                self.center = (int(x), int(y))
                print(self.center)
                self.pixeltoUnits()
                print("calc",self.centerX,",",self.centerY)
                radius = int(radius)
                imageFrame = cv2.circle(imageFrame, self.center, radius,
                                        (255, 0, 0), 2)
                cv2.putText(imageFrame, "puck", self.center,
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0, (255, 0, 0))
            #cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)
        #cv2.imshow("frame", Frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                 cap.release()
                 cv2.destroyAllWindows()
                 break

            #self.centerX,self.centerY=pixeltoUnits(self,center)


#
# if __name__ == "__main__":
#     camera = Calibrate()
#     #camera.startCamera()
#     print("Detect puck color")
#     lower_puck,upper_puck,mask_puck,result_puck=camera.Calibration("Puck Trackbar")
#     print("Detect pusher color")
#     lower_pusher, upper_pusher, mask_pusher, result_pusher = camera.Calibration("Pusher Trackbar")
#     # identify puck and pusher inside the frame
#     camera.multipleDetection("Puck", "Pusher", lower_puck,upper_puck, lower_pusher, upper_pusher);
#



