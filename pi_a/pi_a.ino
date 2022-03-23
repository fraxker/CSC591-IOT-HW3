int potPin = 2;
int potVal;
float convertedVal;

void setup() {
    SerialUSB.begin(115200);
    SerialUSB.setTimeout(1);
}

void loop() {
    potVal = analogRead(potPin); //reads the analogue voltage from the pot via ADC and stores it in the variable
    convertedVal = float(potVal) / 1024; 
    SerialUSB.println(convertedVal);

    delay(100);
}
