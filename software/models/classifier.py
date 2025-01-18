import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import cv2
import numpy as np
import os
from typing import Tuple, List

class TomatoLeafClassifier:
    """A classifier for tomato leaf diseases using a trained deep learning model."""
    
    # Class labels as in model training
    CLASS_LABELS = [
        'Tomato___Bacterial_spot',
        'Tomato___Early_blight',
        'Tomato___Healthy',
        'Tomato___Late_blight',
        'Tomato___Leaf_Mold',
        'Tomato___Septoria_leaf_spot',
        'Tomato___Spider_mites Two-spotted_spider_mite',
        'Tomato___Target_Spot',
        'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
        'Tomato___Tomato_mosaic_virus'
    ]

    def __init__(self, model_path: str):
        """
        Initialize the classifier with a trained model.
        
        Args:
            model_path (str): Path to the saved model file (.h5 format)
        
        Raises:
            FileNotFoundError: If model file doesn't exist
            ValueError: If model file is invalid
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
            
        try:
            self.model = load_model(model_path)
            self.img_size = (224, 224) 
        except Exception as e:
            raise ValueError(f"Failed to load model: {str(e)}")

    def preprocess_image(self, img_array: np.ndarray) -> np.ndarray:
        """
        Preprocess an image for model prediction.
        
        Args:
            img_array (np.ndarray) : img_array
            
        Returns:
            np.ndarray: Preprocessed image array
            
        Raises:
            FileNotFoundError: If image file doesn't exist
            ValueError: If image format is invalid
        """
        img_array = cv2.resize(img_array, self.img_size)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        return img_array

    def predict(self, img_array: np.ndarray) -> Tuple[str, float, dict]:
        """
        Predict the disease class and confidence for a tomato leaf image.
        
        Args:
            img_path (str): Path to the image file
            
        Returns:
            Tuple[str, float, dict]: Predicted class, confidence percentage, and all class probabilities
            
        Raises:
            Exception: If prediction fails
        """
        try:
            img_array = self.preprocess_image(img_array)
            predictions = self.model.predict(img_array, verbose=0)
            
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx] * 100)
            
            class_probabilities = {
                class_name: float(prob * 100)
                for class_name, prob in zip(self.CLASS_LABELS, predictions[0])
            }
            
            return self.CLASS_LABELS[predicted_class_idx], confidence, class_probabilities
            
        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")
