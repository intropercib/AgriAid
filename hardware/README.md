# AgriAid (hardware) 🌱


## Overview

The **AgriAid** is an Arduino-based system designed for real-time agricultural monitoring and automation. It integrates multiple sensors to collect critical environmental data, enabling farmers to optimize plant growth and resource management. This repository contains the hardware component of the AgriAid system, including the Arduino sketch and circuit diagram.

---

## Table of Contents

1. [Key Features](#key-features)
2. [Components Used](#components-used)
3. [System Circuit Diagram](#system-circuit-diagram)
4. [Setup Instructions](#setup-instructions)
   - [Hardware Connections](#1-hardware-connections)
   - [Install Required Libraries](#2-install-required-libraries)
   - [Upload the Code](#3-upload-the-code)
   - [Monitor Sensor Data](#4-monitor-sensor-data)
5. [File Structure](#file-structure)
6. [Dependencies](#dependencies)
7. [Reference Links](#reference-links)

---

---

## Key Features

- **Real-Time Monitoring**:
  - Temperature and humidity (DHT11 sensor).
  - Soil moisture levels (Soil Moisture Sensor).
  - Air quality and CO2 levels (MQ135 Gas Sensor).
- **Automation**:
  - Water pump control via relay for irrigation.
  - Servo motor for mechanical actuation (e.g.,controlling water flow, could be used for opening/closing vents).
- **Visual Indicators**:
  - LED indicators for critical conditions (e.g., low soil moisture, high CO2 levels).
- **Serial Communication**:
  - Output sensor data to the Serial Monitor for debugging and analysis.

---

## Components Used

| Component                | Description                               |
| ------------------------ | ----------------------------------------- |
| **Arduino UNO**          | Microcontroller board for system control. |
| **DHT11 Sensor**         | Measures temperature and humidity.        |
| **Soil Moisture Sensor** | Detects soil moisture levels.             |
| **MQ135 Gas Sensor**     | Monitors air quality and CO2 levels.      |
| **LED Indicator**        | Visual feedback for system status.        |
| **Servo Motor**          | Mechanical actuation for automation.      |
| **Relay Module**         | Controls high-power devices (e.g., pump). |
| **12V DC Motor**         | Fan for ventilation.                      |

---

## System Circuit Diagram

Below is the circuit diagram for the AgriAid hardware component:
<img src="diagram/circuitDiagram.png" alt="Circuit Diagram" width="800"/>
![Circuit Diagram](diagram/circuitDiagram.png)

---

## Setup Instructions

### 1. **Hardware Connections**

Connect the sensors and components to the Arduino UNO as per the following pin configuration:

| Component                | Arduino Pin |
| ------------------------ | ----------- |
| **DHT11 Sensor**         | D4          |
| **Soil Moisture Sensor** | A1          |
| **MQ135 Gas Sensor**     | A0          |
| **Fan Control**          | D2          |
| **Servo Motor**          | D9          |
| **Built-in LED**         | D13         |

### 2. **Install Required Libraries**

Install the following libraries using the Arduino Library Manager or PlatformIO:

- **Adafruit DHT Sensor Library** (version ^1.4.6)
- **Adafruit Unified Sensor** (dependency for DHT library)
- **Servo** (version ^1.2.2)

### 3. **Upload the Code**

- Open the project in the Arduino IDE or PlatformIO.
- Upload the code to the Arduino UNO.

### 4. **Monitor Sensor Data**

- Open the Serial Monitor (`Ctrl+Shift+M` in Arduino IDE or `pio device monitor` in PlatformIO).
- Set the baud rate to `9600` to view real-time sensor data.

---

## File Structure

```
AgriAid_Hardware/
├── src/                      # Main Arduino sketch
│   └── main.ino
├── lib/                      # External libraries
├── diagrams/                 # Circuit diagrams
│   └── AgriAid_Circuit.png
├── README.md                 # Project documentation
└── platformio.ini            # PlatformIO configuration
```

---

## Dependencies

- **PlatformIO**: For building and uploading the code.
- **Libraries**:
  - Adafruit DHT Sensor Library (version ^1.4.6)
  - Adafruit Unified Sensor
  - Servo (version ^1.2.2)
- **Arduino Framework**: For running the code on Arduino boards.

---

## Reference Links

For detailed setup, testing, and implementation of the sensors and components, refer to the following resources:

- **Soil Moisture Sensor**: [Arduino Project Hub](https://projecthub.arduino.cc/Aswinth/soil-moisture-sensor-with-arduino-91c818)
- **DHT11 Sensor**: [Arduino Project Hub](https://projecthub.arduino.cc/arcaegecengiz/using-dht11-12f621)
- **MQ135 Gas Sensor**: [Circuit Digest](https://circuitdigest.com/microcontroller-projects/interfacing-mq2-gas-sensor-with-arduino)
- **Relay Module**: [Last Minute Engineers](https://lastminuteengineers.com/one-channel-relay-module-arduino-tutorial/)
- **Servo Motor**: [Arduino Documentation](https://docs.arduino.cc/tutorials/generic/basic-servo-control/)

---

🌱 **AgriAid - Empowering Agriculture with Technology** 🌱

---
