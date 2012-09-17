/*
* Generate a 1Khz square wave on pin 3
* Read analog voltage on pin 0,1,2 send to serial port every 3 seconds
*/


const int analogInPin0 = A0; // Analog input pin
const int analogInPin1 = A1; // Analog input pin
const int analogInPin2 = A2; // Analog input pin


int sensorValue0 = 0;
int sensorValue1 = 0;
int sensorValue2 = 0;


void setup() {

// initialize serial communications at 9600 bps:

Serial.begin(9600);

// set pwm registers for approx 1Khz
pinMode(3, OUTPUT);
pinMode(11, OUTPUT);
TCCR2A = _BV(COM2A1) | _BV(COM2B1) | _BV(WGM21) | _BV(WGM20);
TCCR2B = _BV(CS22);
OCR2A = 180;
OCR2B = 50;
}

void loop() {
// read the analog pins
sensorValue0 = analogRead(analogInPin0);
delay(4);
sensorValue1 = analogRead(analogInPin1);
delay(4);
sensorValue2 = analogRead(analogInPin2);
delay(4);

// print the results to the serial monitor:

Serial.print("sensorValue0 = " );
Serial.println(sensorValue0);

Serial.print("sensorValue1 = " );
Serial.println(sensorValue1);

Serial.print("sensorValue2 = " );
Serial.println(sensorValue2);

// wait 3 seconds before the next readings

delay(3000-12);
}