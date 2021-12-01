# Python code for Multiple Color Detection

import numpy as np
import cv2
import serial
import time
import sys

# Capturing video through webcam
cap = cv2.VideoCapture(0)
puck_detection_counter = 0

x = 0
y = 0
old_x = 0
old_y = 0
old_time = time.time()

    # Start a while loop
while (1):
    # iterate counter
    puck_detection_counter += 1

    # Reading the video from the
    # webcam in image frames
    _, imageFrame = cap.read()

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

    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    # For yellow color
    yellow_mask = cv2.dilate(yellow_mask, kernal)
    res_yellow = cv2.bitwise_and(imageFrame, imageFrame,
                                     mask=yellow_mask)

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

            cv2.putText(imageFrame, "X:" + str(int(x)) + " Y:" + str(int(y)), center,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (0, 255, 255))


    # get time difference:
    time_difference = time.time() - old_time

    # print out puck's velocity every 0.5s
    #if puck_detection_counter == 100:
    if time_difference >= 0.5:
        # output variables to command window
        displacement = (((x-old_x) ** 2) + ((y-old_y) ** 2)) ** (1/2)
        velocity = displacement / time_difference
        if x-old_x == 0:
            angle_rad = 0
        else:
            angle_rad = np.arctan((y-old_y)/(x-old_x))
        sys.stdout.write("Speed: " + str(velocity) + " Direction: " + str(angle_rad) + "\n")
        old_time = time.time()
        old_x = x
        old_y = y
        puck_detection_counter = 0

    # Program Termination
    cv2.imshow("Puck Velocity Detection", imageFrame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
    
exit()