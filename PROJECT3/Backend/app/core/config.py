"""
Application Configuration (Flask/SQLite Version)
"""
from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AgriSmart AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production-09876543210987654321"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database - SQLite (Auth, Sessions, User Data)
    DATABASE_URL: str = "sqlite:///./agrismart.db"
    
    # Database - MongoDB Atlas (Telemetry, History, Vector Embeddings)
    # Format: mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB: str = "agrismart_dev"  # Changed to match your database
    MONGODB_VECTOR_SEARCH_ENABLED: bool = True  # MongoDB Atlas Vector Search
    
    # Redis (optional)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Weather API
    WEATHER_API_KEY: str = "demo_key"
    WEATHER_API_URL: str = "https://api.openweathermap.org/data/2.5"
    
    # ML Model Settings
    MODEL_PATH: str = "./models/disease_detection_mobilenetv2.h5"
    MODEL_INPUT_SIZE: int = 224
    DISEASE_CONFIDENCE_THRESHOLD: float = 0.65  # HITL threshold
    TENSORFLOW_HUB_URL: str = "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/5"
    
    # RAG Settings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"  # Sentence Transformers
    EMBEDDING_DIMENSION: int = 384
    RAG_TOP_K_RESULTS: int = 3  # Top-K similarity search
    KNOWLEDGE_BASE_PATH: str = "./data/knowledge_base"
    
    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    # ALLOWED_EXTENSIONS is a simple string, we'll split it
    ALLOWED_EXTENSIONS_STR: str = "jpg,jpeg,png"
    
    @property
    def ALLOWED_EXTENSIONS(self) -> List[str]:
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS_STR.split(',')]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    # CORS - Simple string list
    CORS_ORIGINS_STR: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173"
    
    @property
    def CORS_ORIGINS(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS_STR.split(',')]
    
    # Market Data
    AGMARKNET_API_URL: str = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    
    # Supported Languages
    SUPPORTED_LANGUAGES_STR: str = "en,hi,te,ta"
    
    @property
    def SUPPORTED_LANGUAGES(self) -> List[str]:
        return [lang.strip() for lang in self.SUPPORTED_LANGUAGES_STR.split(',')]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = 'ignore'  # Ignore extra fields from .env file

settings = Settings()

# Ensure directories exist
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path("logs").mkdir(exist_ok=True)
Path("models").mkdir(exist_ok=True)
Path("data/raw").mkdir(parents=True, exist_ok=True)
Path("data/processed").mkdir(parents=True, exist_ok=True)
