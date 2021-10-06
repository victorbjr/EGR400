# Python code for Multiple Color Detection

import numpy as np
import cv2
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()

while True:
#def detection():
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

        # Set range for red color and
        # define mask
        red_lower = np.array([136, 87, 111], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8)
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

        # Set range for green color and
        # define mask
        green_lower = np.array([35, 45, 100], np.uint8)
        green_upper = np.array([102, 255, 255], np.uint8)
        green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

        # Set range for blue color and
        # define mask
        blue_lower = np.array([90, 50, 70], np.uint8)
        blue_upper = np.array([128, 255, 255], np.uint8)
        blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

        # Set range for blue color and
        # define mask
        yellow_lower = np.array([25, 50, 70], np.uint8)
        yellow_upper = np.array([35, 255, 255], np.uint8)
        yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

        # Morphological Transform, Dilation
        # for each color and bitwise_and operator
        # between imageFrame and mask determines
        # to detect only that particular color
        kernal = np.ones((5, 5), "uint8")

        # For red color
        red_mask = cv2.dilate(red_mask, kernal) #magnifies object
        res_red = cv2.bitwise_and(imageFrame, imageFrame,
                                  mask=red_mask)

        # For green color
        green_mask = cv2.dilate(green_mask, kernal)
        res_green = cv2.bitwise_and(imageFrame, imageFrame,
                                    mask=green_mask)

        # For blue color
        blue_mask = cv2.dilate(blue_mask, kernal)
        res_blue = cv2.bitwise_and(imageFrame, imageFrame,
                                   mask=blue_mask)

        # For yellow color
        yellow_mask = cv2.dilate(yellow_mask, kernal)
        res_yellow = cv2.bitwise_and(imageFrame, imageFrame,
                                   mask=yellow_mask)

        # Creating contour to track red color
        contours, hierarchy = cv2.findContours(red_mask,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y),(x + w, y + h),(0, 0, 255), 2)

                cv2.putText(imageFrame, "Red Colour", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 0, 255))

        # Creating contour to track green color
        contours, hierarchy = cv2.findContours(green_mask,
                                                       cv2.RETR_TREE,
                                                       cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                           (x + w, y + h),
                                           (0, 255, 0), 2)

                cv2.putText(imageFrame, "Green Color", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0, (0, 255, 0))

        # Creating contour to track blue color
        contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                    x, y, w, h = cv2.boundingRect(contour)
                    imageFrame = cv2.rectangle(imageFrame, (x, y),(x + w, y + h),
                                                       (255, 0, 0), 2)

                    cv2.putText(imageFrame, "Blue Color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0))
            #print("blue", w,h)
        # Creating contour to track yellow color
        contours, hierarchy = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center=(int(x),int(y))
                radius = int(radius)
                imageFrame = cv2.circle(imageFrame, center,radius,
                                           (0,255,255), 2)

                cv2.putText(imageFrame, "Yellow Color", center,
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0, (0, 255, 255))
                #print("Yellow pixels",center)
                centerX=int(x)/8.365; #pixels/inches=8.365
                centerY=int(y)/8.365;
                #return centerX,centerY
                print("Yellow", centerX, ",", centerY)
                #centerXY = (centerX, centerY);
        output = ser.write((str(centerX) + 'x' + str(centerY) + 'y').encode('ascii'));
        linex = ser.readline().decode('utf-8').rstrip()
        liney = ser.readline().decode('utf-8').rstrip()
        print(linex)
        print(liney)
        time.sleep(1)

        # Program Termination
        cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

#if __name__ == '__main__':
    #ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    #ser.flush()
    #centerX = 200;
    #centerY = 400;
    #while True:
    #output = ser.write((str(centerX) + ',' + str(centerY) + '\n').encode('ascii'));
        # ser.write(centerXY.encode('ascii') + b'\n')
        # ser.write(b'2000')
    #line = ser.readline().decode('utf-8').rstrip()
    #print(line)
    #time.sleep(1)





    #
    # with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
    #     time.sleep(0.1)
    #     if arduino.isOpen():
    #         print("{} connected!".format(arduino.port))
    #         try:
    #             while True:
    #                 centerX,centerY=detection();
    #                 arduino.write((str(centerX) + ',' + str(centerY) + '.').encode('ascii'));
    #                 line = arduino.readline().decode('utf-8').rstrip()
    #                 print(line)
    #                 arduino.flushInput()
    #                 time.sleep(1);
    #         except KeyboardInterrupt:
    #             print("Ended")