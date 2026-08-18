"""
Chat/Advisory endpoints (Flask Version) - RAG with Ollama Embeddings
Enhanced multi-lingual chatbot with Retrieval-Augmented Generation
"""
from flask import Blueprint, request, jsonify, g
from app.core.security import token_required

# ✅ USING RAG V3.0: Production Chatbot with Ollama
from app.services.rag_chatbot_production import rag_chatbot_service

from datetime import datetime

blueprint = Blueprint('chat', __name__)

@blueprint.route('/message', methods=['POST'])
@token_required
def send_message():
    """Send a message to RAG-powered chatbot"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({"success": False, "message": "Message is required"}), 400
        
        # Get language preference
        language = data.get('language', 'en')
        
        # Get user ID from token
        user_id = g.user_id if hasattr(g, 'user_id') else None
        
        # Get RAG chatbot response with Ollama embeddings
        result = rag_chatbot_service.chat(message, language)
        
        if not result.get('success'):
            return jsonify(result), 500
        
        return jsonify({
            "success": True,
            "data": {
                "response": result.get('message', ''),
                "type": result.get('type', 'text'),
                "sources": result.get('sources', []),
                "rag_enabled": result.get('rag_enabled', False),
                "embedding_model": "Ollama nomic-embed-text" if result.get('rag_enabled') else "Fallback FAQ",
                "timestamp": datetime.now().isoformat(),
                "language": language
            }
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@blueprint.route('/history', methods=['GET'])
@token_required
def get_chat_history():
    """Get chat history"""
    try:
        # Return dummy chat history
        return jsonify({
            "success": True,
            "data": {
                "messages": [
                    {
                        "id": 1,
                        "message": "Hello, how can I improve tomato yield?",
                        "response": "To increase tomato yield: 1. Ensure proper spacing...",
                        "timestamp": (datetime.now()).isoformat()
                    }
                ]
            }
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
