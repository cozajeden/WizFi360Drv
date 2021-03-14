import serial
from settings import *
from SSIDPASS import *

ser = serial.Serial('COM11', 115200)
temp = ''
while temp != b'ready\r\n':
    temp = ser.readline()
    print(temp)
while temp != b'OK\r\n':
    temp = ser.write(b'AT\r\n')
    temp = ser.readline()
    print(temp)