"""
RAG (Retrieval-Augmented Generation) Service for AgriSmart AI
FREE Implementation - No API Keys Required!

Uses:
- ChromaDB: Local vector database
- Sentence Transformers: Free embeddings (all-MiniLM-L6-v2)
- 100% Offline after initial model download
"""
import logging
import os
from typing import List, Dict, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

# Try importing RAG dependencies (optional)
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    logger.warning("ChromaDB not installed. RAG features disabled.")
    CHROMADB_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    logger.warning("Sentence Transformers not installed. RAG features disabled.")
    SENTENCE_TRANSFORMERS_AVAILABLE = False


class AgriRAGService:
    """
    Agricultural RAG Service - Free & Offline
    Retrieves relevant agricultural knowledge to enhance chatbot responses
    """
    
    def __init__(
        self,
        vector_db_path: str = "./vector_db",
        embedding_model: str = "all-MiniLM-L6-v2",
        collection_name: str = "agri_knowledge"
    ):
        self.vector_db_path = Path(vector_db_path)
        self.embedding_model_name = embedding_model
        self.collection_name = collection_name
        self.enabled = False
        
        # Initialize components
        self.client = None
        self.collection = None
        self.embedding_model = None
        
        # Check if RAG can be enabled
        if CHROMADB_AVAILABLE and SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self._initialize_rag()
                self.enabled = True
                logger.info("✅ RAG Service initialized successfully (FREE mode)")
            except Exception as e:
                logger.error(f"❌ RAG initialization failed: {e}")
                self.enabled = False
        else:
            logger.warning("⚠️ RAG dependencies not available. Running without RAG.")
    
    def _initialize_rag(self):
        """Initialize ChromaDB and embedding model"""
        
        # Create vector DB directory if it doesn't exist
        self.vector_db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.vector_db_path),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            logger.info(f"📚 Loaded existing collection: {self.collection_name}")
        except Exception:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Agricultural knowledge base"}
            )
            logger.info(f"📚 Created new collection: {self.collection_name}")
        
        # Initialize embedding model (downloads ~80MB on first run)
        logger.info(f"🔄 Loading embedding model: {self.embedding_model_name}...")
        self.embedding_model = SentenceTransformer(self.embedding_model_name)
        logger.info(f"✅ Embedding model loaded successfully")
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ) -> bool:
        """
        Add documents to the vector database
        
        Args:
            documents: List of text documents
            metadatas: Optional metadata for each document
            ids: Optional unique IDs for documents
        
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            logger.warning("RAG not enabled. Cannot add documents.")
            return False
        
        try:
            # Generate embeddings
            embeddings = self.embedding_model.encode(documents).tolist()
            
            # Generate IDs if not provided
            if ids is None:
                existing_count = self.collection.count()
                ids = [f"doc_{existing_count + i}" for i in range(len(documents))]
            
            # Add to collection
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas or [{}] * len(documents),
                ids=ids
            )
            
            logger.info(f"✅ Added {len(documents)} documents to RAG database")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error adding documents: {e}")
            return False
    
    def query(
        self,
        query_text: str,
        n_results: int = 3,
        filter_metadata: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Query the vector database for relevant documents
        
        Args:
            query_text: User's question or query
            n_results: Number of relevant documents to retrieve
            filter_metadata: Optional metadata filters
        
        Returns:
            List of relevant documents with metadata
        """
        if not self.enabled:
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query_text]).tolist()[0]
            
            # Query the collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter_metadata
            )
            
            # Format results
            formatted_results = []
            if results and results['documents'] and len(results['documents']) > 0:
                for i, doc in enumerate(results['documents'][0]):
                    formatted_results.append({
                        'document': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else None,
                        'id': results['ids'][0][i] if results['ids'] else None
                    })
            
            logger.info(f"🔍 Retrieved {len(formatted_results)} relevant documents")
            return formatted_results
            
        except Exception as e:
            logger.error(f"❌ Error querying RAG: {e}")
            return []
    
    def get_context_for_query(
        self,
        query_text: str,
        n_results: int = 3
    ) -> Tuple[str, List[Dict]]:
        """
        Get formatted context for a query (useful for chatbot)
        
        Args:
            query_text: User's question
            n_results: Number of documents to retrieve
        
        Returns:
            Tuple of (formatted_context_string, list_of_source_documents)
        """
        if not self.enabled:
            return "", []
        
        # Query for relevant documents
        results = self.query(query_text, n_results=n_results)
        
        if not results:
            return "", []
        
        # Format context
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(f"[Source {i}]: {result['document']}")
        
        formatted_context = "\n\n".join(context_parts)
        return formatted_context, results
    
    def get_statistics(self) -> Dict:
        """Get RAG database statistics"""
        if not self.enabled or not self.collection:
            return {
                "enabled": False,
                "total_documents": 0,
                "collection_name": self.collection_name
            }
        
        try:
            return {
                "enabled": True,
                "total_documents": self.collection.count(),
                "collection_name": self.collection_name,
                "embedding_model": self.embedding_model_name,
                "vector_db_path": str(self.vector_db_path)
            }
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {"enabled": False, "error": str(e)}
    
    def reset_database(self) -> bool:
        """Reset/clear the vector database (use with caution!)"""
        if not self.enabled:
            return False
        
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Agricultural knowledge base"}
            )
            logger.info("✅ RAG database reset successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Error resetting database: {e}")
            return False


