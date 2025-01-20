#include <Arduino.h>
#include <Adafruit_Sensor.h> // For sensor
#include <DHT.h>             // For temperature and humidity sensor

// Pin definitions
#define DHT_PIN 7
#define DHT_TYPE DHT11 // or DHT22 depending on your sensor
#define moisture_sensor_pin A1
#define mq135Pin A3 // Analog pin where MQ-135 is connected

// Create instances
DHT dht(DHT_PIN, DHT_TYPE);

void setup()
{
    // Initialize serial communication
    Serial.begin(9600);
    dht.begin();
    pinMode(13, OUTPUT);
    delay(1000); // Wait for serial monitor to initialize
}

void getDHT_value()
{
    int humidity = dht.readHumidity();
    int temperature = dht.readTemperature();

    // Send temperature and humidity data in the format "key: value"
    Serial.print("Temperature: ");
    Serial.println(temperature);
    Serial.print("Humidity: ");
    Serial.println(humidity);

    // Example action: Turn on LED if temperature > 20 or humidity > 60
    if (temperature > 20 || humidity > 60)
    {
        digitalWrite(13, HIGH);
    }
    else
    {
        digitalWrite(13, LOW);
    }
}

void getMQ135_value()
{
    float sensorValue = analogRead(mq135Pin); // Read the analog value from the MQ135 sensor
    float voltage = sensorValue * (5.0 / 1023.0); // Convert the analog reading to a voltage (0-5V range)
    float co2Concentration = voltage * 100; // Estimate CO2 concentration (calibrate for accuracy)

    // Send CO2 concentration data in the format "key: value"
    Serial.print("CO2: ");
    Serial.println(co2Concentration);
}

void getMoisture_value()
{
    int sensor_analog = analogRead(moisture_sensor_pin); // Read the analog value from the moisture sensor
    float moisture_percentage = (100 - ((sensor_analog / 1023.00) * 100)); // Convert to percentage

    // Send moisture data in the format "key: value"
    Serial.print("Moisture: ");
    Serial.println(moisture_percentage);
}

void loop()
{
    // Read and send DHT11 values
    getDHT_value();

    // Read and send soil moisture sensor values
    getMoisture_value();

    // Read and send MQ135 sensor values
    getMQ135_value();

    delay(1000); // Wait for 1 second before the next reading
}