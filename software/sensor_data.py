import serial
import json
import time
import serial
import json
import time

class SensorData:
    def __init__(self, port='COM5', baudrate=9600, timeout=1, retry_attempts=3):
        """
        Initialize the serial connection to the Arduino.
        :param port: Serial port (e.g., '/dev/ttyUSB0' for Linux or 'COM3' for Windows)
        :param baudrate: Baud rate for serial communication (default: 9600)
        :param timeout: Timeout for serial communication (default: 1 second)
        :param retry_attempts: Number of times to retry connection if it fails
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.serial_conn = None
        self.connect()

    def connect(self):
        """Establish a connection to the Arduino."""
        for attempt in range(1, self.retry_attempts + 1):
            try:
                print(f"Attempt {attempt}: Connecting to {self.port}...")
                self.serial_conn = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    timeout=self.timeout,
                )
                time.sleep(2) 
                self.serial_conn.reset_input_buffer()
                self.serial_conn.reset_output_buffer()
                print(f"Connected to Arduino on {self.port}")
                return
            except Exception as e:
                print(f"Failed to connect on attempt {attempt}: {e}")
                if attempt < self.retry_attempts:
                    print("Retrying in 5 seconds...")
                    time.sleep(5)
        print("Exceeded maximum retry attempts. Connection failed.")
        self.serial_conn = None

    def get_latest_data(self):
        """
        Read data from the Arduino via serial communication.
        :return: JSON string containing sensor data or error message.
        """
        if not self.serial_conn:
            return json.dumps({"error": "Serial connection not established"})

        try:
            if self.serial_conn.in_waiting > 0:
                line = self.serial_conn.readline().decode('utf-8').strip()
                print(f"Received raw data: {line}") 

                if ": " in line:
                    key, value = line.split(": ")
                    try:
                        value = int(value)  
                        json_data = {"key": key, "value": value}
                        print(f"Parsed data: {json_data}")
                        return json.dumps(json_data)
                    except ValueError:
                        return json.dumps({"error": "Invalid value format"})
                else:
                    return json.dumps({"error": "Invalid data format"})
            else:
                return json.dumps({"error": "No data available"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def close(self):
        """Close the serial connection."""
        if self.serial_conn:
            self.serial_conn.close()
            print("Serial connection closed")

sensor_data = SensorData(port='COM5')  
sensor_data.connect()
try:
    while True:
        data = sensor_data.get_latest_data()
        print(data)
        time.sleep(1)
except KeyboardInterrupt:
    sensor_data.close()
