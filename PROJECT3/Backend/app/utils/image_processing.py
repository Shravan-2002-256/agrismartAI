"""
Image Processing Utilities
"""
from PIL import Image
import io
import os
from typing import Tuple

def validate_image(file_bytes: bytes) -> bool:
    """Validate if bytes represent a valid image"""
    try:
        Image.open(io.BytesIO(file_bytes))
        return True
    except Exception:
        return False

def resize_image(file_bytes: bytes, size: Tuple[int, int]) -> bytes:
    """Resize image to specified size"""
    image = Image.open(io.BytesIO(file_bytes))
    
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize
    image = image.resize(size, Image.Resampling.LANCZOS)
    
    # Save to bytes
    output = io.BytesIO()
    image.save(output, format='JPEG', quality=85)
    output.seek(0)
    
    return output.read()

def get_image_dimensions(file_bytes: bytes) -> Tuple[int, int]:
    """Get image width and height"""
    image = Image.open(io.BytesIO(file_bytes))
    return image.size