# Try importing lightweight RAG as fallback
try:
    from app.services.rag_service_lite import get_lightweight_rag_service
    LIGHTWEIGHT_RAG_AVAILABLE = True
except ImportError:
    LIGHTWEIGHT_RAG_AVAILABLE = False

# Try importing simple RAG as final fallback (NO dependencies!)
try:
    from app.services.rag_service_simple import get_simple_rag_service
    SIMPLE_RAG_AVAILABLE = True
except ImportError:
    SIMPLE_RAG_AVAILABLE = False


# Global instance (lazy initialization)
_rag_service_instance = None


def get_rag_service():
    """
    Get or create RAG service singleton
    
    Priority order:
    1. ChromaDB + Sentence Transformers (best quality)
    2. TF-IDF with scikit-learn (good quality, lighter)
    3. Simple keyword matching (basic, but NO dependencies!)
    
    Returns the best available RAG implementation
    """
    global _rag_service_instance
    
    if _rag_service_instance is None:
        # Get configuration from environment
        vector_db_path = os.getenv('VECTOR_DB_PATH', './vector_db')
        embedding_model = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
        rag_enabled = os.getenv('RAG_ENABLED', 'true').lower() == 'true'
        
        if not rag_enabled:
            logger.info("RAG disabled via environment variable")
            # Create disabled instance
            _rag_service_instance = AgriRAGService()
            _rag_service_instance.enabled = False
            return _rag_service_instance
        
        # Try Option 1: Full RAG with ChromaDB and sentence-transformers (BEST)
        if CHROMADB_AVAILABLE and SENTENCE_TRANSFORMERS_AVAILABLE:
            _rag_service_instance = AgriRAGService(
                vector_db_path=vector_db_path,
                embedding_model=embedding_model
            )
            if _rag_service_instance.enabled:
                logger.info("✅ Using FULL RAG (ChromaDB + Sentence Transformers)")
                return _rag_service_instance
        
        # Try Option 2: Lightweight RAG with TF-IDF (GOOD)
        if LIGHTWEIGHT_RAG_AVAILABLE:
            logger.info("⚠️ Full RAG unavailable, trying Lightweight RAG (TF-IDF)")
            _rag_service_instance = get_lightweight_rag_service()
            if _rag_service_instance.enabled:
                logger.info("✅ Using LIGHTWEIGHT RAG (TF-IDF with scikit-learn)")
                return _rag_service_instance
        
        # Try Option 3: Simple RAG with keyword matching (BASIC but ALWAYS WORKS)
        if SIMPLE_RAG_AVAILABLE:
            logger.info("⚠️ Lightweight RAG unavailable, using Simple RAG (keyword matching)")
            _rag_service_instance = get_simple_rag_service()
            logger.info("✅ Using SIMPLE RAG (keyword matching - NO dependencies needed!)")
            return _rag_service_instance
        
        # No RAG available
        logger.warning("⚠️ No RAG implementation available")
        _rag_service_instance = AgriRAGService()
        _rag_service_instance.enabled = False
    
    return _rag_service_instance


# Convenience function for quick queries
def query_knowledge_base(query: str, n_results: int = 3) -> List[Dict]:
    """Quick function to query the knowledge base"""
    rag_service = get_rag_service()
    return rag_service.query(query, n_results=n_results)
