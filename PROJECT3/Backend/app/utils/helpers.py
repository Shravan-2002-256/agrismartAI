"""
Helper Utilities
"""
from datetime import datetime
from typing import Dict, Any
import hashlib

def generate_file_hash(file_bytes: bytes) -> str:
    """Generate SHA256 hash of file"""
    return hashlib.sha256(file_bytes).hexdigest()

def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime to string"""
    return dt.strftime(format_str)

def success_response(data: Any = None, message: str = "Success") -> Dict:
    """Generate standard success response"""
    response = {
        "success": True,
        "message": message
    }
    if data is not None:
        response["data"] = data
    return response

def error_response(message: str = "Error occurred", error: str = None) -> Dict:
    """Generate standard error response"""
    response = {
        "success": False,
        "message": message
    }
    if error:
        response["error"] = error
    return response
