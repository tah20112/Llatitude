// NOTE: must add limit switch to zero stepper motor @ startup

/* Inputs direction data from Raspberry Pi and writes to a stepper motor, turning it toward the location
Outputs magnetometer heading data to RasPi
*/

#include <AFMotor.h>
#include <Stepper.h> // include step motor library
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>
                
const int stepsPerRevolution = 200; // change this to match the stepper motor we use
boolean newBuffer = false; // did new info come from Python?
String buffer;  // string built from serial
float angle;

// create stepper object to control a motor
Stepper motor(stepsPerRevolution, 8, 9, 10, 11);

// Assign a unique ID to the magnetometer
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);

void setup()
{ 
  Serial.begin(9600);
  motor.setSpeed(30); // speed set in rpm
  mag.begin();
} 
 
void loop() 
{ 
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
        buffer = '';
    }else{
        angle = buffer.toFloat(); //getSubString(buffer, ':', 2);
        
        //char carray2[angle.length() + 1];
        //angle.toCharArray(carray2, sizeof(carray));
        //float angleVal = atof(carray2);

        float adjusted_angle = (angle/360)*200;
        motor.step(adjusted_angle);
        newBuffer = false;
        buffer = "";
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
