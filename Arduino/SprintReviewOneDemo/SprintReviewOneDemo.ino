// Sweep
// by BARRAGAN <http://barraganstudio.com> 
// This example code is in the public domain.


#include <Servo.h> 
 
Servo myservo;  // create servo object to control a servo 
                // a maximum of eight servo objects can be created 
 
int pos = 0;    // variable to store the servo position 
const float SIGN_LAT = 42.293045;
const float SIGN_LONG = -71.264086;
 
void setup() 
{ 
  Serial.begin(9600);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object 
  myservo.write(0);
  float angle2 = LatLngtoAngle(SIGN_LAT + 10, SIGN_LONG);
  int intangle = angle2;
  myservo.write(intangle);
} 
 
 
void loop() 
{ 
  //myservo.write(180);
//  for(pos = 0; pos < 180; pos += 1)  // goes from 0 degrees to 180 degrees 
//  {                                  // in steps of 1 degree 
//    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
//    delay(15);                       // waits 15ms for the servo to reach the position 
//  } 
//  for(pos = 180; pos>=1; pos-=1)     // goes from 180 degrees to 0 degrees 
//  {                                
//    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
//    delay(15);                       // waits 15ms for the servo to reach the position 
//  } 

  //int up = LatLngtoAngle(SIGN_LAT + 10, SIGN_LONG);
  //Up
  Serial.println("Up");
  myservo.write(LatLngtoAngle(SIGN_LAT + 10, SIGN_LONG));
  delay(1000);
  // Left
  Serial.println("Left");
  myservo.write(LatLngtoAngle(SIGN_LAT, SIGN_LONG + 10));
  delay(1000);
  Serial.println("Down");
  myservo.write(LatLngtoAngle(SIGN_LAT - 10, SIGN_LONG));
  delay(1000);
  Serial.println("Right");
  myservo.write(LatLngtoAngle(SIGN_LAT, SIGN_LONG - 10));
  delay(1000);
  Serial.println("Germany");
  myservo.write(LatLngtoAngle(51.091606, 10.736070));
  delay(1000);
  
}

float LatLngtoAngle(float Lat,float Long)
{
	float deltaLat = Lat - SIGN_LAT;
//Serial.println(deltaLat);
	float deltaLong = Long - SIGN_LONG;
//Serial.println(deltaLong);
        float angleRad;
        if (deltaLong == 0) {
          if (deltaLat >= 0) {
            angleRad = 3.14/2;
          }
          else {
            angleRad = -3.14/2;
          }
          //Serial.println("deltaLong is zero");
        }
        else if (deltaLat == 0) {
          if (deltaLong >= 0) {
            angleRad = 3.14;
          }
          else {
            angleRad = 0;
          }
          //Serial.println("deltaLat is zero");
        }
        else {
	  angleRad = 3.14 - atanf(deltaLat/deltaLong);
          Serial.println("nothing is zero");
          Serial.println(angleRad);
        }
        //Serial.println(angleRad);
        float res = angleRad*(180/3.14)/2;
        if (res < 0) {
          res = res + 180;
        }
        Serial.println(res);
	return res;
}
