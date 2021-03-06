/* Inputs direction data from Raspberry Pi and writes to a stepper motor, turning it toward the location
Outputs magnetometer heading data to RasPi
*/

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>
#include <Adafruit_MotorShield.h>
#include <utility/Adafruit_PWMServoDriver.h>
                
const int stepsPerRevolution = 200; // change this to match the stepper motor we use
boolean newBuffer = false; // did new info come from Python?
String buffer;  // string built from serial
float angle;
byte pressed = 0;
byte switched = 0;
byte buttonPin = 2;
boolean standby = true;
byte switchPin = 6;

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_StepperMotor *myMotor = AFMS.getStepper(200,1);

// Assign a unique ID to the magnetometer
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);

void setup()
{ 
  Serial.begin(9600);
  myMotor->setSpeed(15); // speed set in rpm
  mag.begin();
} 
 
void loop() 
{ 
  if (standby == true){
    pressed = digitalRead(buttonPin);
    if (pressed == 1){
      standby = false;
      Serial.println("interrupt");
    }
  }
  // while Python is sending over Serial, append characters to buffer
  while (Serial.available()>0) {
    char ch = Serial.read();
    buffer += ch;
    newBuffer = true;
    delay(2); // pause to minimize noise
  }
  // If there's a new input, change the stuff
  if (newBuffer) {
    if (buffer == "need_heading"){
        float heading = getHeading();
        Serial.println(heading);
        buffer = "";
    }else{
        standby = true;
        
        int angle = buffer.toInt();
        while(switched != true){
            switched = digitalRead(switchPin);
            myMotor->step(1, BACKWARD, SINGLE);
        }
        myMotor->step(angle, FORWARD, SINGLE);
        newBuffer = false;
        buffer = "";
        switched = digitalRead(switchPin);
    }
  }
}

String getSubString(String data, char separator, int index)
{
 int found = 0;
  int strIndex[] = {0, -1  };
  int maxIndex = data.length()-1;
  for(int i=0; i<=maxIndex && found<=index; i++){
  if(data.charAt(i)==separator || i==maxIndex){
  found++;
  strIndex[0] = strIndex[1]+1;
  strIndex[1] = (i == maxIndex) ? i+1 : i;
  }
 }
  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

float getHeading(){
  /* Get a new sensor event */ 
  sensors_event_t event; 
  mag.getEvent(&event);

  float heading = atan2(event.magnetic.y, event.magnetic.x);
  
  // Declination angle for Olin is roughly -14deg West, or 0.24rad
  float declinationAngle = 0.24;
  heading += declinationAngle;
  
  // Correct for when signs are reversed.
  if(heading < 0)
    heading += 2*PI;
    
  // Check for wrap due to addition of declination.
  if(heading > 2*PI)
    heading -= 2*PI;
   
  // Convert radians to degrees for readability.
  float headingDegrees = heading * 180/M_PI; 
  
  Serial.println(headingDegrees);
}
