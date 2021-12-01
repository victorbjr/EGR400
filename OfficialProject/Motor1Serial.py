import serial
import time
#from UniTools import FPSCounter
from threading import Thread
from datetime import datetime

class Motor1Serial():
	def __init__(self):
		#self.settings = None
		# Reading ----
		self.vectors = [(0,0), (0,0)]
		self.homed = True
		self.goal = None
		self.status = None
		self.readHistory = []
		self.writeHistory = []

		self._readingLine = ""
		self._writingLine = ""
		self._writingQueue = []

		self.error = False

		self._baudRate = 9600
		#self._readingCounter = FPSCounter(60)
		#self._writingCounter = FPSCounter(60)
		self._ser1 = None

		self._stopped = True
		self._lastRead = 0
		self._lastWriteAt = 0


	def writeCenterData(self, centerX, centerY, centerXR, centerYR):
		print("self.centerX", centerX)
		self._ser1.write((str(centerX) + 'x' + str(centerY) + 'y').encode('ascii'));
		#self._ser1.write((str(centerXR) + 'x' + str(centerYR) + 'y').encode('ascii'));
		line_x = self._ser1.readline().decode('utf-8').rstrip()
		line_y = self._ser1.readline().decode('utf-8').rstrip()
		#line_xR = self._ser1.readline().decode('utf-8').rstrip()
		#line_yR = self._ser1.readline().decode('utf-8').rstrip()
		print(line_x)
		print(line_y)
		#print(line_xR)
		#print(line_yR)
		time.sleep(1)


	def start(self):
		self._ser1 = serial.Serial('/dev/ttyACM0', self._baudRate)
		self._ser1.flush()
		print("Communication started Motor1.")
		return self


	def stop(self):
		self._ser1 = None
		self._stopped = True
		print("Communication _stopped.")
