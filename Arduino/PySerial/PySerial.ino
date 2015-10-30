int DELAY = 1000;
boolean newBuffer = false;
String buffer;

void setup() {
  Serial.begin(9600);
}
void loop() {
  while (Serial.available()>0) {
    char ch = Serial.read();
    buffer += ch;
    newBuffer = true;
    delay(2);
  }
  // If there's a new input, change the stuff
  if (newBuffer) {
    DELAY = buffer.toInt();
    newBuffer = false;
    buffer = "";
  }
  Serial.println("I blinked");
  delay(DELAY);
}
