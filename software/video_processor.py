import cv2
import numpy as np
from models.classifier import TomatoLeafClassifier  

class VideoProcessor:
    def __init__(self, video_url: str, model_path: str, prediction_interval: int = 15):
        """
        Initialize the VideoProcessor class with the given parameters.

        Args:
            video_url (str): URL or file path of the video source.
            model_path (str): Path to the trained model file.
            prediction_interval (int): The number of frames to skip between predictions. Default is 15.
        
        Raises:
            Exception: If the video source cannot be opened.
        """
        self.classifier = TomatoLeafClassifier(model_path)  
        self.video_url = video_url
        self.cap = cv2.VideoCapture(self.video_url) 
        self.frame_width, self.frame_height = 880, 500
        self.prediction_interval = prediction_interval
        self.frame_counter = 0
        # self.last_prediction = None
        self.last_prediction_updated_at = 0
        self.predictions = {}
        self.contours = [
            (50, 80), 
            (550, 80),
        ]
        self.contour_size = (300, 300) 

        if not self.cap.isOpened():
            raise Exception("Failed to open video source.")

    def generate_frames(self):
        """
        Generate frames with plant detection and health status.

        This method continuously reads frames from the video source, processes them to detect plants,
        and yields the processed frames in byte format for streaming.

        Yields:
            bytes: Processed frames in byte format, suitable for streaming over HTTP.

        Raises:
            Exception: If an error occurs while processing a frame.
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
        Detect plants in the frame and draw contours with health status.

        This method processes the input frame to detect plants within predefined regions of interest (ROIs).
        It uses the classifier to predict the health status of the plants and draws bounding boxes and labels
        on the frame.

        Args:
            frame (np.ndarray): Input frame from the video feed.

        Returns:
            np.ndarray: Processed frame with contours and health status labels.

        Raises:
            Exception: If an error occurs during prediction or frame processing.
        """
        self.frame_counter += 1
        
        if self.frame_counter - self.last_prediction_updated_at >= self.prediction_interval:
            for i, (x, y) in enumerate(self.contours):
                w, h = self.contour_size
                roi = frame[y:y + h, x:x + w]

                try:
                    predicted_class, confidence, _ = self.classifier.predict(roi)
                    # self.last_prediction = (predicted_class, confidence)
                    self.predictions[i] = (predicted_class, confidence)
                    self.prediction_updated_at = self.frame_counter 
                except Exception as e:
                    print(f"Prediction failed for ROI at ({x}, {y}): {str(e)}")

        # if self.last_prediction:
        # predicted_class, confidence = self.last_prediction
        for i, (x, y) in enumerate(self.contours):
            if i in self.predictions:
                w, h = self.contour_size
                predicted_class, confidence = self.predictions[i]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                label = f"{predicted_class}: {confidence:.2f}%"
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        return frame

    def __del__(self):
        """
        Release the video capture object when the class is destroyed.

        This method ensures that the video capture object is properly released when the VideoProcessor
        instance is destroyed, freeing up resources.
        """
        if self.cap and self.cap.isOpened():
            self.cap.release()