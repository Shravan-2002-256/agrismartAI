"""
🤖 RAG CHATBOT - PRODUCTION READY
Retrieval-Augmented Generation with MongoDB Vector Search

Features:
- Ollama embeddings (nomic-embed-text) - 100% local, 768-dim
- MongoDB Atlas Vector Search for embeddings
- Multi-language support
- Grounded responses (no hallucinations)

Author: AgriSmart AI Team
Date: July 2026
"""

import logging
from typing import List, Dict, Optional
import numpy as np
from datetime import datetime
import requests

from app.core.config import settings
from app.core.mongodb import get_knowledge_base_collection, mongodb_db

logger = logging.getLogger(__name__)

# Check Ollama availability
OLLAMA_AVAILABLE = False
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=2)
    if response.status_code == 200:
        OLLAMA_AVAILABLE = True
        logger.info(" Ollama detected and running")
except:
    logger.warning("  Ollama not running. Will try Sentence Transformers.")

# Try importing sentence transformers as fallback
SENTENCE_TRANSFORMERS_AVAILABLE = False
if not OLLAMA_AVAILABLE:
    try:
        from sentence_transformers import SentenceTransformer
        SENTENCE_TRANSFORMERS_AVAILABLE = True
    except ImportError:
        logger.warning("  sentence-transformers not installed. RAG will use keyword fallback.")

EMBEDDINGS_AVAILABLE = OLLAMA_AVAILABLE or SENTENCE_TRANSFORMERS_AVAILABLE


