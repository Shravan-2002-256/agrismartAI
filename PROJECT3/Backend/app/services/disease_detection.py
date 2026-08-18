"""
Disease Detection Service using Deep Learning
"""
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import logging
from typing import Tuple, Dict
import os

from app.core.config import settings

logger = logging.getLogger(__name__)

# Disease class names (PlantVillage dataset)
DISEASE_CLASSES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

class DiseaseDetectionService:
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.load_model()
    
    def load_model(self):
        """Load the trained model"""
        try:
            model_path = settings.MODEL_PATH
            
            if os.path.exists(model_path):
                self.model = tf.keras.models.load_model(model_path)
                self.model_loaded = True
                logger.info(f"Disease detection model loaded from {model_path}")
            else:
                logger.warning(f"Model file not found at {model_path}. Using dummy predictions.")
                self.model_loaded = False
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model_loaded = False
    
    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """Preprocess image for model input"""
        # Open image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to model input size
        image = image.resize((settings.MODEL_INPUT_SIZE, settings.MODEL_INPUT_SIZE))
        
        # Convert to array and normalize
        image_array = np.array(image)
        image_array = image_array / 255.0  # Normalize to [0, 1]
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    
    def predict(self, image_bytes: bytes) -> Tuple[str, float, int]:
        """
        Predict disease from image
        Returns: (disease_name, confidence, class_index)
        """
        # Preprocess image
        processed_image = self.preprocess_image(image_bytes)
        
        if self.model_loaded and self.model is not None:
            # Make prediction
            predictions = self.model.predict(processed_image)
            
            # Get class with highest probability
            class_index = np.argmax(predictions[0])
            confidence = float(predictions[0][class_index])
            
            disease_name = DISEASE_CLASSES[class_index]
        else:
            # Dummy prediction for testing
            logger.warning("Using dummy prediction - model not loaded")
            class_index = 0
            confidence = 0.85
            disease_name = DISEASE_CLASSES[0]
        
        return disease_name, confidence, class_index
    
    def get_severity(self, disease_name: str, confidence: float) -> str:
        """Determine disease severity"""
        if "healthy" in disease_name.lower():
            return "none"
        elif confidence >= 0.9:
            return "high"
        elif confidence >= 0.75:
            return "medium"
        else:
            return "low"
    
    def get_recommendations(self, disease_name: str) -> list:
        """Get treatment recommendations for detected disease"""
        # Knowledge base of recommendations
        recommendations_db = {
            "Apple___Apple_scab": [
                {"type": "organic", "treatment": "Apply sulfur-based fungicides"},
                {"type": "chemical", "treatment": "Use Captan or Mancozeb"},
                {"type": "prevention", "treatment": "Remove fallen leaves and improve air circulation"}
            ],
            "Tomato___Early_blight": [
                {"type": "organic", "treatment": "Apply copper-based fungicides"},
                {"type": "chemical", "treatment": "Use Chlorothalonil"},
                {"type": "prevention", "treatment": "Water at soil level, avoid wetting foliage"}
            ],
            "Tomato___Late_blight": [
                {"type": "organic", "treatment": "Remove infected plants immediately"},
                {"type": "chemical", "treatment": "Apply Mancozeb or Chlorothalonil"},
                {"type": "prevention", "treatment": "Ensure good drainage and air circulation"}
            ],
            "Potato___Early_blight": [
                {"type": "organic", "treatment": "Apply neem oil or copper fungicides"},
                {"type": "chemical", "treatment": "Use Azoxystrobin"},
                {"type": "prevention", "treatment": "Rotate crops and maintain soil health"}
            ],
            "Corn_(maize)___Common_rust_": [
                {"type": "organic", "treatment": "Remove infected leaves"},
                {"type": "chemical", "treatment": "Apply Propiconazole"},
                {"type": "prevention", "treatment": "Plant resistant varieties"}
            ],
            "healthy": [
                {"type": "maintenance", "treatment": "Continue regular watering and fertilization"},
                {"type": "monitoring", "treatment": "Regular inspection for early disease detection"},
                {"type": "prevention", "treatment": "Maintain good agricultural practices"}
            ]
        }
        
        # Get disease category
        disease_key = disease_name
        
        # Check if healthy
        if "healthy" in disease_name.lower():
            disease_key = "healthy"
        
        # Get recommendations or default
        recommendations = recommendations_db.get(
            disease_key,
            [
                {"type": "consult", "treatment": "Consult local agricultural expert"},
                {"type": "general", "treatment": "Remove affected plant parts"},
                {"type": "prevention", "treatment": "Improve field hygiene and crop rotation"}
            ]
        )
        
        return recommendations

# Global instance
disease_service = DiseaseDetectionService()
