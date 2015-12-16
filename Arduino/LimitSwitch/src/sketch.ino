byte lim_switch;
byte button;

void setup()
{
    Serial.begin(9600);
    pinMode(6, INPUT_PULLUP);
    pinMode(2, INPUT);
}

void loop()
{
    lim_switch = digitalRead(6);
    button = digitalRead(2);
    Serial.print("Switch: ");
    Serial.print(lim_switch);
    Serial.print(" Button: ");
    Serial.println(button);
}