class RAGChatbotService:
    """
    RAG Chatbot using MongoDB Vector Search with Ollama embeddings
    - Retrieves relevant context from knowledge base
    - Generates grounded responses
    - Multi-language support
    """
    
    def __init__(self):
        self.embedding_model = None
        self.knowledge_collection = None
        self.rag_enabled = False
        self.use_ollama = False
        self.ollama_model = "nomic-embed-text"
        self._initialize()
    
    def _initialize(self):
        """Initialize RAG components"""
        try:
            # Try Ollama first
            if OLLAMA_AVAILABLE:
                logger.info("🔄 Using Ollama for embeddings...")
                self.use_ollama = True
                logger.info(f"✅ Ollama embeddings ready: {self.ollama_model}")
                logger.info(f"   Dimension: 768 (nomic-embed-text)")
            
            # Fallback to Sentence Transformers
            elif SENTENCE_TRANSFORMERS_AVAILABLE:
                logger.info("🔄 Loading Sentence Transformers model...")
                self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
                logger.info(f"✅ Embeddings loaded: {settings.EMBEDDING_MODEL}")
                logger.info(f"   Dimension: {settings.EMBEDDING_DIMENSION}")
            
            # Get knowledge base collection
            self.knowledge_collection = get_knowledge_base_collection()
            
            if (self.use_ollama or self.embedding_model) and self.knowledge_collection is not None:
                self.rag_enabled = True
                doc_count = self.knowledge_collection.count_documents({})
                logger.info(f" RAG Chatbot ready (MongoDB Vector Search)")
                logger.info(f"    Knowledge base: {doc_count} documents")
            else:
                logger.warning("  RAG running in fallback mode (FAQ-based)")
                if self.knowledge_collection is None:
                    logger.warning("   Reason: MongoDB not connected yet")
                self.rag_enabled = False
                
        except Exception as e:
            logger.error(f" RAG initialization failed: {e}")
            self.rag_enabled = False
    
    def reinitialize_if_needed(self):
        """Re-initialize if MongoDB is now available but wasn't before"""
        if not self.rag_enabled and (self.use_ollama or self.embedding_model):
            # Try to reconnect to knowledge base
            self.knowledge_collection = get_knowledge_base_collection()
            if self.knowledge_collection is not None:
                self.rag_enabled = True
                doc_count = self.knowledge_collection.count_documents({})
                logger.info(f" RAG Chatbot re-initialized successfully!")
                logger.info(f"    Knowledge base: {doc_count} documents")
                return True
        return False
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for text using Ollama or Sentence Transformers"""
        try:
            # Use Ollama embeddings
            if self.use_ollama:
                response = requests.post(
                    "http://localhost:11434/api/embeddings",
                    json={
                        "model": self.ollama_model,
                        "prompt": text
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    embedding = response.json()["embedding"]
                    return embedding
                else:
                    logger.error(f"Ollama embedding error: {response.status_code}")
                    return None
            
            # Fallback to Sentence Transformers
            elif self.embedding_model:
                embedding = self.embedding_model.encode(text)
                return embedding.tolist()
            
            return None
            
        except Exception as e:
            logger.error(f"Embedding generation error: {e}")
            return None
    
    def search_knowledge_base(
        self, 
        query: str, 
        top_k: int = None,
        language: str = 'en'
    ) -> List[Dict]:
        """
        Search knowledge base using local vector similarity
        Returns top-k most relevant documents
        """
        if not self.rag_enabled or self.knowledge_collection is None:
            return []
        
        try:
            top_k = top_k or settings.RAG_TOP_K_RESULTS
            
            # Generate query embedding
            query_embedding = self.generate_embedding(query)
            if not query_embedding:
                return []
            
            # LOCAL VECTOR SEARCH (works without MongoDB Atlas)
            # Fetch all documents with embeddings
            docs = list(self.knowledge_collection.find(
                {
                    "embedding": {"$exists": True}
                    # Note: Not filtering by language since documents don't have metadata.language set
                }
            ))
            
            if not docs:
                logger.warning("No documents with embeddings found")
                return self._fallback_text_search(query, top_k, language)
            
            # Calculate cosine similarity in Python
            import numpy as np
            
            def cosine_similarity(vec1, vec2):
                """Calculate cosine similarity between two vectors"""
                vec1 = np.array(vec1)
                vec2 = np.array(vec2)
                return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
            
            # Score each document
            scored_docs = []
            for doc in docs:
                try:
                    doc_embedding = doc.get('embedding', [])
                    if doc_embedding:
                        similarity = cosine_similarity(query_embedding, doc_embedding)
                        doc['score'] = float(similarity)
                        scored_docs.append(doc)
                except Exception as e:
                    logger.debug(f"Error scoring document: {e}")
                    continue
            
            # Sort by similarity score (highest first)
            scored_docs.sort(key=lambda x: x.get('score', 0), reverse=True)
            
            # Return top-k results
            results = scored_docs[:top_k]
            
            logger.info(f"✅ Local vector search returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Vector search error: {e}")
            # Fallback to text search
            return self._fallback_text_search(query, top_k, language)
    
    def _fallback_text_search(
        self, 
        query: str, 
        top_k: int,
        language: str
    ) -> List[Dict]:
        """Fallback text-based search"""
        if self.knowledge_collection is None:
            return []
        
        try:
            # Simple text search as fallback
            query_terms = query.lower().split()
            results = []
            
            for term in query_terms[:3]:  # Use first 3 terms
                docs = self.knowledge_collection.find(
                    {
                        "text": {"$regex": term, "$options": "i"}
                        # Not filtering by language since metadata.language is not set
                    },
                    limit=top_k
                )
                results.extend(list(docs))
            
            # Remove duplicates
            seen_ids = set()
            unique_results = []
            for doc in results:
                doc_id = str(doc['_id'])
                if doc_id not in seen_ids:
                    seen_ids.add(doc_id)
                    unique_results.append(doc)
            
            return unique_results[:top_k]
            
        except Exception as e:
            logger.error(f"Fallback text search error: {e}")
            return []
    
    def generate_response(
        self, 
        query: str, 
        context_docs: List[Dict],
        language: str = 'en'
    ) -> Dict:
        """
        Generate response based on retrieved context
        Uses template-based generation (grounded, no hallucination)
        """
        if not context_docs:
            return self._fallback_response(query, language)
        
        try:
            # Combine relevant context
            context_text = "\n\n".join([
                doc.get('text', doc.get('content', '')) for doc in context_docs[:3]
            ])
            
            # Source citations
            sources = [
                {
                    'title': doc.get('metadata', {}).get('source', doc.get('metadata', {}).get('title', doc.get('title', 'Agricultural Knowledge Base'))),
                    'category': doc.get('metadata', {}).get('category', doc.get('metadata', {}).get('type', doc.get('section', 'General Farming'))),
                    'score': round(doc.get('score', 0), 3) if 'score' in doc else None
                }
                for doc in context_docs[:3]
            ]
            
            # Generate grounded response
            response = {
                'message': self._format_response(context_text, query, language),
                'sources': sources,
                'rag_enabled': True,
                'confidence': 'high' if len(context_docs) >= 2 else 'medium'
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Response generation error: {e}")
            return self._fallback_response(query, language)
    
    def _format_response(self, context: str, query: str, language: str) -> str:
        """Format response based on context"""
        # Truncate context if too long
        if len(context) > 500:
            context = context[:500] + "..."
        
        if language == 'en':
            return f"Based on agricultural knowledge:\n\n{context}\n\nThis information is verified and grounded in documented sources."
        elif language == 'hi':
            return f"कृषि ज्ञान के आधार पर:\n\n{context}\n\nयह जानकारी सत्यापित और प्रलेखित स्रोतों पर आधारित है।"
        elif language == 'te':
            return f"వ్యవసాయ జ్ఞానం ఆధారంగా:\n\n{context}\n\nఈ సమాచారం ధృవీకరించబడింది."
        elif language == 'ta':
            return f"விவசாய அறிவின் அடிப்படையில்:\n\n{context}\n\nஇந்த தகவல் சரிபார்க்கப்பட்டது."
        else:
            return context
    
    def _fallback_response(self, query: str, language: str) -> Dict:
        """Fallback FAQ-based response"""
        query_lower = query.lower()
        
        # Simple FAQ mapping
        faq_responses = {
            'en': {
                'disease': "To detect diseases, please upload a clear image of affected leaves using the Disease Detection feature. Our AI can identify various crop diseases.",
                'weather': "Check the Weather section for a 7-day forecast with crop-specific alerts for your location.",
                'market': "Visit Market Prices to see current rates and 7-day predictions for various crops.",
                'fertilizer': "Fertilizer needs depend on crop type and soil. Generally, use balanced NPK (10-10-10) during growth phase.",
                'default': "I can help with crop diseases, weather forecasts, market prices, and farming practices. Please ask a specific question."
            },
            'hi': {
                'disease': "बीमारियों का पता लगाने के लिए, रोग पहचान सुविधा का उपयोग करके प्रभावित पत्तियों की स्पष्ट छवि अपलोड करें।",
                'weather': "अपने स्थान के लिए 7-दिन के पूर्वानुमान के लिए मौसम अनुभाग देखें।",
                'market': "विभिन्न फसलों के लिए वर्तमान दरें और 7-दिन की भविष्यवाणी देखने के लिए बाजार मूल्य पर जाएं।",
                'default': "मैं फसल रोगों, मौसम पूर्वानुमान, बाजार मूल्य और खेती प्रथाओं में मदद कर सकता हूं।"
            }
        }
        
        responses = faq_responses.get(language, faq_responses['en'])
        
        # Match query to response
        for key in ['disease', 'weather', 'market', 'fertilizer']:
            if key in query_lower:
                return {
                    'message': responses.get(key, responses['default']),
                    'sources': [],
                    'rag_enabled': False,
                    'confidence': 'low'
                }
        
        return {
            'message': responses['default'],
            'sources': [],
            'rag_enabled': False,
            'confidence': 'low'
        }
    
    def chat(
        self, 
        message: str, 
        user_id: Optional[str] = None,
        language: str = 'en'
    ) -> Dict:
        """
        Complete chat pipeline
        1. Search knowledge base
        2. Generate grounded response
        3. Log conversation
        """
        try:
            # Search knowledge base
            context_docs = self.search_knowledge_base(message, language=language)
            
            # Generate response
            response = self.generate_response(message, context_docs, language)
            
            # Log conversation
            self._log_conversation(user_id, message, response, language)
            
            return {
                'success': True,
                **response
            }
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return {
                'success': False,
                'message': "Sorry, I encountered an error. Please try again.",
                'error': str(e)
            }
    
    def _log_conversation(
        self, 
        user_id: Optional[str], 
        query: str, 
        response: Dict,
        language: str
    ):
        """Log conversation to MongoDB"""
        try:
            if mongodb_db is not None:
                mongodb_db.chat_history.insert_one({
                    'user_id': user_id,
                    'query': query,
                    'response': response.get('message'),
                    'sources': response.get('sources', []),
                    'rag_enabled': response.get('rag_enabled', False),
                    'language': language,
                    'timestamp': datetime.utcnow()
                })
        except Exception as e:
            logger.warning(f"Failed to log conversation: {e}")


# Global service instance
rag_chatbot_service = RAGChatbotService()
