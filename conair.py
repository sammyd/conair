import serial
import math

def calculate_temp(value):
    voltage = float(value) / 1024 * 5
    resistance = 10000 / (5 / voltage - 1)
    temp = 1 / (1/298.15 + math.log(resistance / 10000) / 3977)
    print "Temperature is: %f K, (%f degC)" % (temp, temp-273.15)
    return

ser = serial.Serial('/dev/tty.usbserial-A800etDk', 9600)
while 1:
    r = ser.readline()
    split = r.split(": ")
    if split[0] == "sensorValue":
        value = split[1].strip()
        calculate_temp(value)

