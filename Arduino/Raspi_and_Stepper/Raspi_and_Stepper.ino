// NOTE: must add limit switch to zero stepper motor @ startup

/* Inputs distance and direction data from Raspberry Pi and writes to a stepper motor, turning it toward 
   the location
*/


#include <Stepper.h> // include step motor library
#include <LiquidCrystal.h>  // include library for LCD display
                
const int stepsPerRevolution = 200; // change this to match the stepper motor we use
boolean newBuffer = false; // did new info come from Python?
String buffer;  // string built from serial
String place; // strings for Python input
String distance;
String angle;

Stepper motor(stepsPerRevolution, 8, 9, 10, 11);  // create stepper object to control a motor 
// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(13, 12, 5, 4, 3, 2);
 
void setup()
{ 
  Serial.begin(9600);
  motor.setSpeed(30); // speed set in rpm
  lcd.begin(16, 2);
  lcd.print("Ready for Location");
} 
 
 
void loop() 
{ 
  while (Serial.available()>0) {
    char ch = Serial.read();
    buffer += ch;
    newBuffer = true;
    delay(2); // pause to minimize noise
  }
  // If there's a new input, change the stuff
  if (newBuffer) {
    place = getSubString(buffer, ':', 0);
    distance = getSubString(buffer, ':', 1);
    angle = getSubString(buffer, ':', 2);
    
    char carray[distance.length() + 1];
    distance.toCharArray(carray, sizeof(carray));
    float distanceVal = atof(carray);
    char carray2[angle.length() + 1];
    angle.toCharArray(carray2, sizeof(carray));
    float angleVal = atof(carray2);

    Serial.println(place);
    Serial.println(distanceVal);
    Serial.println(angleVal);
    displayPost(place, distance);
    float adjusted_angle = (angleVal/360)*200;
    motor.step(adjusted_angle);
    newBuffer = false;
    buffer = "";
  }
}

void displayPost(String name, String dist) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(name);
  lcd.setCursor(0, 1);
  lcd.print(dist);
  lcd.print(" miles");
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
