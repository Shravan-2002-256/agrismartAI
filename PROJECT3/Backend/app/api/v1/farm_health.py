"""
Farm Health API Endpoints
"""
from flask import Blueprint, jsonify, g
from app.core.security import token_required
from app.services.farm_health import farm_health_service
import logging

logger = logging.getLogger(__name__)

farm_health_bp = Blueprint('farm_health', __name__, url_prefix='/api/v1/farm-health')

@farm_health_bp.route('/score', methods=['GET'])
@token_required
def get_health_score():
    """Get farm health score for current user"""
    try:
        user_id = g.current_user.id
        
        health_data = farm_health_service.calculate_health_score(g.db, user_id)
        
        return jsonify(health_data), 200
        
    except Exception as e:
        logger.error(f"Error fetching health score: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
