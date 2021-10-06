import PySimpleGUI as sg
from tkinter import *
import cv2
import os
from PIL import Image, ImageTk
#Set_options or sg.theme
sg.theme('DarkBlue17')


row1=[sg.Text('            Puck',size=(13,1)),sg.Text('Robot')]
ImgCol=[[sg.Image(filename='',key='image',size=(100,100))]]
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
col1=[row1,row2,row3,row4,row5,row6, row7, row8, row9]
layout = [[sg.Column(col1),sg.VSeperator(),sg.Column(ImgCol)],
        [sg.Button("Calibrate")],
        [sg.Button("Play"), sg.Button("Exit")]]
window = sg.Window('AirHockey Robot',layout)
cap = cv2.VideoCapture(0)       # Setup the camera as a capture device
while True:                     # The PSG "Event Loop"
    event, values = window.Read(timeout=0, timeout_key='timeout')
    ret,frame=cap.read()                                           # if user closed window, quit
    imgbytes=cv2.imencode('.png',frame)[1].tobytes()
    window['image'].update(data=imgbytes)

    if event == "Exit" or event == sg.WIN_CLOSED:
        break
window.close()
