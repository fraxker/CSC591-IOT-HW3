int potPin = 2;
int potVal;

void setup() {
    Serial.begin(115200);
    Serial.setTimeout(1);
}

void loop() {
    while (!Serial.available());

    potVal = analogRead(potPin); //reads the analogue voltage from the pot via ADC and stores it in the variable

    Serial.print(potVal)

    delay(100); //waits an amount of time dependent on the potentiometer position

}