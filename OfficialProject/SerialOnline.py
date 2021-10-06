import serial
import time
from UniTools import FPSCounter
from threading import Thread
from datetime import datetime

class Serial():
	def __init__(self, settings):
		self.settings = settings
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

		self._prevRead = ""
		self._prevWrite = ""

		self._baudRate = 115200
		self._readingCounter = FPSCounter(60)
		self._writingCounter = FPSCounter(60)
		self._ser = None

		self._stopped = True
		self._lastRead = 0
		self._lastWriteAt = 0

	def readStatus(self):
		output = self.status
		self.status = None
		return output

	def writeLine(self, txt, *args):
		self._writingLine = txt


    def _reading(self):
        _prevTime = time.time()
        _num = 0
        while True:
            self._lastRead = time.time()
            self._readingCounter.tick()
            try:
                self._readingLine = self._ser.readline().decode('utf-8').rstrip()
            except:
                self.stop()
                self.error = True
                print("Communication error")
            try:
                # print(self._readingLine)
                if not self._readingLine == "":
                    self._prevRead = self._readingLine
                    self.readHistory.insert(0, "{}  <-  {}".format(datetime.now().strftime('%H:%M:%S.%f')[:-2],
                                                                   self._readingLine))
                    self._parseReading(self._readingLine)
                    _num += 1
                if time.time() - _prevTime > 1:
                    _prevTime = time.time()
                    # print(_num)python

                    _num = 0
            except:
                print("Error while decoding")

            while len(self.readHistory) > 200:
                self.readHistory.pop()

            sleepTime = 1 / 300 - (time.time() - self._lastRead)
            if sleepTime > 0:
                time.sleep(sleepTime)

            if self._stopped:
                return


    def _writing(self):
        while True:
            self._lastWriteAt = time.time()
            queueLine = False
            # print(time.time())
            lineToWrite = self._writingLine
            if len(self._writingQueue) > 0:
                lineToWrite = self._writingQueue[0]
                self._writingQueue.pop(0)
                queueLine = True

            if not lineToWrite == self._prevWrite and not lineToWrite == "":
                self._writingCounter.tick()
                self._ser.write((str(lineToWrite) + '\n').encode('ascii'))
                self.writeHistory.insert(0, "{}  ->  {}".format(datetime.now().strftime('%H:%M:%S.%f')[:-2], lineToWrite))
                if queueLine == False:
                    self._prevWrite = lineToWrite
            # print((str(lineToWrite) + '\n'))

            while len(self.writeHistory) > 200:
                self.writeHistory.pop()

            sleepTime = 1 / 200 - (time.time() - self._lastWriteAt)
            if sleepTime > 0:
                time.sleep(sleepTime)

            if self._stopped:
                return


    def start(self):
        if self._stopped:
            for i in range(9):
                try:
                    try:
                        self._ser = serial.Serial('/dev/ttyACM' + str(i), self._baudRate)
                    except:
                        self._ser = serial.Serial('/dev/ttyUSB' + str(i), self._baudRate)
                except:
                    continue
            self._ser.flush()
            self._readingCounter.start()
            self._writingCounter.start()
            self._stopped = False
            Thread(target=self._reading, args=()).start()
            Thread(target=self._writing, args=()).start()
            self.error = False
            print("Communication started.")
        return self


    def stop(self):
        self._readingCounter.stop()
        self._writingCounter.stop()
        self._ser = None
        self._stopped = True
        print("Communication _stopped.")


if __name__ == '__main__':
    serial = Serial().start()
    serial._readingCounter.schedulePrint(0.5, "Reading:")
    serial._writingCounter.schedulePrint(0.5, "Writing:")

    while True:
        serial.writeLine(input())
