# Python code for Multiple Color Detection

import numpy as np
import cv2
import serial
import time

#ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
#ser.flush()
def nothing(x):
    pass
Title="Pusher Trackbar"

while True:
#def detection(Title,):
# Capturing video through webcam
    webcam = cv2.VideoCapture(0)
    cv2.namedWindow(Title)
    name=Title.split()

    cv2.createTrackbar("L-H", Title, 0, 179, nothing)
    cv2.createTrackbar("L-S", Title, 0, 255, nothing)
    cv2.createTrackbar("L-V", Title, 0, 255, nothing)
    cv2.createTrackbar("U-H", Title, 179, 179, nothing)
    cv2.createTrackbar("U-S", Title, 255, 255, nothing)
    cv2.createTrackbar("U-V", Title, 255, 255, nothing)

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

        l_h = cv2.getTrackbarPos("L-H", Title)
        l_s = cv2.getTrackbarPos("L-S", Title)
        l_v = cv2.getTrackbarPos("L-V", Title)
        u_h = cv2.getTrackbarPos("U-H", Title)
        u_s = cv2.getTrackbarPos("U-S", Title)
        u_v = cv2.getTrackbarPos("U-V", Title)

        lower = np.array([l_h, l_s, l_v])
        upper = np.array([u_h, u_s, u_v])
        mask = cv2.inRange(hsvFrame, lower, upper)
        result = cv2.bitwise_and(imageFrame, imageFrame, mask=mask)

        cv2.imshow("frame", imageFrame)
        cv2.imshow("mask", mask)
        cv2.imshow("result", result)

        # Morphological Transform, Dilation
        # for each color and bitwise_and operator
        # between imageFrame and mask determines
        # to detect only that particular color
        kernal = np.ones((5, 5), "uint8")

        mask = cv2.dilate(mask, kernal)
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
                                        (0, 255, 255), 2)

                cv2.putText(imageFrame, name[0], center,
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0, (0, 255, 255))


        # # Creating contour to track yellow color
        # contours, hierarchy = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #
        # for pic, contour in enumerate(contours):
        #     area = cv2.contourArea(contour)
        #     if (area > 300):
        #         (x, y), radius = cv2.minEnclosingCircle(contour)
        #         center=(int(x),int(y))
        #         radius = int(radius)
        #         imageFrame = cv2.circle(imageFrame, center,radius,
        #                                    (0,255,255), 2)
        #
        #         cv2.putText(imageFrame, "Yellow Color", center,
        #                     cv2.FONT_HERSHEY_SIMPLEX,
        #                     1.0, (0, 255, 255))
        #         #print("Yellow pixels",center)
        #         centerX=int(x)/8.365; #pixels/inches=8.365
        #         centerY=int(y)/8.365;
        #         #return centerX,centerY
        #         print("Yellow", centerX, ",", centerY)
        #         #centerXY = (centerX, centerY);
        # output = ser.write((str(centerX) + 'x' + str(centerY) + 'y').encode('ascii'));
        # linex = ser.readline().decode('utf-8').rstrip()
        # liney = ser.readline().decode('utf-8').rstrip()
        # print(linex)
        # print(liney)
        # time.sleep(0.1)

        # Program Termination
        cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
