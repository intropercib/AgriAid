import cv2
import numpy as np
from models.classifier import TomatoLeafClassifier  

class VideoProcessor:
    def __init__(self, video_url):
        """
        Initialize the video processor.
        :param video_url: URL or file path of the video.
        """
        self.classifier = TomatoLeafClassifier('models/model.h5')  
        self.video_url = video_url
        self.cap = cv2.VideoCapture(self.video_url) 
        # contours position
        self.contours = [
            (250, 250), 
            (1150, 250),
        ]
        self.contour_size = (500, 500)  # Size of the contour box

    def generate_frames(self):
        """Generate frames with plant detection and health status."""
        while True:
            success, frame = self.cap.read()
            if not success:
                break

            # Process the frame for plant detection
            processed_frame = self.detect_plants(frame)

            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            if not ret:
                break

            # Yield the frame in byte format
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def detect_plants(self, frame):
        """
        Detect plants in the frame and draw contours with health status.
        :param frame: Input frame from the video feed.
        :return: Processed frame with contours and health status.
        """
        for i, (x, y) in enumerate(self.contours):
            w, h = self.contour_size

            # Extract the ROI from the frame
            roi = frame[y:y + h, x:x + w]

            # Preprocess the ROI as required by TomatoLeafClassifier
            # roi_path = f'temp_roi_{i}.jpg'
            # cv2.imwrite(roi_path, roi)
            
            predicted_class, confidence, _ = self.classifier.predict(roi)
            health_status = f"{predicted_class} ({confidence:.2f}%)"

            # Draw the bounding box and health status on the frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  
            cv2.putText(frame, f"{health_status} {i + 1}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)  

        return frame

    def __del__(self):
        """Release the video capture object when the class is destroyed."""
        if self.cap and self.cap.isOpened():
            self.cap.release()