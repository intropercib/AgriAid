#include <Arduino.h>

void setup()
{
    Serial.begin(9600); 
}

void loop()
{
    int randomValue = random(0, 100); 
    String key = "randomValue";
    Serial.print(key);
    Serial.print(": ");
    Serial.println(randomValue);
    delay(1000); 
}