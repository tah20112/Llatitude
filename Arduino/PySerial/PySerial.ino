int num;
boolean newBuffer = false;
String buffer;
String lat;
String lon;

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
    lat = getSubString(buffer, ':', 0);
    lon = getSubString(buffer, ':', 1);
    char carray[lat.length() + 1];
    lat.toCharArray(carray, sizeof(carray));
    float latVal = atof(carray);
    char carray2[lat.length() + 1];
    lat.toCharArray(carray2, sizeof(carray));
    float lonVal = atof(carray2);
    Serial.println(latVal);
    Serial.println(lonVal);
    num = buffer.toInt();
    newBuffer = false;
    buffer = "";
  }
}

String getSubString(String data, char separator, int index)
{
 int found = 0;
  int strIndex[] = {
0, -1  };
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
