"""
Reports API Endpoints
Generate data for various report types
"""
from flask import Blueprint, jsonify, g, request
from app.core.security import token_required
from app.models.detection import Detection
from app.services.farm_health import farm_health_service
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

reports_bp = Blueprint('reports', __name__, url_prefix='/api/v1/reports')

@reports_bp.route('/disease', methods=['GET'])
@token_required
def get_disease_report():
    """Get disease detection report data"""
    try:
        user_id = g.current_user.id
        days = int(request.args.get('days', 30))
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Get all detections
        detections = g.db.query(Detection).filter(
            Detection.user_id == user_id,
            Detection.detected_at >= cutoff_date
        ).order_by(Detection.detected_at.desc()).all()
        
        total_detections = len(detections)
        healthy_count = sum(1 for d in detections if 'healthy' in d.disease_detected.lower())
        disease_count = total_detections - healthy_count
        health_rate = (healthy_count / total_detections * 100) if total_detections > 0 else 0
        
        history = []
        for d in detections[:50]:  # Limit to 50 recent
            history.append({
                'detected_at': d.detected_at.isoformat() if d.detected_at else None,
                'crop_type': d.crop_type or 'Unknown',
                'disease_detected': d.disease_detected,
                'confidence': int(d.confidence * 100) if d.confidence <= 1 else int(d.confidence),
                'severity': d.severity or 'N/A'
            })
        
        return jsonify({
            'success': True,
            'total_detections': total_detections,
            'healthy_count': healthy_count,
            'disease_count': disease_count,
            'health_rate': int(health_rate),
            'period_days': days,
            'history': history
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating disease report: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@reports_bp.route('/farm-health', methods=['GET'])
@token_required
def get_farm_health_report():
    """Get farm health report data"""
    try:
        user_id = g.current_user.id
        health_data = farm_health_service.calculate_health_score(g.db, user_id)
        return jsonify(health_data), 200
        
    except Exception as e:
        logger.error(f"Error generating farm health report: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
