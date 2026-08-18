"""
Disease Analytics API Endpoints
"""
from flask import Blueprint, request, jsonify, g
from app.core.security import token_required
from app.services.disease_analytics import disease_analytics
import logging

logger = logging.getLogger(__name__)

disease_analytics_bp = Blueprint('disease_analytics', __name__, url_prefix='/api/v1/disease-analytics')

@disease_analytics_bp.route('/history', methods=['GET'])
@token_required
def get_disease_history():
    """
    Get user's disease detection history
    Query params:
    - days: number of days (default 30)
    - limit: max results (default 50)
    """
    try:
        user_id = g.current_user.id
        days = int(request.args.get('days', 30))
        limit = int(request.args.get('limit', 50))
        
        history = disease_analytics.get_user_history(g.db, user_id, days, limit)
        
        return jsonify({
            "success": True,
            "history": history,
            "count": len(history),
            "period_days": days
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        return jsonify({"error": str(e)}), 500

@disease_analytics_bp.route('/trends', methods=['GET'])
@token_required
def get_disease_trends():
    """
    Get disease trends and analytics
    Query params:
    - days: analysis period (default 30)
    """
    try:
        user_id = g.current_user.id
        days = int(request.args.get('days', 30))
        
        trends = disease_analytics.get_disease_trends(g.db, user_id, days)
        
        return jsonify({
            "success": True,
            "trends": trends,
            "period_days": days
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching trends: {e}")
        return jsonify({"error": str(e)}), 500

@disease_analytics_bp.route('/treatment-effectiveness', methods=['GET'])
@token_required
def get_treatment_effectiveness():
    """Get treatment effectiveness analysis"""
    try:
        user_id = g.current_user.id
        
        effectiveness = disease_analytics.get_treatment_effectiveness(g.db, user_id)
        
        return jsonify({
            "success": True,
            "effectiveness": effectiveness
        }), 200
        
    except Exception as e:
        logger.error(f"Error analyzing treatments: {e}")
        return jsonify({"error": str(e)}), 500

@disease_analytics_bp.route('/field-analysis', methods=['GET'])
@token_required
def get_field_analysis():
    """Get field/location-wise disease analysis"""
    try:
        user_id = g.current_user.id
        
        field_analysis = disease_analytics.get_field_wise_analysis(g.db, user_id)
        
        return jsonify({
            "success": True,
            "field_analysis": field_analysis,
            "fields_count": len(field_analysis)
        }), 200
        
    except Exception as e:
        logger.error(f"Error in field analysis: {e}")
        return jsonify({"error": str(e)}), 500

@disease_analytics_bp.route('/detection', methods=['POST'])
@token_required
def save_detection():
    """
    Save a disease detection
    
    Body:
    {
        "disease_name": "Tomato Early Blight",
        "confidence": 0.87,
        "severity": "moderate",
        "crop_type": "Tomato",
        "crop_id": 1,
        "field_location": "Field A",
        "image_path": "/uploads/123.jpg",
        "weather_conditions": {}
    }
    """
    try:
        user_id = g.current_user.id
        data = request.get_json()
        
        if not data or 'disease_name' not in data:
            return jsonify({"error": "disease_name required"}), 400
        
        detection = disease_analytics.save_detection(
            db=g.db,
            user_id=user_id,
            disease_name=data['disease_name'],
            confidence=float(data.get('confidence', 0.0)),
            severity=data.get('severity', 'unknown'),
            crop_type=data.get('crop_type'),
            crop_id=data.get('crop_id'),
            field_location=data.get('field_location'),
            image_path=data.get('image_path'),
            weather_conditions=data.get('weather_conditions')
        )
        
        if detection:
            return jsonify({
                "success": True,
                "message": "Detection saved",
                "detection_id": detection.id
            }), 201
        else:
            return jsonify({"error": "Failed to save detection"}), 500
            
    except Exception as e:
        logger.error(f"Error saving detection: {e}")
        return jsonify({"error": str(e)}), 500

@disease_analytics_bp.route('/detection/<int:detection_id>/treatment', methods=['PUT'])
@token_required
def update_treatment_result(detection_id):
    """
    Update treatment result for a detection
    
    Body:
    {
        "treatment_applied": "Fungicide spray",
        "treatment_result": "effective",
        "notes": "Applied twice, symptoms reduced"
    }
    """
    try:
        user_id = g.current_user.id
        data = request.get_json()
        
        if not data or 'treatment_result' not in data:
            return jsonify({"error": "treatment_result required"}), 400
        
        success = disease_analytics.update_treatment_result(
            db=g.db,
            detection_id=detection_id,
            user_id=user_id,
            treatment_applied=data.get('treatment_applied', ''),
            treatment_result=data['treatment_result'],
            notes=data.get('notes')
        )
        
        if success:
            return jsonify({
                "success": True,
                "message": "Treatment result updated"
            }), 200
        else:
            return jsonify({"error": "Detection not found"}), 404
            
    except Exception as e:
        logger.error(f"Error updating treatment: {e}")
        return jsonify({"error": str(e)}), 500
