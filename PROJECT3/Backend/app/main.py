"""
AgriSmart AI - Main Application Entry Point (Flask Version)
"""
from flask import Flask, request, jsonify, g
import time
import logging
import sys
from pathlib import Path

from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
# DON'T import register_blueprints here - it triggers RAG import!
# from app.api.v1.router import register_blueprints

# Try to import MongoDB (optional dependency)
try:
    from app.core.mongodb import connect_mongodb
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("MongoDB libraries not installed. Expert consultations will use fallback.")

# Configure logging
Path("logs").mkdir(exist_ok=True)

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['MAX_CONTENT_LENGTH'] = settings.MAX_UPLOAD_SIZE

# CORS Configuration (manual implementation)
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin in settings.CORS_ORIGINS or '*' in settings.CORS_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS,PATCH'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

# Request timing middleware
@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def add_process_time_header(response):
    if hasattr(g, 'start_time'):
        process_time = time.time() - g.start_time
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(f"{request.method} {request.path} - {response.status_code} - {process_time:.3f}s")
    return response

# Exception handler
@app.errorhandler(Exception)
def global_exception_handler(exc):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return jsonify({
        "success": False,
        "message": "Internal server error",
        "error": str(exc) if settings.DEBUG else "An error occurred"
    }), 500

# Database session management
@app.before_request
def create_db_session():
    g.db = SessionLocal()

@app.teardown_request
def close_db_session(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Database session management
@app.before_request
def create_db_session():
    g.db = SessionLocal()

@app.teardown_request
def close_db_session(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Health check endpoints
@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "success": True,
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "running"
    })

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "success": True,
        "status": "healthy",
        "version": settings.APP_VERSION
    })

# Serve uploads directory (MUST be before catch-all OPTIONS route)
@app.route('/uploads/<path:filename>', methods=['GET'])
def serve_upload(filename):
    from flask import send_from_directory
    import os
    upload_dir = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    return send_from_directory(upload_dir, filename)

# OPTIONS handler for CORS preflight
@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    return '', 204

# Initialize database and MongoDB FIRST (before importing services that need it)
def init_database():
    """Initialize database connections"""
    logger.info("Starting AgriSmart AI Backend...")
    
    # Create SQLite tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")
    
    # Connect to MongoDB (if available) - MUST happen before blueprint registration
    if MONGODB_AVAILABLE:
        try:
            connect_mongodb()
            logger.info("✅ MongoDB connection initialized")
        except Exception as e:
            logger.warning(f"⚠️ MongoDB connection failed: {e}")
            logger.warning("   Some features (RAG, history, expert consultations) may not work")
    else:
        logger.warning("⚠️ MongoDB not available - install pymongo and motor for full features")

# Initialize MongoDB BEFORE registering blueprints
init_database()

# Import blueprints AFTER MongoDB is connected (blueprints import services that need MongoDB)
from app.api.v1.router import register_blueprints

# Register API blueprints (these import services that need MongoDB)
register_blueprints(app, prefix=settings.API_V1_PREFIX)

# Complete app initialization
def init_app():
    """Complete application initialization"""
    # Create necessary directories
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path("models").mkdir(exist_ok=True)
    
    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} started successfully!")

# Finish initialization
init_app()

if __name__ == "__main__":
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG
    )
