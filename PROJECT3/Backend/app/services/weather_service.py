"""
Weather Service - Fetches weather data and generates crop alerts
"""
import requests
import logging
from typing import Dict, List
from datetime import datetime, timedelta

from app.core.config import settings

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.api_key = getattr(settings, 'WEATHER_API_KEY', None)
        self.api_url = getattr(settings, 'WEATHER_API_URL', 'https://api.openweathermap.org/data/2.5')
    
    def get_weather_forecast(self, lat: float, lon: float) -> Dict:
        """Get 7-day weather forecast"""
        try:
            # If no API key, use dummy data
            if not self.api_key or self.api_key == 'your_api_key_here':
                logger.warning("Weather API key not configured. Using dummy data.")
                return self._get_dummy_weather()
            
            # Current weather
            current_url = f"{self.api_url}/weather"
            current_params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            
            current_response = requests.get(current_url, params=current_params)
            current_data = current_response.json()
            
            # 7-day forecast
            forecast_url = f"{self.api_url}/forecast"
            forecast_params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric",
                "cnt": 40  # 5 days, 3-hour intervals
            }
            
            forecast_response = requests.get(forecast_url, params=forecast_params)
            forecast_data = forecast_response.json()
            
            # Process forecast data
            daily_forecast = self._process_forecast(forecast_data)
            
            # Generate alerts
            alerts = self._generate_crop_alerts(daily_forecast, current_data)
            
            return {
                "success": True,
                "location": current_data.get("name", "Unknown"),
                "current": {
                    "temp": current_data["main"]["temp"],
                    "feels_like": current_data["main"]["feels_like"],
                    "humidity": current_data["main"]["humidity"],
                    "description": current_data["weather"][0]["description"],
                    "icon": current_data["weather"][0]["icon"],
                    "wind_speed": current_data["wind"]["speed"]
                },
                "forecast": daily_forecast,
                "alerts": alerts
            }
            
        except Exception as e:
            logger.error(f"Weather API error: {e}", exc_info=True)
            # Return dummy data for testing
            logger.info("Falling back to dummy weather data")
            return self._get_dummy_weather()
    
    def _process_forecast(self, forecast_data: Dict) -> List[Dict]:
        """Process forecast data into daily summaries"""
        daily_data = {}
        
        for item in forecast_data.get("list", []):
            date = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")
            
            if date not in daily_data:
                daily_data[date] = {
                    "temps": [],
                    "humidity": [],
                    "precipitation": 0,
                    "description": item["weather"][0]["description"],
                    "icon": item["weather"][0]["icon"],
                    "wind_speed": []
                }
            
            daily_data[date]["temps"].append(item["main"]["temp"])
            daily_data[date]["humidity"].append(item["main"]["humidity"])
            daily_data[date]["wind_speed"].append(item["wind"]["speed"])
            
            if "rain" in item:
                daily_data[date]["precipitation"] += item["rain"].get("3h", 0)
        
        # Convert to list format
        forecast = []
        for date, data in list(daily_data.items())[:7]:
            forecast.append({
                "date": date,
                "temp_min": round(min(data["temps"]), 1),
                "temp_max": round(max(data["temps"]), 1),
                "humidity": round(sum(data["humidity"]) / len(data["humidity"])),
                "description": data["description"],
                "icon": data["icon"],
                "precipitation": round(data["precipitation"], 1),
                "wind_speed": round(sum(data["wind_speed"]) / len(data["wind_speed"]), 1)
            })
        
        return forecast
    
    def _generate_crop_alerts(self, forecast: List[Dict], current: Dict) -> List[Dict]:
        """Generate crop-specific weather alerts"""
        alerts = []
        
        # Check for heavy rain
        for day in forecast[:3]:
            if day["precipitation"] > 50:
                alerts.append({
                    "alert_type": "heavy_rain",
                    "severity": "high",
                    "message": f"Heavy rainfall expected on {day['date']}",
                    "recommendation": "Ensure proper drainage. Delay fertilizer application."
                })
        
        # Check for frost
        for day in forecast[:3]:
            if day["temp_min"] < 5:
                alerts.append({
                    "alert_type": "frost_risk",
                    "severity": "high",
                    "message": f"Low temperature on {day['date']}",
                    "recommendation": "Protect sensitive crops. Consider using covers."
                })
        
        # Check for drought conditions
        total_rain = sum(day["precipitation"] for day in forecast)
        if total_rain < 5:
            alerts.append({
                "alert_type": "drought",
                "severity": "medium",
                "message": "Low rainfall expected this week",
                "recommendation": "Plan irrigation schedule. Monitor soil moisture."
            })
        
        # Check for high heat
        for day in forecast[:3]:
            if day["temp_max"] > 38:
                alerts.append({
                    "alert_type": "heat_stress",
                    "severity": "medium",
                    "message": f"High temperature on {day['date']}",
                    "recommendation": "Ensure adequate watering. Provide shade if possible."
                })
        
        return alerts
    
    def _get_dummy_weather(self) -> Dict:
        """Return dummy weather data for testing"""
        return {
            "success": True,
            "location": "Test Location",
            "current": {
                "temp": 28,
                "feels_like": 30,
                "humidity": 65,
                "description": "partly cloudy",
                "icon": "02d",
                "wind_speed": 3.5
            },
            "forecast": [
                {
                    "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                    "temp_min": 22 + i,
                    "temp_max": 32 + i,
                    "humidity": 60 + i,
                    "description": "sunny",
                    "icon": "01d",
                    "precipitation": 0,
                    "wind_speed": 3.0
                }
                for i in range(7)
            ],
            "alerts": []
        }

# Global instance
weather_service = WeatherService()
