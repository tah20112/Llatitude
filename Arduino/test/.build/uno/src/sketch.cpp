#include <Arduino.h>

void setup();
void loop();
void test();
#line 1 "src/sketch.ino"

volatile int val;

void setup()
{
    Serial.begin(9600);
    attachInterrupt(digitalPinToInterrupt(2), test, RISING);
}

void loop()
{
    noInterrupts();
    interrupts();
}

void test(){
    val = digitalRead(2);
    Serial.println(val);
}
