from flask import Flask, render_template, Response
from video_processor import VideoProcessor
from sensor_data import SensorData

app = Flask(__name__)

# Initialize classes for video processing and sensor data
video_processor = VideoProcessor(video_url="http://192.168.18.7:8080/video", model_path="models/model.h5")
sensor_data = SensorData(port='COM5', baudrate=9600, timeout=1) 

def generate_video_feed():
    for frame in video_processor.generate_frames():
        yield frame

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/cure')
def cure():
    """Route for the cure page."""
    return render_template('cure.html')

@app.route('/video_feed')
def video_feed():
    """Route for the live video feed."""
    print("Accessing video feed...")
    return Response(generate_video_feed(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/sensor_data')
def get_sensor_data():
    """Route to fetch the latest sensor data."""
    data = sensor_data.get_latest_data()
    print(f"Sending data to frontend: {data}") 
    return data

if __name__ == '__main__':

    app.run(debug=False)