import serial
import math
import datetime
import random
from tempodb import Client, DataPoint

client = Client('cc0c654d01774b128c1e0495de51784b', 'a280c43f6b27400998a4aba0b1eb4545')

def calculate_temp(value):
    voltage = float(value) / 1024 * 5
    resistance = 10000 / (5 / voltage - 1)
    temp = 1 / (1/298.15 + math.log(resistance / 10000) / 3977)
    print "Temperature is: %f K, (%f degC)" % (temp, temp-273.15)
    return temp-273.15

ser = serial.Serial('/dev/tty.usbserial-A800etDk', 9600)
temperature_array = []
while 1:
    r = ser.readline()
    split = r.split(" = ")
    if split[0] == "sensorValue0":
        value = split[1].strip()
        temp = calculate_temp(value)
        temperature_array.append(temp)
        if(len(temperature_array) >= 20):
            mean = sum(temperature_array) / float(len(temperature_array)) 
            print "Saving off this minute's mean: %f" % mean
            client.write_key('temperature', [DataPoint(datetime.datetime.now(), mean)])
            temperature_array = []

