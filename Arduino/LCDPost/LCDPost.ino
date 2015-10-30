/*
  The circuit:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * LCD VSS pin to ground
 * LCD VCC pin to 5V
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)

 Library originally added 18 Apr 2008
 by David A. Mellis
 library modified 5 Jul 2009
 by Limor Fried (http://www.ladyada.net)
 example added 9 Jul 2009
 by Tom Igoe
 modified 22 Nov 2010
 by Tom Igoe

 This example code is in the public domain.

 http://www.arduino.cc/en/Tutorial/LiquidCrystal
 */

// include the library code:
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

boolean newInput = false;
String buffer;
String currMessage = "hello, world!";

void setup() {
  Serial.begin(9600);
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print(currMessage);
}

void loop() {
  while (Serial.available()>0) {
    char ch = Serial.read();
    buffer += ch;
    newInput = true;
    delay(2);
  }
  // If there's a new input, change the stuff
  if (newInput) {
    displayNew(buffer, currMessage);
    currMessage = buffer;
    newInput = false;
    buffer = "";
  }
}

void displayNew(String newMessage, String oldMessage) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(newMessage);
  lcd.setCursor(0, 1);
  lcd.print(oldMessage);
}
