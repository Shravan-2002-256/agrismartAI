"""
MongoDB Database Connection and Utilities
Supports both local MongoDB and MongoDB Atlas
"""
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from typing import Optional
import os

from app.core.config import settings

logger = logging.getLogger(__name__)

# MongoDB clients
mongodb_client: Optional[MongoClient] = None
mongodb_async_client: Optional[AsyncIOMotorClient] = None
mongodb_db = None
mongodb_async_db = None


def connect_mongodb():
    """Initialize MongoDB connection (synchronous)"""
    global mongodb_client, mongodb_db
    
    try:
        mongodb_url = settings.MONGODB_URL
        
        # Connect to MongoDB
        mongodb_client = MongoClient(
            mongodb_url,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000
        )
        
        # Test connection
        mongodb_client.server_info()
        
        # Get database
        mongodb_db = mongodb_client[settings.MONGODB_DB]
        
        logger.info(f"✅ MongoDB connected successfully: {settings.MONGODB_DB}")
        
        # Create indexes
        _create_indexes()
        
        return mongodb_db
        
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        logger.warning("⚠️  Application will run without MongoDB features")
        mongodb_client = None
        mongodb_db = None
        return None


async def connect_mongodb_async():
    """Initialize MongoDB connection (asynchronous)"""
    global mongodb_async_client, mongodb_async_db
    
    try:
        mongodb_url = settings.MONGODB_URL
        
        # Connect to MongoDB (async)
        mongodb_async_client = AsyncIOMotorClient(
            mongodb_url,
            serverSelectionTimeoutMS=5000
        )
        
        # Test connection
        await mongodb_async_client.server_info()
        
        # Get database
        mongodb_async_db = mongodb_async_client[settings.MONGODB_DB]
        
        logger.info(f"✅ MongoDB (async) connected successfully: {settings.MONGODB_DB}")
        
        return mongodb_async_db
        
    except Exception as e:
        logger.error(f"❌ MongoDB (async) connection failed: {e}")
        mongodb_async_client = None
        mongodb_async_db = None
        return None


def _create_indexes():
    """Create MongoDB indexes for performance"""
    if mongodb_db is None:
        return
    
    try:
        # Disease history indexes
        mongodb_db.disease_history.create_index([("user_id", 1), ("detected_at", -1)])
        mongodb_db.disease_history.create_index([("disease_detected", 1)])
        mongodb_db.disease_history.create_index([("crop_type", 1)])
        
        # Knowledge base vector index (if Vector Search enabled)
        if settings.MONGODB_VECTOR_SEARCH_ENABLED:
            # MongoDB Atlas Vector Search index created via UI or API
            # Index definition:
            # {
            #   "fields": [{
            #     "type": "vector",
            #     "path": "embedding",
            #     "numDimensions": 384,
            #     "similarity": "cosine"
            #   }]
            # }
            logger.info("✅ Vector Search enabled (create index via MongoDB Atlas UI)")
        
        # Market prices indexes
        mongodb_db.market_prices.create_index([("commodity", 1), ("date", -1)])
        
        # Expert consultation indexes
        mongodb_db.expert_consultations.create_index([("phone", 1), ("timestamp", -1)])
        mongodb_db.expert_consultations.create_index([("disease", 1)])
        mongodb_db.expert_consultations.create_index([("timestamp", -1)])
        
        logger.info("✅ MongoDB indexes created")
        
    except Exception as e:
        logger.warning(f"⚠️  Index creation warning: {e}")


def get_mongodb():
    """Get MongoDB database instance (synchronous)"""
    return mongodb_db


def get_mongodb_async():
    """Get MongoDB database instance (asynchronous)"""
    return mongodb_async_db


def close_mongodb():
    """Close MongoDB connections"""
    global mongodb_client, mongodb_async_client
    
    if mongodb_client:
        mongodb_client.close()
        logger.info("MongoDB connection closed")
    
    if mongodb_async_client:
        mongodb_async_client.close()
        logger.info("MongoDB (async) connection closed")


# Collection helpers
def get_disease_history_collection():
    """Get disease history collection"""
    if mongodb_db is not None:
        return mongodb_db.disease_history
    return None


def get_knowledge_base_collection():
    """Get knowledge base collection (for RAG)"""
    if mongodb_db is not None:
        return mongodb_db.knowledge_base
    return None


def get_market_prices_collection():
    """Get market prices collection"""
    if mongodb_db is not None:
        return mongodb_db.market_prices
    return None


def get_expert_consultations_collection():
    """Get expert consultations collection"""
    if mongodb_db is not None:
        return mongodb_db.expert_consultations
    return None
