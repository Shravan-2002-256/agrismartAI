"""
Database Configuration and Session Management (Flask/SQLite Version)
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# SQLAlchemy Database (SQLite by default)
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# MongoDB Connection (Optional)
try:
    from pymongo import MongoClient
    mongo_client = MongoClient(settings.MONGODB_URL)
    mongo_db = mongo_client[settings.MONGODB_DB]
    logger.info("MongoDB connected successfully")
except Exception as e:
    logger.warning(f"MongoDB not available: {e}")
    mongo_db = None

# Redis Connection (Optional)
try:
    import redis
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True
    )
    redis_client.ping()
    logger.info("Redis connected successfully")
except Exception as e:
    logger.warning(f"Redis not available: {e}")
    redis_client = None

# Dependency for getting DB session (Flask uses g.db instead)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get MongoDB database
def get_mongo_db():
    return mongo_db

# Get Redis client
def get_redis():
    return redis_client
