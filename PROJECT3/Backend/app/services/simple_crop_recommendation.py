"""
Simplified Crop Recommendation - Works WITHOUT scikit-learn
Uses rule-based AI algorithms
"""
import numpy as np
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class SimpleCropRecommendationAI:
    """
    Rule-based AI for crop recommendations
    NO scikit-learn required - uses agricultural knowledge base
    """
    
    def __init__(self):
        self.model_loaded = True
        logger.info("✅ Simple Crop Recommendation AI initialized (No scikit-learn required)")
        
        # Agricultural knowledge base
        self.crop_requirements = {
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
        }
    
    def calculate_suitability(self, crop: str, requirements: Dict, inputs: Dict) -> float:
        """
        AI algorithm to calculate crop suitability score
        Uses Euclidean distance in normalized feature space
        """
        # Normalize and calculate distance
        weights = {'N': 1.0, 'P': 1.0, 'K': 1.0, 'pH': 2.0, 'temp': 1.5, 'humidity': 1.0, 'rainfall': 1.0}
        
        total_distance = 0
        for param, ideal_value in requirements.items():
            actual_value = inputs.get(param, ideal_value)
            
            # Normalize by typical ranges
            ranges = {'N': 100, 'P': 100, 'K': 100, 'pH': 2, 'temp': 10, 'humidity': 20, 'rainfall': 100}
            normalized_diff = abs(actual_value - ideal_value) / ranges.get(param, 100)
            
            total_distance += weights[param] * (normalized_diff ** 2)
        
        # Convert distance to suitability score (0-100)
        suitability = max(0, 100 - (total_distance * 15))
        return min(100, suitability)
    
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
        AI-based crop recommendation
        Returns top 3 crops with suitability scores
        """
        inputs = {
            'N': nitrogen,
            'P': phosphorus,
            'K': potassium,
            'pH': ph,
            'temp': temperature,
            'humidity': humidity,
            'rainfall': rainfall
        }
        
        # Calculate suitability for all crops
        scores = []
        for crop, requirements in self.crop_requirements.items():
            score = self.calculate_suitability(crop, requirements, inputs)
            scores.append((crop, score))
        
        # Sort by suitability (descending)
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Get top 3 recommendations
        recommendations = []
        for crop, score in scores[:3]:
            recommendations.append({
                'crop': crop.capitalize(),
                'suitability_score': int(score),
                'confidence': round(score / 100, 3),
                'recommendation': self._get_crop_advice(crop, int(score))
            })
        
        return recommendations
    
    def _get_crop_advice(self, crop: str, score: int) -> str:
        """Get specific advice"""
        advice_map = {
            'rice': f"Suitability: {score}%. Ensure adequate water supply and flooded conditions.",
            'wheat': f"Suitability: {score}%. Plant in cooler months. Avoid waterlogging.",
            'corn': f"Suitability: {score}%. Requires good drainage and moderate water.",
            'tomato': f"Suitability: {score}%. Needs support structures. Watch for diseases.",
            'potato': f"Suitability: {score}%. Hill soil around plants.",
            'cotton': f"Suitability: {score}%. Requires warm climate. Control pests regularly.",
            'sugarcane': f"Suitability: {score}%. Long-duration crop. Needs abundant water.",
            'banana': f"Suitability: {score}%. Requires rich soil and consistent moisture.",
            'mango': f"Suitability: {score}%. Tree crop. Requires good drainage.",
            'grapes': f"Suitability: {score}%. Needs trellis support."
        }
        return advice_map.get(crop, f"Suitability: {score}%. Consult local experts.")

# Global instance
simple_crop_ai = SimpleCropRecommendationAI()
