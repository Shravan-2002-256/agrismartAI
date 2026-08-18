"""
Chatbot Schemas
"""
from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    message: str
    language: str = "en"

class ChatResponse(BaseModel):
    success: bool
    reply: str
    suggestions: List[str]
    language: str
