import serial
import time
from Constants import *
from Motor1Serial import *
from Motor2Serial import *
from Calibrate import *
from pygame.math import Vector2
import PySimpleGUI as sg
#Set_options or sg.theme

if __name__ == "__main__":
    #set up objects
    puck = Calibrate()
    pusher = Calibrate()
    camera = Calibrate()
    #serialObj = Serial()

    #GUI design
    sg.theme('DarkBlue17')
    row1=[sg.Text('            Puck',size=(13,1)),sg.Text('Robot')]
    ImgCol=[[sg.Image(filename='',key='image')]]
    row2=[sg.Text('L-H',size=(5,1)),sg.Input(key='PL-H', size=(6,1)),sg.Input(key='RL-H', size=(6,1))]
    row3=[sg.Text('L-S',size=(5,1)),sg.Input(key='PL-S', size=(6,1)),sg.Input(key='RL-S', size=(6,1))]
    row4=[sg.Text('L-V',size=(5,1)),sg.Input(key='PL-V', size=(6,1)),sg.Input(key='RL-V', size=(6,1))]
    row5=[sg.Text('U-H',size=(5,1)),sg.Input(key='PU-H', size=(6,1)),sg.Input(key='RU-H', size=(6,1))]
    row6=[sg.Text('U-S',size=(5,1)),sg.Input(key='PU-S', size=(6,1)),sg.Input(key='RU-S', size=(6,1))]
    row7=[sg.Text('U-V',size=(5,1)),sg.Input(key='PU-V', size=(6,1)),sg.Input(key='RU-V', size=(6,1))]
    row8=[sg.Text('Cropped Frame')]
    row9=[sg.Text('x',size=(2,1)), sg.Input(key='x', size=(5,1)),
          sg.Text('y',size=(2,1)), sg.Input(key='y', size=(5,1)),
          sg.Text('w',size=(2,1)), sg.Input(key='w', size=(5,1)),
          sg.Text('h',size=(2,1)), sg.Input(key='h', size=(5,1))]
    row10=[sg.Button("Set Frame"),sg.Button("Set Limits"),sg.Button("Calibrate")]
    col1=[row1,row2,row3,row4,row5,row6, row7, row8, row9, row10]
    layout = [[sg.Column(col1),sg.VSeperator(),sg.Column(ImgCol)],
            [sg.Button("Play"), sg.Button("Exit")]]
    window = sg.Window('AirHockey Robot',layout)

    cap = cv2.VideoCapture(0)       # Setup the camera as a capture device

    while True:   #Event loops
        event, values = window.Read(timeout=0, timeout_key='timeout')
        ret,frame=cap.read()
        imgbytes=cv2.imencode('.png',frame)[1].tobytes()
        window['image'].update(data=imgbytes)
        x, y, h, w = 80, 80, 400, 400;
        Frame = frame[y:y+h, x:x+w]
        cv2.imshow("frame", Frame)


        if event=="Calibrate":
            cap.release()
            puck.Calibration("Puck Trackbar")
            pusher.Calibration("Pusher Trackbar")
            camera.multipleDetection("Puck", "Pusher", puck.lower, puck.upper, pusher.lower, pusher.upper, x, y, w, h)

        if event=="Set Limits":
            cap.release()
            puck.lower=(int(values['PL-H']),int(values['PL-S']),int(values['PL-V']))
            puck.upper = (int(values['PU-H']), int(values['PU-S']), int(values['PU-V']))
            pusher.lower = (int(values['RL-H']), int(values['RL-S']), int(values['RL-V']))
            pusher.upper = (int(values['RU-H']), int(values['RU-S']), int(values['RU-V']))
            #Display it in the window
            camera.multipleDetection("Puck", "Pusher", puck.lower, puck.upper, pusher.lower, pusher.upper,x,y,w,h)
        if event == "Set Frame":
            x = int(values['x'])
            y = int(values['y'])
            h = int(values['h'])
            w = int(values['w'])
            frame=frame[y:y + h, x:x + w]

        if event=="Play":
            cap.release()
            #serialObj.start()
            while True:
                # Start camera
                webcam = cv2.VideoCapture(0)
                while True:
                    print("test")
                    _, Frame = webcam.read()
                    imageFrame = Frame[y:y + h, x:x + w]
                    # detect puck
                    puck.detection(imageFrame)
                    # detect pusher
                    pusher.detection(imageFrame)
                    # send coordinate to arduino function write
                    serialObj.writeCenterData(puck.centerX, puck.centerY)
                    serialObj.writeCenterData(pusher.centerX, pusher.centerY)
                    # send arduino Time
                    key = cv2.waitKey(1)
                    if key == 32:  # space key
                        webcam.release()
                        cv2.destroyAllWindows()
                        break
                break
                #serialObj.stop()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    window.close()






