"""
AI-Powered Crop Recommendation System
Uses Machine Learning to recommend best crops based on:
- Soil parameters (N, P, K, pH)
- Climate conditions (temperature, humidity, rainfall)
- Historical data
- Region-specific factors
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import logging
from typing import Dict, List
import os

logger = logging.getLogger(__name__)

class CropRecommendationAI:
    """
    ML-based crop recommendation system
    Uses Random Forest Classifier trained on crop suitability data
    """
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.crop_labels = [
            'rice', 'wheat', 'corn', 'potato', 'tomato', 
            'cotton', 'sugarcane', 'banana', 'mango', 'grapes',
            'apple', 'orange', 'papaya', 'coconut', 'watermelon',
            'muskmelon', 'onion', 'garlic', 'ginger', 'turmeric'
        ]
        self.load_or_create_model()
    
    def load_or_create_model(self):
        """Load pre-trained model or create new one"""
        model_path = "./models/crop_recommendation.pkl"
        scaler_path = "./models/crop_scaler.pkl"
        
        try:
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                logger.info("✅ Crop recommendation model loaded")
            else:
                logger.info("Creating new crop recommendation model...")
                self.create_model()
        except Exception as e:
            logger.warning(f"Could not load model: {e}. Creating new one...")
            self.create_model()
    
    def create_model(self):
        """Create and train a simple crop recommendation model"""
        try:
            # Generate synthetic training data based on agricultural knowledge
            X_train, y_train = self._generate_training_data()
            
            # Create and train model
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            
            # Fit scaler
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X_train)
            
            # Train model
            self.model.fit(X_scaled, y_train)
            
            logger.info("✅ Crop recommendation model trained successfully")
            
            # Save model
            os.makedirs("./models", exist_ok=True)
            joblib.dump(self.model, "./models/crop_recommendation.pkl")
            joblib.dump(self.scaler, "./models/crop_scaler.pkl")
            
        except Exception as e:
            logger.error(f"Model creation error: {e}")
            self.model = None
            self.scaler = None
    
    def _generate_training_data(self, samples_per_crop=100):
        """Generate synthetic training data based on crop requirements"""
        
        # Crop growing conditions (N, P, K, pH, temp, humidity, rainfall)
        crop_conditions = {
            'rice': {'N': 80, 'P': 40, 'K': 40, 'pH': 6.5, 'temp': 25, 'humidity': 80, 'rainfall': 200},
            'wheat': {'N': 50, 'P': 30, 'K': 30, 'pH': 6.5, 'temp': 20, 'humidity': 60, 'rainfall': 80},
            'corn': {'N': 80, 'P': 50, 'K': 50, 'pH': 6.0, 'temp': 25, 'humidity': 65, 'rainfall': 100},
            'potato': {'N': 50, 'P': 50, 'K': 50, 'pH': 5.5, 'temp': 20, 'humidity': 70, 'rainfall': 90},
            'tomato': {'N': 60, 'P': 60, 'K': 80, 'pH': 6.5, 'temp': 24, 'humidity': 60, 'rainfall': 70},
            'cotton': {'N': 120, 'P': 40, 'K': 40, 'pH': 6.5, 'temp': 28, 'humidity': 65, 'rainfall': 100},
            'sugarcane': {'N': 90, 'P': 45, 'K': 45, 'pH': 6.5, 'temp': 28, 'humidity': 75, 'rainfall': 180},
            'banana': {'N': 100, 'P': 75, 'K': 100, 'pH': 6.5, 'temp': 27, 'humidity': 80, 'rainfall': 200},
            'mango': {'N': 40, 'P': 40, 'K': 60, 'pH': 6.5, 'temp': 27, 'humidity': 70, 'rainfall': 120},
            'grapes': {'N': 60, 'P': 60, 'K': 80, 'pH': 6.5, 'temp': 25, 'humidity': 65, 'rainfall': 70},
            'apple': {'N': 40, 'P': 40, 'K': 50, 'pH': 6.0, 'temp': 18, 'humidity': 60, 'rainfall': 110},
            'orange': {'N': 60, 'P': 50, 'K': 70, 'pH': 6.5, 'temp': 25, 'humidity': 70, 'rainfall': 130},
            'papaya': {'N': 60, 'P': 60, 'K': 60, 'pH': 6.5, 'temp': 26, 'humidity': 75, 'rainfall': 150},
            'coconut': {'N': 70, 'P': 50, 'K': 120, 'pH': 6.0, 'temp': 28, 'humidity': 80, 'rainfall': 180},
            'watermelon': {'N': 80, 'P': 60, 'K': 100, 'pH': 6.5, 'temp': 27, 'humidity': 70, 'rainfall': 80},
            'muskmelon': {'N': 70, 'P': 50, 'K': 90, 'pH': 6.5, 'temp': 26, 'humidity': 65, 'rainfall': 70},
            'onion': {'N': 40, 'P': 40, 'K': 60, 'pH': 6.5, 'temp': 22, 'humidity': 65, 'rainfall': 80},
            'garlic': {'N': 40, 'P': 40, 'K': 60, 'pH': 6.5, 'temp': 20, 'humidity': 65, 'rainfall': 70},
            'ginger': {'N': 60, 'P': 60, 'K': 80, 'pH': 6.0, 'temp': 25, 'humidity': 75, 'rainfall': 150},
            'turmeric': {'N': 60, 'P': 60, 'K': 80, 'pH': 6.5, 'temp': 25, 'humidity': 75, 'rainfall': 150}
        }
        
        X = []
        y = []
        
        for crop, conditions in crop_conditions.items():
            for _ in range(samples_per_crop):
                # Add variation to create realistic data
                sample = [
                    conditions['N'] + np.random.normal(0, 15),
                    conditions['P'] + np.random.normal(0, 10),
                    conditions['K'] + np.random.normal(0, 10),
                    conditions['pH'] + np.random.normal(0, 0.5),
                    conditions['temp'] + np.random.normal(0, 3),
                    conditions['humidity'] + np.random.normal(0, 5),
                    conditions['rainfall'] + np.random.normal(0, 20)
                ]
                X.append(sample)
                y.append(crop)
        
        return np.array(X), np.array(y)
    
    def recommend_crops(
        self, 
        nitrogen: float, 
        phosphorus: float, 
        potassium: float,
        ph: float = 6.5,
        temperature: float = 25,
        humidity: float = 70,
        rainfall: float = 100
    ) -> List[Dict]:
        """
        Recommend top 3 suitable crops based on soil and climate parameters
        
        Returns list of {crop, suitability_score, confidence}
        """
        try:
            if self.model is None or self.scaler is None:
                return self._get_fallback_recommendations(
                    nitrogen, phosphorus, potassium, ph, temperature, humidity, rainfall
                )
            
            # Prepare input
            X = np.array([[nitrogen, phosphorus, potassium, ph, temperature, humidity, rainfall]])
            X_scaled = self.scaler.transform(X)
            
            # Get predictions with probabilities
            probabilities = self.model.predict_proba(X_scaled)[0]
            
            # Get top 3 crops
            top_indices = np.argsort(probabilities)[-3:][::-1]
            
            recommendations = []
            for idx in top_indices:
                crop = self.model.classes_[idx]
                confidence = float(probabilities[idx])
                
                # Calculate suitability score (0-100)
                suitability_score = int(confidence * 100)
                
                recommendations.append({
                    'crop': crop.capitalize(),
                    'suitability_score': suitability_score,
                    'confidence': round(confidence, 3),
                    'recommendation': self._get_crop_advice(crop, suitability_score)
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Recommendation error: {e}")
            return self._get_fallback_recommendations(
                nitrogen, phosphorus, potassium, ph, temperature, humidity, rainfall
            )
    
    def _get_fallback_recommendations(self, N, P, K, pH, temp, humidity, rainfall) -> List[Dict]:
        """Rule-based fallback recommendations"""
        
        recommendations = []
        
        # Rice - high water, moderate nutrients
        if rainfall > 150 and humidity > 75:
            recommendations.append({
                'crop': 'Rice',
                'suitability_score': 85,
                'confidence': 0.85,
                'recommendation': 'Excellent conditions for rice cultivation. High rainfall and humidity favor rice growth.'
            })
        
        # Tomato - moderate everything
        if 20 < temp < 30 and 50 < humidity < 70 and 50 < rainfall < 100:
            recommendations.append({
                'crop': 'Tomato',
                'suitability_score': 80,
                'confidence': 0.80,
                'recommendation': 'Good conditions for tomato. Moderate climate is ideal.'
            })
        
        # Wheat - cooler temperature, less water
        if temp < 25 and rainfall < 100:
            recommendations.append({
                'crop': 'Wheat',
                'suitability_score': 75,
                'confidence': 0.75,
                'recommendation': 'Suitable for wheat. Cooler temperatures and moderate rainfall are favorable.'
            })
        
        # Cotton - warm, moderate water
        if temp > 25 and 80 < rainfall < 120:
            recommendations.append({
                'crop': 'Cotton',
                'suitability_score': 78,
                'confidence': 0.78,
                'recommendation': 'Good for cotton cultivation. Warm climate suits cotton growth.'
            })
        
        # Default suggestions
        if len(recommendations) < 3:
            recommendations.extend([
                {
                    'crop': 'Corn',
                    'suitability_score': 70,
                    'confidence': 0.70,
                    'recommendation': 'Versatile crop suitable for various conditions.'
                },
                {
                    'crop': 'Potato',
                    'suitability_score': 68,
                    'confidence': 0.68,
                    'recommendation': 'Good general-purpose crop for moderate climates.'
                }
            ])
        
        return recommendations[:3]
    
    def _get_crop_advice(self, crop: str, score: int) -> str:
        """Get specific advice for recommended crop"""
        
        advice_map = {
            'rice': f"Suitability: {score}%. Ensure adequate water supply and maintain flooded conditions during growth.",
            'wheat': f"Suitability: {score}%. Plant in cooler months. Avoid waterlogging.",
            'corn': f"Suitability: {score}%. Requires good drainage and moderate water. Space plants properly.",
            'tomato': f"Suitability: {score}%. Needs support structures. Watch for fungal diseases.",
            'potato': f"Suitability: {score}%. Hill soil around plants. Harvest when foliage dies back.",
            'cotton': f"Suitability: {score}%. Requires warm climate. Control pests regularly.",
            'sugarcane': f"Suitability: {score}%. Long-duration crop. Needs abundant water and nutrients.",
            'banana': f"Suitability: {score}%. Requires rich soil and consistent moisture.",
            'mango': f"Suitability: {score}%. Tree crop. Requires good drainage and warm climate.",
            'grapes': f"Suitability: {score}%. Needs trellis support. Control fungal diseases."
        }
        
        return advice_map.get(crop.lower(), f"Suitability: {score}%. Consult local agricultural experts for best practices.")

# Global instance
crop_recommendation_ai = CropRecommendationAI()
