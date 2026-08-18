"""
Insights API Endpoints
"""
from flask import Blueprint, jsonify, request, g
from app.services.insights_service import InsightsService
from app.core.security import token_required

blueprint = Blueprint('insights', __name__)


@blueprint.route('/weekly', methods=['GET'])
@token_required
def get_weekly_insights():
    """
    Get weekly insights and analysis
    
    Query Parameters:
        - days: Number of days to analyze (default: 7)
        - user_only: Whether to get insights for current user only (default: true)
        - language: Language code for translations (en, hi, te, ta)
    
    Returns:
        JSON with insights, patterns, and remedies
    """
    try:
        db = g.db
        current_user = g.current_user
        
        # Get query parameters
        days = request.args.get('days', 7, type=int)
        user_only = request.args.get('user_only', 'true').lower() == 'true'
        language = request.args.get('language', 'en')
        
        # Validate days parameter
        if days < 1 or days > 90:
            return jsonify({
                'success': False,
                'message': 'Days parameter must be between 1 and 90'
            }), 400
        
        # Get insights
        user_id = current_user.id if user_only else None
        insights_data = InsightsService.get_weekly_insights(db, user_id=user_id, days=days, language=language)
        
        return jsonify({
            'success': True,
            'data': insights_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to generate insights: {str(e)}'
        }), 500


@blueprint.route('/crop/<crop_type>', methods=['GET'])
@token_required
def get_crop_insights(crop_type):
    """
    Get insights for a specific crop type
    
    Args:
        crop_type: Type of crop to analyze
    
    Query Parameters:
        - days: Number of days to analyze (default: 7)
        - user_only: Whether to get insights for current user only (default: true)
    
    Returns:
        JSON with crop-specific insights
    """
    try:
        db = g.db
        current_user = g.current_user
        days = request.args.get('days', 7, type=int)
        user_only = request.args.get('user_only', 'true').lower() == 'true'
        
        # Get all insights
        user_id = current_user.id if user_only else None
        all_insights = InsightsService.get_weekly_insights(db, user_id=user_id, days=days)
        
        # Filter for specific crop
        crop_insights = None
        for insight in all_insights.get('insights', []):
            if insight['crop_type'].lower() == crop_type.lower():
                crop_insights = insight
                break
        
        if not crop_insights:
            return jsonify({
                'success': False,
                'message': f'No data found for {crop_type} in the last {days} days'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'crop_type': crop_type,
                'period': all_insights['period'],
                'insights': crop_insights
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get crop insights: {str(e)}'
        }), 500


@blueprint.route('/remedies/<disease_name>', methods=['GET'])
@token_required
def get_disease_remedies(disease_name):
    """
    Get remedies for a specific disease
    
    Args:
        disease_name: Name of the disease
    
    Returns:
        JSON with disease information and remedies
    """
    try:
        remedies_data = InsightsService._get_remedies(disease_name)
        
        return jsonify({
            'success': True,
            'data': {
                'disease': disease_name,
                'info': remedies_data
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get remedies: {str(e)}'
        }), 500
