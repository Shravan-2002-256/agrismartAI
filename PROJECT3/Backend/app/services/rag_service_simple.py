"""
Ultra-Lightweight RAG Service - ZERO External Dependencies!
Uses only Python built-in libraries (no pip install needed)

Perfect for restricted networks where pip install doesn't work
"""
import logging
import os
import json
import re
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from collections import Counter
import math

logger = logging.getLogger(__name__)


class SimpleRAGService:
    """
    Simple RAG using keyword matching and basic similarity
    NO external dependencies - uses only Python built-ins!
    """
    
    def __init__(
        self,
        vector_db_path: str = "./vector_db_simple",
        collection_name: str = "agri_knowledge"
    ):
        self.vector_db_path = Path(vector_db_path)
        self.collection_name = collection_name
        self.enabled = True  # Always enabled - no dependencies!
        
        # Storage
        self.documents = []
        self.metadatas = []
        self.document_tokens = []  # Tokenized documents for similarity
        
        # Initialize
        self._initialize_rag()
        logger.info("✅ Simple RAG Service initialized (keyword matching mode - NO dependencies!)")
    
    def _initialize_rag(self):
        """Initialize storage and load existing data if available"""
        
        # Create storage directory
        self.vector_db_path.mkdir(parents=True, exist_ok=True)
        
        # Try to load existing database
        self._load_database()
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization - split into words and normalize"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        
        # Split into words
        words = text.split()
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be', 
                     'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                     'would', 'should', 'could', 'may', 'might', 'can', 'this', 'that',
                     'these', 'those', 'it', 'its', 'i', 'you', 'he', 'she', 'we', 'they'}
        
        words = [w for w in words if w not in stop_words and len(w) > 2]
        
        return words
    
    def _calculate_similarity(self, tokens1: List[str], tokens2: List[str]) -> float:
        """Calculate cosine similarity between two token lists"""
        if not tokens1 or not tokens2:
            return 0.0
        
        # Count word frequencies
        freq1 = Counter(tokens1)
        freq2 = Counter(tokens2)
        
        # Get all unique words
        all_words = set(freq1.keys()) | set(freq2.keys())
        
        # Calculate dot product and magnitudes
        dot_product = sum(freq1.get(word, 0) * freq2.get(word, 0) for word in all_words)
        
        magnitude1 = math.sqrt(sum(freq**2 for freq in freq1.values()))
        magnitude2 = math.sqrt(sum(freq**2 for freq in freq2.values()))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        similarity = dot_product / (magnitude1 * magnitude2)
        return similarity
    
    def _save_database(self):
        """Save the database to disk (JSON format)"""
        try:
            db_file = self.vector_db_path / f"{self.collection_name}.json"
            
            data = {
                'documents': self.documents,
                'metadatas': self.metadatas,
                'document_tokens': self.document_tokens
            }
            
            with open(db_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 Database saved: {len(self.documents)} documents")
            
        except Exception as e:
            logger.error(f"Error saving database: {e}")
    
    def _load_database(self):
        """Load existing database from disk"""
        try:
            db_file = self.vector_db_path / f"{self.collection_name}.json"
            
            if db_file.exists():
                with open(db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.documents = data.get('documents', [])
                self.metadatas = data.get('metadatas', [])
                self.document_tokens = data.get('document_tokens', [])
                
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
        Add documents to the database
        
        Args:
            documents: List of text documents
            metadatas: Optional metadata for each document
            ids: Optional unique IDs (not used in this implementation)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Add documents and metadata
            for doc in documents:
                self.documents.append(doc)
                self.document_tokens.append(self._tokenize(doc))
            
            if metadatas:
                self.metadatas.extend(metadatas)
            else:
                self.metadatas.extend([{}] * len(documents))
            
            # Save to disk
            self._save_database()
            
            logger.info(f"✅ Added {len(documents)} documents to simple RAG")
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
        Query the database for relevant documents
        
        Args:
            query_text: User's question or query
            n_results: Number of relevant documents to retrieve
            filter_metadata: Optional metadata filters (not implemented)
        
        Returns:
            List of relevant documents with metadata
        """
        if not self.documents:
            return []
        
        try:
            # Tokenize the query
            query_tokens = self._tokenize(query_text)
            
            if not query_tokens:
                return []
            
            # Calculate similarity with all documents
            similarities = []
            for i, doc_tokens in enumerate(self.document_tokens):
                similarity = self._calculate_similarity(query_tokens, doc_tokens)
                similarities.append((i, similarity))
            
            # Sort by similarity (highest first)
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Get top N results
            formatted_results = []
            for idx, similarity in similarities[:n_results]:
                if similarity > 0:  # Only include if there's some similarity
                    formatted_results.append({
                        'document': self.documents[idx],
                        'metadata': self.metadatas[idx] if idx < len(self.metadatas) else {},
                        'similarity': similarity,
                        'id': f"doc_{idx}"
                    })
            
            logger.info(f"🔍 Retrieved {len(formatted_results)} relevant documents")
            return formatted_results
            
        except Exception as e:
            logger.error(f"❌ Error querying simple RAG: {e}")
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
        # Query for relevant documents
        results = self.query(query_text, n_results=n_results)
        
        if not results:
            return "", []
        
        # Format context
        context_parts = []
        for i, result in enumerate(results, 1):
            # Truncate long documents
            doc_text = result['document']
            if len(doc_text) > 500:
                doc_text = doc_text[:500] + "..."
            context_parts.append(f"[Source {i}]: {doc_text}")
        
        formatted_context = "\n\n".join(context_parts)
        return formatted_context, results
    
    def get_statistics(self) -> Dict:
        """Get RAG database statistics"""
        return {
            "enabled": True,
            "total_documents": len(self.documents),
            "collection_name": self.collection_name,
            "vector_db_path": str(self.vector_db_path),
            "mode": "Simple (keyword matching - NO dependencies)"
        }
    
    def reset_database(self) -> bool:
        """Reset/clear the database"""
        try:
            self.documents = []
            self.metadatas = []
            self.document_tokens = []
            
            # Delete saved file if exists
            db_file = self.vector_db_path / f"{self.collection_name}.json"
            if db_file.exists():
                db_file.unlink()
            
            logger.info("✅ Simple RAG database reset successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Error resetting database: {e}")
            return False


# Global instance
_simple_rag_instance = None


def get_simple_rag_service() -> SimpleRAGService:
    """Get or create simple RAG service singleton"""
    global _simple_rag_instance
    
    if _simple_rag_instance is None:
        vector_db_path = os.getenv('VECTOR_DB_PATH', './vector_db_simple')
        rag_enabled = os.getenv('RAG_ENABLED', 'true').lower() == 'true'
        
        if rag_enabled:
            _simple_rag_instance = SimpleRAGService(vector_db_path=vector_db_path)
        else:
            logger.info("Simple RAG disabled via environment variable")
            _simple_rag_instance = SimpleRAGService()
            _simple_rag_instance.enabled = False
    
    return _simple_rag_instance
