import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from typing import Tuple, List

class TomatoLeafClassifier:
    """A classifier for tomato leaf diseases using a trained deep learning model."""
    
    # Class labels should be a class variable since they're constant
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
            self.img_size = (224, 224)  # MobileNetV2 input size
        except Exception as e:
            raise ValueError(f"Failed to load model: {str(e)}")

    def preprocess_image(self, img_path: str) -> np.ndarray:
        """
        Preprocess an image for model prediction.
        
        Args:
            img_path (str): Path to the image file
            
        Returns:
            np.ndarray: Preprocessed image array
            
        Raises:
            FileNotFoundError: If image file doesn't exist
            ValueError: If image format is invalid
        """
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Image file not found: {img_path}")
            
        try:
            img = image.load_img(img_path, target_size=self.img_size)
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0  # Normalize
            return img_array
        except Exception as e:
            raise ValueError(f"Failed to process image: {str(e)}")

    def predict(self, img_path: str) -> Tuple[str, float, dict]:
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
            img_array = self.preprocess_image(img_path)
            predictions = self.model.predict(img_array, verbose=0)
            
            # Get the predicted class and confidence
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx] * 100)
            
            # Create probability dictionary for all classes
            class_probabilities = {
                class_name: float(prob * 100)
                for class_name, prob in zip(self.CLASS_LABELS, predictions[0])
            }
            
            return self.CLASS_LABELS[predicted_class_idx], confidence, class_probabilities
            
        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")

    def batch_predict(self, image_dir: str) -> List[Tuple[str, str, float]]:
        """
        Predict disease classes for all images in a directory.
        
        Args:
            image_dir (str): Directory containing image files
            
        Returns:
            List[Tuple[str, str, float]]: List of (image_name, predicted_class, confidence) tuples
        """
        results = []
        valid_extensions = {'.jpg', '.jpeg', '.png'}
        
        for img_name in os.listdir(image_dir):
            if any(img_name.lower().endswith(ext) for ext in valid_extensions):
                img_path = os.path.join(image_dir, img_name)
                try:
                    predicted_class, confidence, _ = self.predict(img_path)
                    results.append((img_name, predicted_class, confidence))
                except Exception as e:
                    print(f"Failed to process {img_name}: {str(e)}")
                    
        return results

# test
def main():
    try:
        # Initialize classifier
        classifier = TomatoLeafClassifier('model.h5')
        
        # Test single image
        test_image = 'images/Tomato___Bacterial_spot/07458546-6893-49c8-b94f-edde706b19fa___GCREC_Bact.Sp 3835.JPG'
        # test_image = 'images/Tomato___Bacterial_spot/086880d1-73c4-40d3-99ea-d446c2299692___GCREC_Bact.Sp 3333.JPG'
        # test_image = 'images/Tomato___Early_blight/089243e5-f319-4ed2-b10c-603328ff4143___RS_Erly.B 9428.JPG'
        # test_image = 'images/Tomato___Healthy/05598cc1-60b9-4436-a233-973c42eff2d6___GH_HL Leaf 503.1.JPG'


        predicted_class, confidence, class_probs = classifier.predict(test_image)
        print(f"\nSingle Image Prediction:")
        print(f"Predicted Class: {predicted_class}")
        print(f"Confidence: {confidence:.2f}%")
        
        # Print top 3 predictions
        top_3 = sorted(class_probs.items(), key=lambda x: x[1], reverse=True)[:3]
        print("\nTop 3 Predictions:")
        for class_name, prob in top_3:
            print(f"{class_name}: {prob:.2f}%")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()