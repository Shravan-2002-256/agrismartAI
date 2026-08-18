"""
User endpoints (Flask Version) - Minimal implementation
"""
from flask import Blueprint, request, jsonify, g
from app.core.security import token_required
from app.models.crop import Crop

blueprint = Blueprint('user', __name__)

@blueprint.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Get user profile"""
    try:
        user = g.current_user
        return jsonify({
            "success": True,
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name or "",
                "phone": user.phone or "",
                "language": user.language
            }
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@blueprint.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    """Update user profile"""
    try:
        user = g.current_user
        data = request.get_json()
        
        if 'full_name' in data:
            user.full_name = data['full_name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'language' in data:
            user.language = data['language']
        
        g.db.commit()
        
        return jsonify({
            "success": True,
            "message": "Profile updated successfully"
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@blueprint.route('/crops', methods=['GET'])
@token_required
def get_crops():
    """Get user's crops"""
    try:
        user = g.current_user
        crops = g.db.query(Crop).filter(Crop.user_id == user.id).all()
        
        return jsonify({
            "success": True,
            "data": [{
                "id": crop.id,
                "crop_type": crop.crop_type,
                "variety": crop.variety,
                "area_size": crop.area_size,
                "planted_date": crop.planted_date.isoformat() if crop.planted_date else None,
                "location": crop.location
            } for crop in crops]
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@blueprint.route('/crops', methods=['POST'])
@token_required
def add_crop():
    """Add a new crop"""
    try:
        user = g.current_user
        data = request.get_json()
        
        from datetime import datetime
        
        new_crop = Crop(
            user_id=user.id,
            crop_type=data.get('crop_type'),
            variety=data.get('variety', ''),
            area_size=data.get('area_size', 0),
            planted_date=datetime.fromisoformat(data['planted_date']) if data.get('planted_date') else None,
            location=data.get('location', '')
        )
        
        g.db.add(new_crop)
        g.db.commit()
        g.db.refresh(new_crop)
        
        return jsonify({
            "success": True,
            "message": "Crop added successfully",
            "data": {
                "id": new_crop.id,
                "crop_type": new_crop.crop_type,
                "variety": new_crop.variety,
                "area_size": new_crop.area_size,
                "planted_date": new_crop.planted_date.isoformat() if new_crop.planted_date else None,
                "location": new_crop.location
            }
        }), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@blueprint.route('/crops/<int:crop_id>', methods=['DELETE'])
@token_required
def delete_crop(crop_id):
    """Delete a crop"""
    try:
        user = g.current_user
        crop = g.db.query(Crop).filter(Crop.id == crop_id, Crop.user_id == user.id).first()
        
        if not crop:
            return jsonify({"success": False, "message": "Crop not found"}), 404
        
        g.db.delete(crop)
        g.db.commit()
        
        return jsonify({
            "success": True,
            "message": "Crop deleted successfully"
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
