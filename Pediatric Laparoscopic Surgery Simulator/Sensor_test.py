
import time
import serial

ser = serial.Serial('COM5', 19200)
while True:
    stuff = ser.readline()
    stuff_string = stuff.decode()
    string = stuff_string.rstrip()
    print(string)
    time.sleep(0.1)
