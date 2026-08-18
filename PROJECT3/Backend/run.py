"""
Run script for AgriSmart AI Backend (Flask)
"""
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.main import app

if __name__ == "__main__":
    print("🚀 Starting AgriSmart AI Backend...")
    print("📍 Server running at: http://localhost:8000")
    print("📖 Health check: http://localhost:8000/health")
    print("�� Press CTRL+C to quit")
    
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )
