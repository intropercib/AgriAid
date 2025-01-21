import cv2
import numpy as np
from models.classifier import TomatoLeafClassifier  

class VideoProcessor:
    def __init__(self, video_url: str, model_path: str, prediction_interval: int = 50):
        """
        Initializes the VideoProcessor with video source, model, and prediction interval.

        Args:
            video_url (str): URL or file path of the video source.
            model_path (str): Path to the trained model file.
            prediction_interval (int): Frames to skip between predictions. Default is 50.

        Raises:
            Exception: If the video source cannot be opened.
        """
        self.classifier = TomatoLeafClassifier(model_path)  
        self.video_url = video_url
        self.cap = cv2.VideoCapture(self.video_url) 
        self.frame_width, self.frame_height = 880, 500
        self.prediction_interval = prediction_interval
        self.frame_counter = 0
        self.last_prediction_updated_at = 0
        self.predictions = {}
        self.contours = [(50, 80), (550, 80)]  # ROI coordinates
        self.contour_size = (300, 300)  # ROI size

        if not self.cap.isOpened():
            raise Exception("Failed to open video source.")

    def generate_frames(self):
        """
        Yields processed frames with plant detection and health status for streaming.

        Yields:
            bytes: Processed frames in byte format for HTTP streaming.

        Raises:
            Exception: If frame processing fails.
        """
        while True:
            success, frame = self.cap.read()
            if not success:
                continue

            frame = cv2.resize(frame, (self.frame_width, self.frame_height))

            try:
                processed_frame = self.detect_plants(frame)
            except Exception as e:
                print(f"Error processing frame: {e}")
                continue

            ret, buffer = cv2.imencode('.jpg', processed_frame)
            if not ret:
                print("Failed to encode frame.")
                continue

            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    

    def detect_plants(self, frame: np.ndarray) -> np.ndarray:
        """
        Detects plants in ROIs, predicts health status, and draws bounding boxes.

        Args:
            frame (np.ndarray): Input frame from the video feed.

        Returns:
            np.ndarray: Frame with contours and health status labels.

        Raises:
            Exception: If prediction or frame processing fails.
        """
        self.frame_counter += 1
        
        if self.frame_counter - self.last_prediction_updated_at >= self.prediction_interval:
            for i, (x, y) in enumerate(self.contours):
                w, h = self.contour_size
                roi = frame[y:y + h, x:x + w]

                try:
                    predicted_class, confidence, _ = self.classifier.predict(roi)
                    self.predictions[i] = (predicted_class, confidence)
                    self.last_prediction_updated_at = self.frame_counter 
                except Exception as e:
                    print(f"Prediction failed for ROI at ({x}, {y}): {str(e)}")

        for i, (x, y) in enumerate(self.contours):
            if i in self.predictions:
                w, h = self.contour_size
                predicted_class, confidence = self.predictions[i]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                label = f"{predicted_class}: {confidence:.2f}%"
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        return frame

    def __del__(self):
        """Releases the video capture object when the instance is destroyed."""
        if self.cap and self.cap.isOpened():
            self.cap.release()