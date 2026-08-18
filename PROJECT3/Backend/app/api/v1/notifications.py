"""
Notification API Endpoints
"""
from flask import Blueprint, request, jsonify, g
from app.core.security import token_required
from app.services.notification_service import notification_service
import logging

logger = logging.getLogger(__name__)

notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/v1/notifications')

@notifications_bp.route('/', methods=['GET'])
@token_required
def get_notifications():
    """
    Get user notifications
    Query params:
    - unread_only: true/false
    - limit: number (default 50)
    """
    try:
        user_id = g.current_user.id
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        limit = int(request.args.get('limit', 50))
        
        notifications = notification_service.get_user_notifications(
            g.db, user_id, unread_only, limit
        )
        
        return jsonify({
            "success": True,
            "notifications": notifications,
            "count": len(notifications)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching notifications: {e}")
        return jsonify({"error": str(e)}), 500

@notifications_bp.route('/<int:notification_id>/read', methods=['PUT'])
@token_required
def mark_notification_read(notification_id):
    """Mark a notification as read"""
    try:
        user_id = g.current_user.id
        
        success = notification_service.mark_as_read(g.db, notification_id, user_id)
        
        if success:
            return jsonify({"success": True, "message": "Notification marked as read"}), 200
        else:
            return jsonify({"error": "Notification not found"}), 404
            
    except Exception as e:
        logger.error(f"Error marking notification as read: {e}")
        return jsonify({"error": str(e)}), 500

@notifications_bp.route('/read-all', methods=['PUT'])
@token_required
def mark_all_read():
    """Mark all notifications as read"""
    try:
        user_id = g.current_user.id
        
        success = notification_service.mark_all_as_read(g.db, user_id)
        
        if success:
            return jsonify({"success": True, "message": "All notifications marked as read"}), 200
        else:
            return jsonify({"error": "Failed to mark notifications as read"}), 500
            
    except Exception as e:
        logger.error(f"Error marking all as read: {e}")
        return jsonify({"error": str(e)}), 500

@notifications_bp.route('/<int:notification_id>', methods=['DELETE'])
@token_required
def delete_notification(notification_id):
    """Delete a notification"""
    try:
        user_id = g.current_user.id
        
        success = notification_service.delete_notification(g.db, notification_id, user_id)
        
        if success:
            return jsonify({"success": True, "message": "Notification deleted"}), 200
        else:
            return jsonify({"error": "Notification not found or unauthorized"}), 404
            
    except Exception as e:
        logger.error(f"Error deleting notification: {e}")
        return jsonify({"error": str(e)}), 500

@notifications_bp.route('/test', methods=['POST'])
@token_required
def create_test_notification():
    """Create a test notification (for development)"""
    try:
        user_id = g.current_user.id
        data = request.get_json()
        
        notification = notification_service.create_notification(
            db=g.db,
            user_id=user_id,
            notification_type=data.get('type', 'test'),
            title=data.get('title', 'Test Notification'),
            message=data.get('message', 'This is a test notification'),
            priority=data.get('priority', 'medium')
        )
        
        if notification:
            return jsonify({
                "success": True,
                "message": "Test notification created",
                "notification_id": notification.id
            }), 201
        else:
            return jsonify({"error": "Failed to create notification"}), 500
            
    except Exception as e:
        logger.error(f"Error creating test notification: {e}")
        return jsonify({"error": str(e)}), 500

@notifications_bp.route('/weather-alert', methods=['POST'])
@token_required
def create_weather_alert():
    """Generate weather-based alert"""
    try:
        user_id = g.current_user.id
        data = request.get_json()
        
        alerts = notification_service.generate_weather_alert(
            db=g.db,
            user_id=user_id,
            weather_condition=data.get('condition', 'normal'),
            temperature=float(data.get('temperature', 25)),
            rainfall=float(data.get('rainfall', 0))
        )
        
        return jsonify({
            "success": True,
            "alerts_generated": alerts,
            "count": len(alerts)
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating weather alert: {e}")
        return jsonify({"error": str(e)}), 500
