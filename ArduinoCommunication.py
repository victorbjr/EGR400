# #!/usr/bin/env python3
# import serial
#
# if __name__ == '__main__':
#     ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
#     ser.flush()
#
#     while True:
#        if ser.in_waiting > 0:
#
#             line = ser.readline()
#             print(line)

# import serial
# import time
# if __name__ == '__main__':
#     ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
#     ser.flush()
#     while True:
#         ser.write(b"2000\n")
#         line = ser.readline().decode('utf-8').rstrip()
#         print(line)
#         time.sleep(1)

#!/usr/bin/env python3
import serial
import time
if __name__ == '__main__':
    ser1 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
#    ser2 = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    ser1.flush()
#    ser2.flush()
    centerX = -550;
    centerY = -500;
    centerX1= 550;
    centerY1= 500;
    while True:
        print("CenterXY")
        output = ser1.write((str(centerX) + 'x' + str(centerY) + 'y').encode('ascii'));
        #output1 = ser2.write((str(centerX1) + 'x' + str(centerY1) + 'y').encode('ascii'));
        #ser.write(centerXY.encode('ascii') + b'\n')
        #ser.write(b'2000')
        linex = ser1.readline().decode('utf-8').rstrip()
        #liney = ser2.readline().decode('utf-8').rstrip()
        print(linex)
        #print(liney)
        time.sleep(2)