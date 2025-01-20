import serial
import json
import time

class SensorData:
    def __init__(self, port, baudrate, timeout):
        """
        Initialize the SensorData class with serial connection parameters.

        Args:
            port (str): The serial port to which the Arduino is connected (e.g., 'COM5').
            baudrate (int): The baud rate for serial communication (e.g., 9600).
            timeout (int): The timeout for serial communication in seconds.
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.connect()

    def connect(self):
        """
        Establish a serial connection to the Arduino.

        This method attempts to open a serial connection to the Arduino using the specified
        port, baud rate, and timeout. If the connection is successful, it sets the
        `serial_conn` attribute. If the connection fails, it logs an error and sets
        `serial_conn` to None.

        Raises:
            Exception: If the serial connection cannot be established.
        """
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
            )
            if self.serial_conn:
                print(f"Connected to Arduino on {self.port}")
            else:
                print(f"Failed to connect to Arduino on {self.port}")
                self.serial_conn = None
        except Exception as e:
            print(f"Error connecting to {self.port}: {e}")
            self.serial_conn = None

    def get_latest_data(self):
        """
        Read the latest data from the Arduino via serial communication.

        This method reads all available lines from the serial port, parses them, and returns
        the data as a single JSON object. If no data is available or the data is invalid,
        an error message is returned.

        Returns:
            str: A JSON string containing the parsed data or an error message.
                  Example: {"Temperature": 25, "Humidity": 60, "CO2": 400, "Moisture": 50}
                           or {"error": "No data available"}.

        Raises:
            serial.SerialException: If there is an issue with the serial port.
            Exception: If any other error occurs during data reading or parsing.
        """
        if not self.serial_conn:
            return json.dumps({"error": "Serial connection not established"})

        try:
            time.sleep(0.1)  # Add a small delay to allow data to arrive
            if self.serial_conn.in_waiting > 0:
                data = {}
                while self.serial_conn.in_waiting > 0:
                    line = self.serial_conn.readline().decode('utf-8').strip()
                    print(f"Received raw data: {line}")
                    if ": " in line:
                        key, value = line.split(": ")
                        try:
                            value = float(value)  # Convert value to float
                            data[key] = value
                        except ValueError:
                            print(f"Invalid value format: {line}")
                if data:
                    return json.dumps(data)
                else:
                    return json.dumps({"error": "No valid data available"})
            else:
                return json.dumps({"error": "No data available"})
        except serial.SerialException as e:
            return json.dumps({"error": f"Serial port error: {str(e)}"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def close(self):
        """
        Close the serial connection to the Arduino.

        This method closes the serial connection if it is open and sets the `serial_conn`
        attribute to None. It also logs a message indicating that the connection has been closed.
        """
        if self.serial_conn:
            self.serial_conn.close()
            print("Serial connection closed")