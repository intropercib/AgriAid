#include <Arduino.h>
#include <Adafruit_Sensor.h> // Library for sensor compatibility
#include <DHT.h>             // Library for DHT temperature and humidity sensor
#include <Servo.h>           // Library for servo motor control

// Pin definitions
#define DHT_PIN 4            // Digital pin connected to the DHT sensor
#define DHT_TYPE DHT11       // DHT sensor type (DHT11 or DHT22)
#define mq135Pin A0          // Analog pin connected to the MQ-135 gas sensor
#define moisture_sensor_pin A1 // Analog pin connected to the soil moisture sensor
#define fan_pin 2            // Digital pin connected to the fan
#define servo_pin 9          // Digital pin connected to the servo motor

// Create instances
DHT dht(DHT_PIN, DHT_TYPE);  // Initialize DHT sensor
Servo myservo;               // Initialize servo motor

// Variables for servo control
unsigned long servoMoveTime = 0; // Timestamp when the servo was last moved
bool servoMoved = false;         // Flag to track if the servo has moved

void setup()
{
    // Initialize serial communication for debugging
    Serial.begin(9600);

    // Initialize DHT sensor
    dht.begin();

    // Set pin modes
    pinMode(13, OUTPUT);       // Built-in LED (optional for debugging)
    pinMode(fan_pin, OUTPUT);  // Fan control pin
    myservo.attach(servo_pin); // Attach servo to the specified pin
    myservo.write(90);         // Initialize servo to 90 degrees (neutral position)
    delay(1000);               // Wait for serial monitor to initialize
}

/**
 * Reads and prints temperature and humidity values from the DHT sensor.
 */
void getDHT_value()
{
    // Read humidity and temperature from the DHT sensor
    int humidity = dht.readHumidity();
    int temperature = dht.readTemperature();

    // Print temperature and humidity values to the Serial Monitor
    Serial.print("Temperature: ");
    Serial.println(temperature);
    Serial.print("Humidity: ");
    Serial.println(humidity);
}

/**
 * Reads and prints CO2 concentration from the MQ-135 sensor.
 * Controls the fan based on CO2 levels.
 */
void getMQ135_value()
{
    // Read the analog value from the MQ-135 sensor
    float sensorValue = analogRead(mq135Pin);

    // Convert the analog reading to a voltage (0-5V range)
    float voltage = sensorValue * (5.0 / 1023.0);

    // Estimate CO2 concentration (calibrate for accuracy)
    float co2Concentration = voltage * 1000;

    // Control the fan based on CO2 concentration
    if (co2Concentration < 800)
    {
        digitalWrite(fan_pin, HIGH); // Turn on the fan if CO2 is below 800 ppm
    }
    else
    {
        digitalWrite(fan_pin, LOW); // Turn off the fan if CO2 is above 800 ppm
    }

    // Print CO2 concentration to the Serial Monitor
    Serial.print("CO2: ");
    Serial.println(co2Concentration);
}

/**
 * Reads and prints soil moisture percentage from the moisture sensor.
 * Controls the servo motor based on moisture levels.
 */
void getMoisture_value()
{
    // Read the analog value from the soil moisture sensor
    int sensor_analog = analogRead(moisture_sensor_pin);

    // Convert the analog value to a moisture percentage
    float moisture_percentage = (100 - ((sensor_analog / 1023.00) * 100));

    // Print moisture percentage to the Serial Monitor
    Serial.print("Moisture: ");
    Serial.println(moisture_percentage);

    // Check if the moisture level is below 20%
    if (moisture_percentage <= 20)
    {
        if (!servoMoved) // Only move the servo if it hasn't already moved
        {
            myservo.write(180);        // Move servo to 180 degrees (e.g., open valve)
            servoMoveTime = millis(); // Record the time when the servo moved
            servoMoved = true;        // Set the flag to indicate the servo has moved
        }
    }
    else
    {
        myservo.write(90);   // Return servo to 90 degrees (neutral position)
        servoMoved = false; // Reset the flag
    }

    // Check if the servo has been at 180 degrees for 3 seconds
    if (servoMoved && (millis() - servoMoveTime >= 3000))
    {
        myservo.write(90);   // Return the servo to 90 degrees
        servoMoved = false; // Reset the flag
    }
}

void loop()
{
    // Read and print DHT sensor values (temperature and humidity)
    getDHT_value();

    // Read and print soil moisture sensor values
    getMoisture_value();

    // Read and print MQ-135 sensor values (CO2 concentration)
    getMQ135_value();

    delay(3000); // Wait for 3 seconds before the next reading
}