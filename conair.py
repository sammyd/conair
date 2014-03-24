import serial
import math
import datetime
import random
from tempodb import Client, DataPoint

POTENTIAL_DIVIDER_RESISTOR = 10000
THERMISTOR_B_VALUE = 3977
THERMISTOR_REF_TEMP = 298.15
THERMISTOR_REF_RESISTANCE = 10000

client = Client('cc0c654d01774b128c1e0495de51784b', 'a280c43f6b27400998a4aba0b1eb4545')

def calculate_temp(value):
    voltage = float(value) / 1024 * 5
    resistance = POTENTIAL_DIVIDER_RESISTOR / (5 / voltage - 1)
    temp = 1 / (1/THERMISTOR_REF_TEMP + math.log(resistance / THERMISTOR_REF_RESISTANCE) / THERMISTOR_B_VALUE)
    print "Temperature is: %f K, (%f degC)" % (temp, temp-273.15)
    return temp-273.15

ser = serial.Serial('/dev/tty.usbserial-A800etDk', 9600)
temperature_array = []
while 1:
    r = ser.readline()
    split = r.split(",")
    if(len(split) == 3):
        # Deal with the temperature pin first
        value = split[0].strip()
        temp = calculate_temp(value)
        temperature_array.append(temp)
        if(len(temperature_array) >= 20):
            mean = sum(temperature_array) / float(len(temperature_array)) 
            print "Saving off this minute's mean: %f" % mean
            try:
                client.write_key('temperature', [DataPoint(datetime.datetime.utcnow(), mean)])
            except ConnectionError as err:
                print "Failed to upload data point. Ignore this minute."

            temperature_array = []

        # And now the LDR resistance
        value = split[1].strip()
        voltage = float(value) / 1024 * 5
        resistance = POTENTIAL_DIVIDER_RESISTOR / (5 / voltage - 1)
        print "LDR resistance is: %f Ohms" % resistance

        # And finally, the humidity
        value = split[2].strip()
        print "Humidity reading is: %d" % float(value)

