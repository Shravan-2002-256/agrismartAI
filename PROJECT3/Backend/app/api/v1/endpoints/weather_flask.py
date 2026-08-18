"""
Weather endpoints with AI Advisory Layer
AI-Enhanced Weather Intelligence for Crop Management
"""
from flask import Blueprint, request, jsonify, g
from app.core.security import token_required
from app.services.ai_weather_advisory import get_smart_weather_advisory
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)

blueprint = Blueprint('weather', __name__)

@blueprint.route('/current', methods=['GET'])
@token_required
def get_current_weather():
    """Get current weather"""
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        
        if not lat or not lon:
            return jsonify({"success": False, "message": "Latitude and longitude required"}), 400
        
        return jsonify({
            "success": True,
            "data": {
                "temperature": round(25 + random.uniform(-5, 5), 1),
                "humidity": random.randint(60, 85),
                "pressure": random.randint(1010, 1020),
                "wind_speed": round(random.uniform(5, 15), 1),
                "description": random.choice(["Clear sky", "Partly cloudy", "Cloudy", "Light rain"]),
                "icon": "01d",
                "location": f"Location ({lat}, {lon})",
                "timestamp": datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@blueprint.route('/forecast', methods=['GET'])
@token_required
def get_forecast():
    """
    🧠 AI-ENHANCED WEATHER FORECAST ENDPOINT
    
    Returns weather data PLUS AI-generated crop-specific advisory
    """
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        days = request.args.get('days', 7, type=int)
        crop_type = request.args.get('crop_type', 'tomato')
        
        if not lat or not lon:
            return jsonify({"success": False, "message": "Latitude and longitude required"}), 400
        
        logger.info(f"Fetching intelligent weather advisory for {crop_type} at ({lat}, {lon})")
        
        # 🚀 CALL AGENTIC WEATHER SERVICE
        advisory_result = get_smart_weather_advisory(lat, lon, crop_type)
        
        if not advisory_result.get('success'):
            return jsonify(advisory_result), 500
        
        # Return enhanced response with AI layer
        return jsonify({
            "success": True,
            "data": advisory_result
        })
        
    except Exception as e:
        logger.error(f"Weather forecast error: {e}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500
        current = {
            "temp": round(25 + random.uniform(-5, 5), 1),
            "humidity": random.randint(60, 85),
            "pressure": random.randint(1010, 1020),
            "wind_speed": round(random.uniform(5, 15), 1),
            "description": random.choice(["Clear sky", "Partly cloudy", "Cloudy", "Light rain"]),
            "icon": "01d"
        }
        
        # Generate forecast
        forecast = []
        for i in range(min(days, 7)):
            date = datetime.now() + timedelta(days=i)
            forecast.append({
                "date": date.date().isoformat(),
                "temperature_max": round(28 + random.uniform(-3, 3), 1),
                "temperature_min": round(18 + random.uniform(-3, 3), 1),
                "humidity": random.randint(60, 85),
                "precipitation": round(random.uniform(0, 10), 1),
                "description": random.choice(["Clear", "Partly cloudy", "Cloudy", "Rain"]),
                "icon": random.choice(["01d", "02d", "03d", "10d"])
            })
        
        return jsonify({
            "success": True,
            "data": {
                "location": f"Location ({lat}, {lon})",
                "current": current,
                "forecast": forecast
            }
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@blueprint.route('/alerts', methods=['GET'])
@token_required
def get_weather_alerts():
    """Get weather alerts"""
    try:
        return jsonify({
            "success": True,
            "data": {
                "alerts": [
                    {
                        "id": 1,
                        "type": "rain",
                        "severity": "moderate",
                        "message": "Heavy rainfall expected in next 48 hours",
                        "start_time": (datetime.now() + timedelta(hours=12)).isoformat(),
                        "end_time": (datetime.now() + timedelta(hours=60)).isoformat()
                    }
                ]
            }
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
