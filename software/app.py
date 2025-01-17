from flask import Flask, render_template, Response
from video_processor import VideoProcessor
from sensor_data import SensorData

app = Flask(__name__)

# Initialize classes for video processing and sensor data
video_processor = VideoProcessor(video_url="http://192.168.18.7:8080/video")
sensor_data = SensorData(port='COM5') 

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Route for the live video feed."""
    return Response(video_processor.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/sensor_data')
def get_sensor_data():
    """Route to fetch the latest sensor data."""
    data = sensor_data.get_latest_data()
    print(f"Sending data to frontend: {data}") 
    return data

if __name__ == '__main__':
    app.run(debug=True)