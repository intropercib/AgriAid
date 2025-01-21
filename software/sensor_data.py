import serial
import json
import time

class SensorData:
    def __init__(self, port, baudrate, timeout):
        """
        Initializes the SensorData class with serial connection parameters.

        Args:
            port (str): Serial port to which the Arduino is connected (e.g., 'COM5').
            baudrate (int): Baud rate for serial communication (e.g., 9600).
            timeout (int): Timeout for serial communication in seconds.
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.connect()

    def connect(self):
        """
        Establishes a serial connection to the Arduino.

        Raises:
            Exception: If the serial connection cannot be established.
        """
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
            )
            print(f"Connected to Arduino on {self.port}" if self.serial_conn else f"Failed to connect to Arduino on {self.port}")
        except Exception as e:
            print(f"Error connecting to {self.port}: {e}")
            self.serial_conn = None

    def get_latest_data(self):
        """
        Reads and parses the latest data from the Arduino.

        Returns:
            str: JSON string containing parsed data or an error message.
                 Example: {"Temperature": 25, "Humidity": 60} or {"error": "No data available"}.

        Raises:
            serial.SerialException: If there is an issue with the serial port.
            Exception: If any other error occurs during data reading or parsing.
        """
        if not self.serial_conn:
            return json.dumps({"error": "Serial connection not established"})

        try:
            time.sleep(0.1)
            if self.serial_conn.in_waiting > 0:
                data = {}
                while self.serial_conn.in_waiting > 0:
                    line = self.serial_conn.readline().decode('utf-8').strip()
                    if ": " in line:
                        key, value = line.split(": ")
                        try:
                            data[key] = float(value)
                        except ValueError:
                            print(f"Invalid value format: {line}")
                return json.dumps(data) if data else json.dumps({"error": "No valid data available"})
            else:
                return json.dumps({"error": "No data available"})
        except serial.SerialException as e:
            return json.dumps({"error": f"Serial port error: {str(e)}"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def close(self):
        """Closes the serial connection to the Arduino."""
        if self.serial_conn:
            self.serial_conn.close()
            print("Serial connection closed")