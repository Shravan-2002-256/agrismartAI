"""
Lightweight RAG Service - No Heavy Dependencies Required!
Uses TF-IDF for embeddings instead of sentence-transformers

This is a fallback when sentence-transformers cannot be installed
Works with standard Python packages (sklearn, numpy)
"""
import logging
import os
import json
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import pickle

logger = logging.getLogger(__name__)

# Try importing lightweight dependencies
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    logger.warning("sklearn not available. Lightweight RAG disabled.")
    SKLEARN_AVAILABLE = False


class LightweightRAGService:
    """
    Lightweight RAG using TF-IDF (no sentence-transformers needed!)
    Perfect for restricted networks or offline environments
    """
    
    def __init__(
        self,
        vector_db_path: str = "./vector_db_lite",
        collection_name: str = "agri_knowledge"
    ):
        self.vector_db_path = Path(vector_db_path)
        self.collection_name = collection_name
        self.enabled = False
        
        # Storage
        self.documents = []
        self.metadatas = []
        self.vectorizer = None
        self.document_vectors = None
        
        # Check if we can enable
        if SKLEARN_AVAILABLE:
            try:
                self._initialize_rag()
                self.enabled = True
                logger.info("✅ Lightweight RAG Service initialized (TF-IDF mode)")
            except Exception as e:
                logger.error(f"❌ Lightweight RAG initialization failed: {e}")
                self.enabled = False
        else:
            logger.warning("⚠️ sklearn not available. Install with: pip install scikit-learn")
    
    def _initialize_rag(self):
        """Initialize TF-IDF vectorizer and load existing data if available"""
        
        # Create storage directory
        self.vector_db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),  # Unigrams and bigrams
            min_df=1,
            max_df=0.95
        )
        
        # Try to load existing database
        self._load_database()
    
    def _save_database(self):
        """Save the database to disk"""
        try:
            db_file = self.vector_db_path / f"{self.collection_name}.pkl"
            
            data = {
                'documents': self.documents,
                'metadatas': self.metadatas,
                'vectorizer': self.vectorizer,
                'document_vectors': self.document_vectors
            }
            
            with open(db_file, 'wb') as f:
                pickle.dump(data, f)
            
            logger.info(f"💾 Database saved: {len(self.documents)} documents")
            
        except Exception as e:
            logger.error(f"Error saving database: {e}")
    
    def _load_database(self):
        """Load existing database from disk"""
        try:
            db_file = self.vector_db_path / f"{self.collection_name}.pkl"
            
            if db_file.exists():
                with open(db_file, 'rb') as f:
                    data = pickle.load(f)
                
                self.documents = data.get('documents', [])
                self.metadatas = data.get('metadatas', [])
                self.vectorizer = data.get('vectorizer')
                self.document_vectors = data.get('document_vectors')
                
                logger.info(f"📚 Loaded existing database: {len(self.documents)} documents")
            else:
                logger.info(f"📚 Creating new database: {self.collection_name}")
                
        except Exception as e:
            logger.warning(f"Could not load existing database: {e}")
    
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
            ids: Optional unique IDs (not used in this implementation)
        
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            logger.warning("Lightweight RAG not enabled. Cannot add documents.")
            return False
        
        try:
            # Add documents and metadata
            self.documents.extend(documents)
            
            if metadatas:
                self.metadatas.extend(metadatas)
            else:
                self.metadatas.extend([{}] * len(documents))
            
            # Rebuild TF-IDF vectors for all documents
            if self.documents:
                self.document_vectors = self.vectorizer.fit_transform(self.documents)
            
            # Save to disk
            self._save_database()
            
            logger.info(f"✅ Added {len(documents)} documents to lightweight RAG")
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
            filter_metadata: Optional metadata filters (not implemented in lite version)
        
        Returns:
            List of relevant documents with metadata
        """
        if not self.enabled or not self.documents:
            return []
        
        try:
            # Vectorize the query
            query_vector = self.vectorizer.transform([query_text])
            
            # Calculate cosine similarity with all documents
            similarities = cosine_similarity(query_vector, self.document_vectors)[0]
            
            # Get top N results
            top_indices = similarities.argsort()[-n_results:][::-1]
            
            # Format results
            formatted_results = []
            for idx in top_indices:
                if similarities[idx] > 0:  # Only include if there's some similarity
                    formatted_results.append({
                        'document': self.documents[idx],
                        'metadata': self.metadatas[idx] if idx < len(self.metadatas) else {},
                        'similarity': float(similarities[idx]),
                        'id': f"doc_{idx}"
                    })
            
            logger.info(f"🔍 Retrieved {len(formatted_results)} relevant documents")
            return formatted_results
            
        except Exception as e:
            logger.error(f"❌ Error querying lightweight RAG: {e}")
            return []
    
    def get_context_for_query(
        self,
        query_text: str,
        n_results: int = 3
    ) -> Tuple[str, List[Dict]]:
        """
        Get formatted context for a query
        
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
        if not self.enabled:
            return {
                "enabled": False,
                "total_documents": 0,
                "collection_name": self.collection_name,
                "mode": "disabled"
            }
        
        return {
            "enabled": True,
            "total_documents": len(self.documents),
            "collection_name": self.collection_name,
            "vector_db_path": str(self.vector_db_path),
            "mode": "TF-IDF (lightweight)"
        }
    
    def reset_database(self) -> bool:
        """Reset/clear the vector database"""
        if not self.enabled:
            return False
        
        try:
            self.documents = []
            self.metadatas = []
            self.document_vectors = None
            
            # Delete saved file if exists
            db_file = self.vector_db_path / f"{self.collection_name}.pkl"
            if db_file.exists():
                db_file.unlink()
            
            logger.info("✅ Lightweight RAG database reset successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Error resetting database: {e}")
            return False


# Global instance
_lightweight_rag_instance = None


def get_lightweight_rag_service() -> LightweightRAGService:
    """Get or create lightweight RAG service singleton"""
    global _lightweight_rag_instance
    
    if _lightweight_rag_instance is None:
        vector_db_path = os.getenv('VECTOR_DB_PATH', './vector_db_lite')
        rag_enabled = os.getenv('RAG_ENABLED', 'true').lower() == 'true'
        
        if rag_enabled:
            _lightweight_rag_instance = LightweightRAGService(
                vector_db_path=vector_db_path
            )
        else:
            logger.info("Lightweight RAG disabled via environment variable")
            _lightweight_rag_instance = LightweightRAGService()
            _lightweight_rag_instance.enabled = False
    
    return _lightweight_rag_instance
