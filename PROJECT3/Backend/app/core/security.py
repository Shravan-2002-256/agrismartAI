"""
Security utilities for authentication and password hashing (Flask Version)
"""
from datetime import datetime, timedelta
from typing import Optional
import jwt
import bcrypt
from functools import wraps
from flask import request, jsonify, g

from app.core.config import settings
from app.models.user import User

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    """Hash a password"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt

def decode_token(token: str) -> dict:
    """Decode JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

def token_required(f):
    """Decorator for routes that require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({
                    "success": False,
                    "message": "Token format invalid"
                }), 401
        
        if not token:
            return jsonify({
                "success": False,
                "message": "Authentication token is missing"
            }), 401
        
        # Decode token
        payload = decode_token(token)
        
        if payload is None:
            return jsonify({
                "success": False,
                "message": "Invalid or expired token"
            }), 401
        
        username = payload.get("sub")
        
        if username is None:
            return jsonify({
                "success": False,
                "message": "Invalid token payload"
            }), 401
        
        # Get user from database
        db = g.get('db')
        if db is None:
            return jsonify({
                "success": False,
                "message": "Database session not available"
            }), 500
        
        user = db.query(User).filter(User.username == username).first()
        
        if user is None:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 401
        
        # Store user in g for access in route
        g.current_user = user
        
        return f(*args, **kwargs)
    
    return decorated

def get_current_user():
    """Get current authenticated user from g"""
    return g.get('current_user')
