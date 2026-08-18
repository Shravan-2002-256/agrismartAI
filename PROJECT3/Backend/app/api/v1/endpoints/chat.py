"""
Chatbot Endpoints - RAG with Ollama Embeddings
"""
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.chat import ChatMessage, ChatResponse

# ✅ USING RAG V3.0: Production Chatbot with Ollama
from app.services.rag_chatbot_production import rag_chatbot_service

router = APIRouter()

@router.post("/query", response_model=ChatResponse)
async def chat_query(
    message: ChatMessage,
    current_user: User = Depends(get_current_active_user)
):
    """Send message to RAG-powered chatbot with Ollama embeddings"""
    
    try:
        response = rag_chatbot_service.chat(
            message.message,
            message.language
        )
        
        if not response.get('success'):
            raise HTTPException(
                status_code=500,
                detail=response.get('error', 'Chatbot error')
            )
        
        return {
            "success": True,
            "message": response.get('message', ''),
            "sources": response.get('sources', []),
            "rag_enabled": response.get('rag_enabled', False),
            "embedding_model": "Ollama nomic-embed-text" if response.get('rag_enabled') else "Fallback FAQ"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chatbot error: {str(e)}"
        )

@router.get("/history")
async def get_chat_history(
    limit: int = 20,
    current_user: User = Depends(get_current_active_user)
):
    """Get user's chat history (placeholder for MongoDB implementation)"""
    
    return {
        "success": True,
        "messages": [],
        "note": "Chat history feature coming soon"
    }
