# Python code for Multiple Color Detection

import numpy as np
import cv2
import serial
import time

while True:
# Capturing video through webcam
    webcam = cv2.VideoCapture(0)

    # Start a while loop
    while (1):
        # Reading the video from the
        # webcam in image frames
        _, imageFrame = webcam.read()

        # Convert the imageFrame in
        # BGR(RGB color space) to
        # HSV(hue-saturation-value)
        # color space
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

        # Set range for yellow color and
        # define mask
        yellow_lower = np.array([25, 50, 70], np.uint8)
        yellow_upper = np.array([35, 255, 255], np.uint8)
        yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)
        
        # Set range for blue color and
        # define mask
        blue_lower = np.array([90, 50, 70], np.uint8)
        blue_upper = np.array([128, 255, 255], np.uint8)
        blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

        # Morphological Transform, Dilation
        # for each color and bitwise_and operator
        # between imageFrame and mask determines
        # to detect only that particular color
        kernal = np.ones((5, 5), "uint8")

        # For yellow color
        yellow_mask = cv2.dilate(yellow_mask, kernal)
        res_yellow = cv2.bitwise_and(imageFrame, imageFrame,
                                     mask=yellow_mask)
        
        # For blue color
        blue_mask = cv2.dilate(blue_mask, kernal)
        res_blue = cv2.bitwise_and(imageFrame, imageFrame,
                                     mask=blue_mask)

        # Creating contour for yellow
        contours, hierarchy = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)
                imageFrame = cv2.circle(imageFrame, center, radius,
                                        (0, 255, 255), 2)

                cv2.putText(imageFrame, "Yellow Puck", center,
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0, (0, 255, 255))
        
        # Creating contour for blue
        contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)
                imageFrame = cv2.circle(imageFrame, center, radius,
                                        (255, 0, 0), 2)

                cv2.putText(imageFrame, "Blue Puck", center,
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0, (255, 0, 0))

        # Program Termination
        cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
