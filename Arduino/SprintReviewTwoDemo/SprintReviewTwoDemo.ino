#include <Servo.h>
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
 
Servo myservo;  // create servo object to control a servo
 
int pos = 0;    // variable to store the servo position
boolean newInput = false;
String buffer;
String currMessage = "hello, world!";
String locationData[3];
const float SIGN_LAT = 42.293045;
const float SIGN_LONG = -71.264086;
const float R = 3959; // radius of Earth

 
void setup() 
{ 
  Serial.begin(9600);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object 
  myservo.write(0);
  float angle2 = LatLngtoAngle(SIGN_LAT + 10, SIGN_LONG);
  int intangle = angle2;
  myservo.write(intangle);
  lcd.begin(16, 2);
  lcd.print("Ready for Location");
}
 
 
void loop() 
{
  // Read the whole input before proceeding
  int i = 0;
  while (Serial.available()>0) {
    char ch = Serial.read();
    if (ch == '|') {
      i++;
    }
    else {
      locationData[i] += ch;
    }
    newInput = true;
    delay(2);
  }
  // If there's a new input, change the stuff
  if (newInput) {
    //displayNew(buffer, currMessage);
    //currMessage = buffer;
    newLocationData(locationData);
    newInput = false;
    buffer = "";
    locationData[0] = "";
    locationData[1] = "";
    locationData[2] = "";
  }
  
  
//  //Up
//  Serial.println("Up");
//  myservo.write(LatLngtoAngle(SIGN_LAT + 10, SIGN_LONG));
//  delay(1000);
//  // Left
//  Serial.println("Left");
//  myservo.write(LatLngtoAngle(SIGN_LAT, SIGN_LONG + 10));
//  delay(1000);
//  Serial.println("Down");
//  myservo.write(LatLngtoAngle(SIGN_LAT - 10, SIGN_LONG));
//  delay(1000);
//  Serial.println("Right");
//  myservo.write(LatLngtoAngle(SIGN_LAT, SIGN_LONG - 10));
//  delay(1000);
//  Serial.println("Germany");
//  myservo.write(LatLngtoAngle(51.091606, 10.736070));
//  delay(1000);
}

void newLocationData(String data[3]) {
  float lat = StringtoFloat(data[1]);
  float lng = StringtoFloat(data[2]);
  pointArrowAt(lat, lng);
    
  float dist = LatLngtoDist(lat, lng);
  displayPost(data[0], dist);
}

float StringtoFloat(String str) {
  char buff[256];
  str.toCharArray(buff,256);
  return atof(buff);
}

void pointArrowAt(float lat, float lng) {
  float angle = LatLngtoAngle(lat, lng);
  myservo.write(angle);
}

void displayPost(String name, float dist) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(name);
  lcd.setCursor(0, 1);
  lcd.print(dist);
  lcd.print(" miles");
}

void displayLocationData(String data[3]) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(data[0]);
  lcd.setCursor(0, 1);
  String latlng = data[1].substring(0,7) + ", " + data[2].substring(0,7);
  lcd.print(latlng);
}

float LatLngtoDist(float lat, float lng) {
  float latRad = degtoRad(lat);
  float lngRad = degtoRad(lng);
  float slatRad = degtoRad(SIGN_LAT);
  float slngRad = degtoRad(SIGN_LONG);
  float dlat = latRad - slatRad;
  float dlon = lngRad - slngRad;
  //return sqrt(sq(deltaLat) + sq(deltaLong));
  //dlon = lon2 - lon1 
  //dlat = lat2 - lat1   
  //float a = sq(sin(dlat/2)) + cos(slatRad) * cos(latRad) * sq(sin(dlon/2));
  float a = sq(sin(dlat/2)) + cos(slatRad) * cos(latRad) * sq(sin(dlon/2));
  float c = 2 * atan2( sqrt(a), sqrt(1-a) );
  return R * c; // where R is the radius of the Earth
}

float degtoRad(float deg) {
  return deg*(3.14/180);
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
          float temp = atanf(deltaLat/deltaLong);
          Serial.print("actual angle?: ");
          Serial.println(temp);
	  angleRad = 3.14 - temp;
          Serial.print("actual angle2?: ");
          Serial.println(angleRad);
        }
        //Serial.println(angleRad);
        float res = angleRad*(180/3.14)/2;
        if (res < 0) {
          res = res + 180;
        }
        Serial.print("Servo Angle: ");
        Serial.println(res);
	return res;
}
