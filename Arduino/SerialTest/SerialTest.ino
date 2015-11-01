void setup() {
  Serial.begin(9600);
  Serial.print("Serial up and running");

}

void loop() {
  Serial.print("Serial still running");
  delay(500);
}
