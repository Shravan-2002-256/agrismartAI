"""
Authentication endpoints (Flask Version)
"""
from flask import Blueprint, request, jsonify, g
from datetime import timedelta

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    token_required
)
from app.models.user import User
from app.core.config import settings

blueprint = Blueprint('auth', __name__)

@blueprint.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Debug logging
        print(f"📝 Register request data: {data}")
        print(f"📝 Request content type: {request.content_type}")
        print(f"📝 Request data: {request.data}")
        
        # Check if data is None
        if data is None:
            print("❌ No JSON data received")
            return jsonify({
                "success": False,
                "message": "No JSON data received. Please send JSON with Content-Type: application/json"
            }), 400
        
        # Validate required fields
        if not all(k in data for k in ['username', 'email', 'password']):
            missing = [k for k in ['username', 'email', 'password'] if k not in data]
            print(f"❌ Missing fields: {missing}")
            return jsonify({
                "success": False,
                "message": f"Missing required fields: {', '.join(missing)}"
            }), 400
        
        db = g.db
        
        # Check if user exists
        existing_user = db.query(User).filter(
            (User.username == data['username']) | (User.email == data['email'])
        ).first()
        
        if existing_user:
            return jsonify({
                "success": False,
                "message": "Username or email already exists"
            }), 400
        
        # Create new user
        hashed_password = get_password_hash(data['password'])
        new_user = User(
            username=data['username'],
            email=data['email'],
            password_hash=hashed_password,
            full_name=data.get('full_name', ''),
            phone=data.get('phone', ''),
            language=data.get('language', 'en')
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Create access token
        access_token = create_access_token(data={"sub": new_user.username})
        
        return jsonify({
            "success": True,
            "message": "User registered successfully",
            "data": {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": new_user.id,
                    "username": new_user.username,
                    "email": new_user.email,
                    "full_name": new_user.full_name
                }
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@blueprint.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.form.get('username')
            password = request.form.get('password')
        
        if not username or not password:
            return jsonify({
                "success": False,
                "message": "Username and password required"
            }), 400
        
        db = g.db
        
        # Find user
        user = db.query(User).filter(User.username == username).first()
        
        if not user or not verify_password(password, user.password_hash):
            return jsonify({
                "success": False,
                "message": "Invalid username or password"
            }), 401
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return jsonify({
            "success": True,
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@blueprint.route('/refresh', methods=['POST'])
@token_required
def refresh_token():
    """Refresh access token"""
    try:
        user = g.current_user
        
        # Create new access token
        access_token = create_access_token(data={"sub": user.username})
        
        return jsonify({
            "success": True,
            "message": "Token refreshed",
            "access_token": access_token,
            "token_type": "bearer"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@blueprint.route('/me', methods=['GET'])
@token_required
def get_me():
    """Get current user info"""
    try:
        user = g.current_user
        
        return jsonify({
            "success": True,
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "phone": user.phone,
                "language": user.language
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
