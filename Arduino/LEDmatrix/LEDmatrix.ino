
#include <Adafruit_GFX.h>   // Core graphics library
#include <RGBmatrixPanel.h> // Hardware-specific library

#define CLK 8
#define LAT A3
#define OE  9
#define A   A0
#define B   A1
#define C   A2
RGBmatrixPanel matrix(A, B, C, CLK, LAT, OE, false);

byte counter;
boolean newBuffer = false;
String buffer;  // string built from serial
String place; // strings for Python input
String distance;
String angle;

void setup() {
  Serial.begin(9600);
  matrix.begin();
  matrix.setTextWrap(false); // Allow text to run off right edge
  matrix.setTextSize(1);    // size 1 == 8 pixels high

// print first line to say "Ready"
  matrix.setTextColor(matrix.Color333(3,3,6)); // set text color (R,G,B)
  matrix.print("Ready");  // print a string
  // matrix.print() statements used in succession print inline

//print next line to say "To Go"
  matrix.setCursor(1, 9);   // next line  
  matrix.setTextColor(matrix.Color333(3,0,3));
  matrix.print("To Go");
}

void loop() {
  matrix.setTextColor(matrix.Color333(2,0,4)); // set text color
  // while Python is sending over Serial, append characters to buffer
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
    
    char carray[angle.length() + 1];
    angle.toCharArray(carray, sizeof(carray));
    float angleVal = atof(carray);

    // fill the screen with 'black'
    matrix.fillScreen(matrix.Color333(0, 0, 0));
    matrix.setCursor(1,0); // return cursor to first row
    matrix.setTextColor(matrix.Color333(3,3,6));
    matrix.print(place);
    matrix.setCursor(1,9);
    matrix.setTextColor(matrix.Color333(3,0,3));
    matrix.print(distance);
    matrix.print(" mi");
    newBuffer = false;
    buffer = "";
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
