"""
Irrigation Calculator API Endpoints
"""
from flask import Blueprint, request, jsonify
from app.services.irrigation_calculator import irrigation_calculator
import logging

logger = logging.getLogger(__name__)

irrigation_bp = Blueprint('irrigation', __name__, url_prefix='/api/v1/irrigation')

@irrigation_bp.route('/calculate', methods=['POST'])
def calculate_irrigation():
    """
    Calculate irrigation requirements
    
    Body:
    {
        "crop_type": "tomato",
        "soil_type": "loamy",
        "area_acres": 2.5,
        "growth_stage": "mid",
        "temperature": 28,
        "humidity": 65,
        "rainfall_last_week": 10,
        "irrigation_efficiency": 0.75
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body required"}), 400
        
        # Required fields
        required = ['crop_type', 'soil_type', 'area_acres', 'growth_stage', 'temperature', 'humidity']
        missing = [field for field in required if field not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400
        
        result = irrigation_calculator.calculate_irrigation(
            crop_type=data['crop_type'],
            soil_type=data['soil_type'],
            area_acres=float(data['area_acres']),
            growth_stage=data['growth_stage'],
            temperature=float(data['temperature']),
            humidity=float(data['humidity']),
            rainfall_last_week=float(data.get('rainfall_last_week', 0)),
            irrigation_efficiency=float(data.get('irrigation_efficiency', 0.75))
        )
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except ValueError as e:
        return jsonify({"error": f"Invalid data format: {str(e)}"}), 400
    except Exception as e:
        logger.error(f"Irrigation calculation error: {e}")
        return jsonify({"error": str(e)}), 500

@irrigation_bp.route('/crops', methods=['GET'])
def get_supported_crops():
    """Get list of supported crops"""
    crops = list(irrigation_calculator.crop_water_requirements.keys())
    return jsonify({
        "crops": [crop.capitalize() for crop in crops],
        "count": len(crops)
    }), 200

@irrigation_bp.route('/soil-types', methods=['GET'])
def get_soil_types():
    """Get list of supported soil types"""
    soil_types = list(irrigation_calculator.soil_water_capacity.keys())
    return jsonify({
        "soil_types": [soil.capitalize() for soil in soil_types],
        "count": len(soil_types)
    }), 200

@irrigation_bp.route('/growth-stages', methods=['GET'])
def get_growth_stages():
    """Get list of growth stages"""
    stages = ['initial', 'development', 'mid', 'late']
    return jsonify({
        "growth_stages": [stage.capitalize() for stage in stages],
        "count": len(stages)
    }), 200
