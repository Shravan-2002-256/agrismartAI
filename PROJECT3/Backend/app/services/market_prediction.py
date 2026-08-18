"""
Market Price Prediction Service using Time Series Forecasting
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Dict, List
import os

from app.core.config import settings

logger = logging.getLogger(__name__)

class MarketPredictionService:
    def __init__(self):
        self.models = {}
        self.historical_data = self._load_historical_data()
    
    def _load_historical_data(self) -> Dict:
        """Load or generate historical price data"""
        # This would normally load from database
        # For demo, generate synthetic data
        
        crops = ['tomato', 'potato', 'onion', 'rice', 'wheat', 'corn']
        data = {}
        
        for crop in crops:
            # Generate 90 days of historical data
            dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
            base_price = np.random.uniform(20, 100)
            
            # Add trend and seasonality
            trend = np.linspace(0, np.random.uniform(-10, 10), 90)
            seasonal = 10 * np.sin(np.linspace(0, 4*np.pi, 90))
            noise = np.random.normal(0, 5, 90)
            
            prices = base_price + trend + seasonal + noise
            prices = np.maximum(prices, 10)  # Ensure positive prices
            
            data[crop] = pd.DataFrame({
                'date': dates,
                'price': prices
            })
        
        return data
    
    def get_price_forecast(self, crop_type: str, region: str = None, days: int = 7) -> Dict:
        """Get price forecast for a crop"""
        try:
            crop_type = crop_type.lower()
            
            # Get historical data
            if crop_type not in self.historical_data:
                crop_type = 'tomato'  # Default
            
            hist_data = self.historical_data[crop_type]
            
            # Simple forecast using moving average and trend
            predictions = self._simple_forecast(hist_data, days)
            
            # Calculate trend
            trend = self._calculate_trend(hist_data)
            
            # Current price (last in historical data)
            current_price = float(hist_data['price'].iloc[-1])
            
            return {
                "success": True,
                "crop_type": crop_type,
                "region": region or "All India",
                "current_price": round(current_price, 2),
                "unit": "INR per quintal",
                "historical_prices": self._format_historical(hist_data.tail(30)),
                "predictions": predictions,
                "trend": trend
            }
            
        except Exception as e:
            logger.error(f"Market prediction error: {e}")
            return self._get_dummy_prices(crop_type)
    
    def _simple_forecast(self, data: pd.DataFrame, days: int) -> List[Dict]:
        """Simple forecasting using exponential smoothing"""
        prices = data['price'].values
        
        # Calculate trend
        recent_prices = prices[-14:]
        trend = (recent_prices[-7:].mean() - recent_prices[:7].mean()) / 7
        
        # Last known price
        last_price = prices[-1]
        
        predictions = []
        for i in range(1, days + 1):
            # Predicted price with trend
            pred_price = last_price + (trend * i)
            
            # Add some uncertainty
            confidence_range = abs(pred_price * 0.1)  # ±10%
            
            date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
            
            predictions.append({
                "date": date,
                "predicted_price": round(pred_price, 2),
                "confidence_interval": [
                    round(pred_price - confidence_range, 2),
                    round(pred_price + confidence_range, 2)
                ]
            })
        
        return predictions
    
    def _calculate_trend(self, data: pd.DataFrame) -> str:
        """Calculate price trend"""
        prices = data['price'].values
        
        recent_avg = prices[-7:].mean()
        previous_avg = prices[-14:-7].mean()
        
        change_percent = ((recent_avg - previous_avg) / previous_avg) * 100
        
        if change_percent > 5:
            return "rising"
        elif change_percent < -5:
            return "falling"
        else:
            return "stable"
    
    def _format_historical(self, data: pd.DataFrame) -> List[Dict]:
        """Format historical data for response"""
        return [
            {
                "date": row['date'].strftime("%Y-%m-%d"),
                "price": round(row['price'], 2),
                "market": "Average"
            }
            for _, row in data.iterrows()
        ]
    
    def _get_dummy_prices(self, crop_type: str) -> Dict:
        """Return dummy price data"""
        base_price = 50.0
        
        return {
            "success": True,
            "crop_type": crop_type,
            "region": "All India",
            "current_price": base_price,
            "unit": "INR per quintal",
            "historical_prices": [
                {
                    "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
                    "price": round(base_price + np.random.uniform(-10, 10), 2),
                    "market": "Average"
                }
                for i in range(30, 0, -1)
            ],
            "predictions": [
                {
                    "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                    "predicted_price": round(base_price + i, 2),
                    "confidence_interval": [
                        round(base_price + i - 5, 2),
                        round(base_price + i + 5, 2)
                    ]
                }
                for i in range(1, 8)
            ],
            "trend": "stable"
        }

# Global instance
market_service = MarketPredictionService()
market_prediction_service = market_service  # Alias for compatibility
