"""
AI-Powered Chatbot Service using LangChain & Advanced NLP
Supports: OpenAI GPT, Google Gemini, Offline Models, and RAG
"""
import logging
from typing import Dict, List, Optional
import re
import os
from datetime import datetime

logger = logging.getLogger(__name__)

# Try importing RAG service (optional)
try:
    from app.services.rag_service import get_rag_service
    RAG_AVAILABLE = True
except ImportError:
    logger.warning("RAG service not available. Running without RAG.")
    RAG_AVAILABLE = False

# Try importing AI libraries (optional dependencies)
try:
    from langchain.llms import OpenAI
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts import PromptTemplate, ChatPromptTemplate
    from langchain.chains import LLMChain, ConversationChain
    from langchain.memory import ConversationBufferMemory
    LANGCHAIN_AVAILABLE = True
except ImportError:
    logger.warning("LangChain not installed. Using fallback chatbot.")
    LANGCHAIN_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    logger.warning("Google Generative AI not installed.")
    GEMINI_AVAILABLE = False

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    logger.warning("Transformers not installed.")
    TRANSFORMERS_AVAILABLE = False


class AIAgriChatbot:
    """
    Advanced AI Chatbot for Agriculture with multiple backends:
    1. OpenAI GPT-3.5/4 (if API key available)
    2. Google Gemini (if API key available)
    3. Local Transformers model (offline)
    4. RAG-enhanced responses (FREE, no API key)
    5. Rule-based fallback (always available)
    """
    
    def __init__(self):
        self.mode = "rule-based"  # default
        self.llm = None
        self.conversation_memory = {}
        self.rag_service = None
        self.rag_enabled = False
        self.initialize_ai()
        self.initialize_rag()
    
    def initialize_rag(self):
        """Initialize RAG service if available and enabled"""
        rag_enabled_env = os.getenv('RAG_ENABLED', 'true').lower() == 'true'
        
        logger.info(f"🔧 RAG Initialization: ENV RAG_ENABLED={rag_enabled_env}, RAG_AVAILABLE={RAG_AVAILABLE}")
        
        if RAG_AVAILABLE and rag_enabled_env:
            try:
                logger.info("🔧 Calling get_rag_service()...")
                self.rag_service = get_rag_service()
                logger.info(f"🔧 RAG Service returned: {self.rag_service}")
                logger.info(f"🔧 RAG Service enabled: {self.rag_service.enabled if self.rag_service else 'None'}")
                
                if self.rag_service and self.rag_service.enabled:
                    self.rag_enabled = True
                    stats = self.rag_service.get_statistics()
                    logger.info(f"✅ RAG enabled for enhanced chatbot responses")
                    logger.info(f"📊 RAG Statistics: {stats}")
                else:
                    logger.warning("ℹ️ RAG service available but not enabled")
            except Exception as e:
                logger.warning(f"RAG initialization failed: {e}", exc_info=True)
                self.rag_enabled = False
        else:
            logger.info(f"ℹ️ RAG not available (RAG_AVAILABLE={RAG_AVAILABLE}) or disabled via environment (rag_enabled_env={rag_enabled_env})")

    
    def initialize_ai(self):
        """Initialize available AI backend"""
        
        # Try OpenAI first
        openai_key = os.getenv('OPENAI_API_KEY')
        if LANGCHAIN_AVAILABLE and openai_key:
            try:
                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.7,
                    openai_api_key=openai_key
                )
                self.mode = "openai"
                logger.info("✅ AI Chatbot initialized with OpenAI GPT-3.5")
                return
            except Exception as e:
                logger.warning(f"OpenAI initialization failed: {e}")
        
        # Try Google Gemini
        gemini_key = os.getenv('GOOGLE_API_KEY')
        if GEMINI_AVAILABLE and gemini_key:
            try:
                genai.configure(api_key=gemini_key)
                self.llm = genai.GenerativeModel('gemini-pro')
                self.mode = "gemini"
                logger.info("✅ AI Chatbot initialized with Google Gemini")
                return
            except Exception as e:
                logger.warning(f"Gemini initialization failed: {e}")
        
        # Try Local Transformers (offline)
        if TRANSFORMERS_AVAILABLE:
            try:
                # Using a small conversational model
                self.llm = pipeline('text-generation', model='gpt2', max_length=100)
                self.mode = "transformers"
                logger.info("✅ AI Chatbot initialized with local Transformers model")
                return
            except Exception as e:
                logger.warning(f"Transformers initialization failed: {e}")
        
        # Fallback to rule-based
        logger.info("ℹ️ Using enhanced rule-based chatbot")
        self.mode = "rule-based"
    
    def _get_rag_context(self, message: str, n_results: int = 3) -> tuple:
        """
        Get relevant context from RAG knowledge base
        
        Returns:
            tuple: (context_string, list_of_sources)
        """
        if not self.rag_enabled or not self.rag_service:
            logger.info("❌ RAG not enabled or service not available")
            return "", []
        
        try:
            logger.info(f"🔍 RAG Query: {message[:50]}...")
            context, sources = self.rag_service.get_context_for_query(
                message, 
                n_results=n_results
            )
            logger.info(f"✅ RAG Retrieved: {len(sources)} documents, context length: {len(context)}")
            if sources:
                logger.info(f"📚 Sources: {[s.get('source', 'unknown') for s in sources]}")
            return context, sources
        except Exception as e:
            logger.error(f"RAG query error: {e}", exc_info=True)
            return "", []
    
    def get_response(self, message: str, user_id: str = None, language: str = "en") -> Dict:
        """
        Get AI response to user message (RAG-enhanced when available)
        Returns: {response: str, confidence: float, source: str, rag_used: bool, sources: list}
        """
        logger.info(f"💬 Chatbot get_response called: message='{message[:50]}...', language={language}, rag_enabled={self.rag_enabled}")
        
        # Get RAG context if available
        rag_context = ""
        rag_sources = []
        rag_used = False
        
        if self.rag_enabled:
            try:
                logger.info("🔍 Attempting to get RAG context...")
                rag_context, rag_sources = self._get_rag_context(message)
                if rag_context:
                    rag_used = True
                    logger.info(f"✅ RAG context retrieved: {len(rag_sources)} relevant documents, context length: {len(rag_context)}")
                else:
                    logger.info("⚠️ RAG returned empty context")
            except Exception as e:
                logger.warning(f"RAG context retrieval failed: {e}", exc_info=True)
        else:
            logger.info("❌ RAG is not enabled, skipping RAG context retrieval")
        
        try:
            logger.info(f"🤖 Using mode: {self.mode}")
            if self.mode == "openai":
                result = self._get_openai_response(message, user_id, language, rag_context)
            elif self.mode == "gemini":
                result = self._get_gemini_response(message, user_id, language, rag_context)
            elif self.mode == "transformers":
                result = self._get_transformers_response(message, user_id, language)
            else:
                logger.info(f"📝 Using rule-based response with RAG context length: {len(rag_context)}")
                result = self._get_rule_based_response(message, language, rag_context)
            
            # Add RAG information to result
            result['rag_used'] = rag_used
            result['rag_sources'] = rag_sources if rag_used else []
            
            logger.info(f"✅ Response generated: confidence={result.get('confidence')}, source={result.get('source')}, rag_used={rag_used}")
            return result
        except Exception as e:
            logger.error(f"Chatbot error: {e}", exc_info=True)
            fallback = self._get_rule_based_response(message, language)
            fallback['rag_used'] = False
            fallback['rag_sources'] = []
            return fallback
    
    def _get_openai_response(self, message: str, user_id: str, language: str, rag_context: str = "") -> Dict:
        """Get response from OpenAI GPT (RAG-enhanced if context available)"""
        try:
            # Create agriculture-specific prompt with optional RAG context
            system_prompt = f"""You are an expert agricultural AI assistant for farmers. 
            Provide practical, accurate advice about:
            - Crop diseases and their treatment
            - Fertilizer recommendations
            - Pest control methods
            - Irrigation and water management
            - Best farming practices
            - Weather-related crop care
            
            Language: {language}
            Keep responses concise and practical. Use simple farmer-friendly language."""
            
            # Add RAG context if available
            if rag_context:
                system_prompt += f"\n\nRelevant Knowledge Base Information:\n{rag_context}\n\nUse this information to provide accurate, evidence-based answers."
            
            # Get or create conversation memory
            if user_id not in self.conversation_memory:
                self.conversation_memory[user_id] = ConversationBufferMemory()
            
            conversation = ConversationChain(
                llm=self.llm,
                memory=self.conversation_memory[user_id],
                verbose=False
            )
            
            response = conversation.predict(input=f"{system_prompt}\n\nUser: {message}")
            
            return {
                "response": response,
                "confidence": 0.95 if rag_context else 0.90,
                "source": "OpenAI GPT-3.5" + (" + RAG" if rag_context else ""),
                "mode": "ai"
            }
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return self._get_rule_based_response(message, language, rag_context)
    
    def _get_gemini_response(self, message: str, user_id: str, language: str, rag_context: str = "") -> Dict:
        """Get response from Google Gemini (RAG-enhanced if context available)"""
        try:
            prompt = f"""You are an agricultural expert AI. Answer this farming question in {language} language:
            
            Question: {message}
            """
            
            # Add RAG context if available
            if rag_context:
                prompt += f"\n\nRelevant Knowledge Base Information:\n{rag_context}\n\nProvide a concise, practical answer based on this information."
            else:
                prompt += "\n\nProvide a concise, practical answer suitable for farmers."
            
            response = self.llm.generate_content(prompt)
            
            return {
                "response": response.text,
                "confidence": 0.93 if rag_context else 0.88,
                "source": "Google Gemini" + (" + RAG" if rag_context else ""),
                "mode": "ai"
            }
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return self._get_rule_based_response(message, language, rag_context)
    
    def _get_transformers_response(self, message: str, user_id: str, language: str) -> Dict:
        """Get response from local Transformers model"""
        try:
            prompt = f"Agricultural expert: {message}\nAnswer:"
            response = self.llm(prompt, max_length=150, num_return_sequences=1)
            text = response[0]['generated_text'].replace(prompt, '').strip()
            
            return {
                "response": text,
                "confidence": 0.80,
                "source": "Local AI Model",
                "mode": "ai"
            }
        except Exception as e:
            logger.error(f"Transformers error: {e}")
            return self._get_rule_based_response(message, language)
    
    def _get_rule_based_response(self, message: str, language: str = "en", rag_context: str = "") -> Dict:
        """Enhanced rule-based chatbot with pattern matching and optional RAG context"""
        
        message_lower = message.lower()
        
        # If RAG context is available, prioritize it as the main response
        if rag_context and len(rag_context.strip()) > 50:
            # RAG context is substantial, use it as primary response
            # Format it nicely for the user
            formatted_response = self._format_rag_response(rag_context, message_lower, language)
            
            return {
                "response": formatted_response,
                "confidence": 0.90,
                "source": "Knowledge Base + RAG",
                "mode": "rule-based-rag"
            }
        else:
            # No RAG context or it's too short, use pattern-based response only
            response_text = self._get_pattern_based_response(message_lower, language)
            
            return {
                "response": response_text,
                "confidence": 0.85,
                "source": "Knowledge Base",
                "mode": "rule-based"
            }
    
    def _format_rag_response(self, rag_context: str, message: str, language: str) -> str:
        """Format RAG context into a user-friendly response"""
        
        # Clean up the RAG context
        context_parts = rag_context.split('\n\n')
        
        # Create a structured response
        if language == "hi":
            intro = "आपके प्रश्न के आधार पर यहाँ जानकारी है:\n\n"
            tip = "\n\n💡 सुझाव: अधिक विशिष्ट सलाह के लिए, आप रोग पहचान फीचर का उपयोग कर सकते हैं।"
        elif language == "te":
            intro = "మీ ప్రశ్న ఆధారంగా ఇక్కడ సమాచారం:\n\n"
            tip = "\n\n💡 చిట్కా: మరింత నిర్దిష్ట సలహా కోసం, మీరు వ్యాధి గుర్తింపు ఫీచర్‌ను ఉపయోగించవచ్చు।"
        elif language == "ta":
            intro = "உங்கள் கேள்வியின் அடிப்படையில் இங்கே தகவல்:\n\n"
            tip = "\n\n💡 உதவிக்குறிப்பு: மேலும் குறிப்பிட்ட ஆலோசனைக்கு, நீங்கள் நோய் கண்டறிதல் அம்சத்தைப் பயன்படுத்தலாம்।"
        else:  # English
            intro = "Based on your question, here's what I found:\n\n"
            tip = "\n\n💡 Tip: For more specific advice, you can use the Disease Detection feature or ask follow-up questions!"
        
        # Limit context to avoid overwhelming response
        formatted_context = '\n\n'.join(context_parts[:3])  # Use top 3 relevant chunks
        
        # Combine intro + context + tip
        response = intro + formatted_context + tip
        
        return response
    
    def _get_pattern_based_response(self, message: str, language: str = "en") -> str:
        """Get response based on pattern matching in specified language"""
        
        # Multi-language responses
        responses = {
            "en": self._get_english_response(message),
            "hi": self._get_hindi_response(message),
            "te": self._get_telugu_response(message),
            "ta": self._get_tamil_response(message)
        }
        
        return responses.get(language, responses["en"])
    
    def _get_english_response(self, message: str) -> str:
        """English responses"""
        
        # Greetings
        if any(word in message for word in ['hello', 'hi', 'hey', 'namaste']):
            return "Hello! I'm AgriSmart AI Assistant. I can help you with crop diseases, fertilizers, irrigation, pest control, and farming advice. What would you like to know?"
        
        # Disease detection
        if any(word in message for word in ['disease', 'sick', 'problem', 'leaf', 'spot', 'rot']):
            return "I can help identify crop diseases! Please upload a clear photo of the affected plant leaf using the Disease Detection feature. I can recognize 38+ different plant diseases and provide treatment recommendations."
        
        # Weather
        if any(word in message for word in ['weather', 'rain', 'temperature', 'forecast']):
            return "Check the Weather section for 7-day forecasts and crop-specific alerts. I provide temperature, rainfall, humidity, and wind speed predictions to help you plan your farming activities."
        
        # Market prices
        if any(word in message for word in ['price', 'market', 'sell', 'cost', 'mandi']):
            return "Visit the Market Prices section to see current rates and 7-day price predictions for various crops. This helps you decide the best time to sell your produce for maximum profit."
        
        # Fertilizer
        if any(word in message for word in ['fertilizer', 'nutrient', 'npk', 'manure', 'compost']):
            return "For fertilizers: Use balanced NPK (19:19:19) @ 2g/liter every 15 days. Apply organic compost @ 100g/plant monthly. For micronutrients, spray once a month. Soil testing is recommended for precise recommendations."
        
        # Irrigation
        if any(word in message for word in ['water', 'irrigation', 'watering', 'drip']):
            return "Irrigation tips: Most crops need 1-2 inches of water per week. Water deeply but less frequently. Drip irrigation saves 50% water compared to flood irrigation. Water in early morning to reduce fungal diseases."
        
        # Pest control
        if any(word in message for word in ['pest', 'insect', 'bug', 'caterpillar', 'aphid']):
            return "For pest control: Try neem oil spray (5ml/liter) as organic option. Remove affected parts. Use yellow sticky traps. For severe infestations, consult the disease detection feature or use appropriate pesticides as per local agricultural guidelines."
        
        # Tomato specific
        if 'tomato' in message:
            return "Tomato care: Space plants 24-30 inches apart. Water at soil level. Use balanced NPK during growth, high potassium for fruiting. Watch for early blight, late blight, and bacterial spot. Upload leaf photos if you see any spots or discoloration."
        
        # Thank you
        if any(word in message for word in ['thank', 'thanks', 'appreciate']):
            return "You're welcome! Feel free to ask more questions anytime. Happy farming! 🌱"
        
        # Default
        return "I'm here to help with your farming questions! You can ask me about:\n• Crop diseases and treatments\n• Fertilizer recommendations\n• Irrigation and watering\n• Pest control\n• Weather forecasts\n• Market prices\n• General farming tips\n\nWhat would you like to know?"
    
    def _get_hindi_response(self, message: str) -> str:
        """Hindi responses"""
        
        if any(word in message for word in ['hello', 'नमस्ते', 'हाय']):
            return "नमस्ते! मैं AgriSmart AI सहायक हूं। मैं फसल रोगों, उर्वरकों, सिंचाई और खेती की सलाह में मदद कर सकता हूं। आप क्या जानना चाहेंगे?"
        
        if any(word in message for word in ['रोग', 'बीमारी', 'समस्या']):
            return "मैं फसल रोगों की पहचान कर सकता हूं! कृपया रोग पहचान फीचर का उपयोग करके प्रभावित पत्ती की तस्वीर अपलोड करें। मैं 38+ विभिन्न पौधों की बीमारियों को पहचान सकता हूं और उपचार सुझा सकता हूं।"
        
        return "मैं यहां आपके खेती के सवालों में मदद के लिए हूं। आप पूछ सकते हैं:\n• फसल रोग और उपचार\n• उर्वरक सिफारिशें\n• सिंचाई\n• कीट नियंत्रण\n• मौसम पूर्वानुमान\n• बाजार मूल्य"
    
    def _get_telugu_response(self, message: str) -> str:
        """Telugu responses"""
        
        if any(word in message for word in ['hello', 'హలో', 'నమస్కారం']):
            return "నమస్కారం! నేను AgriSmart AI సహాయకుడిని. నేను పంట వ్యాధులు, ఎరువులు, నీటిపారుదల మరియు వ్యవసాయ సలహాలో సహాయం చేయగలను. మీరు ఏమి తెలుసుకోవాలనుకుంటున్నారు?"
        
        if any(word in message for word in ['వ్యాధి', 'సమస్య', 'రోగం']):
            return "నేను పంట వ్యాధులను గుర్తించగలను! దయచేసి వ్యాధి గుర్తింపు ఫీచర్ ఉపయోగించి ప్రభావిత ఆకు యొక్క స్పష్టమైన ఫోటోను అప్‌లోడ్ చేయండి. నేను 38+ విభిన్న మొక్కల వ్యాధులను గుర్తించి చికిత్స సిఫార్సులను అందించగలను."
        
        return "నేను మీ వ్యవసాయ ప్రశ్నలకు సహాయం చేయడానికి ఇక్కడ ఉన్నాను. మీరు అడగవచ్చు:\n• పంట వ్యాధులు మరియు చికిత్సలు\n• ఎరువుల సిఫార్సులు\n• నీటిపారుదల\n• తెగులు నియంత్రణ\n• వాతావరణ సూచన\n• మార్కెట్ ధరలు"
    
    def _get_tamil_response(self, message: str) -> str:
        """Tamil responses"""
        
        if any(word in message for word in ['hello', 'வணக்கம்', 'ஹலோ']):
            return "வணக்கம்! நான் AgriSmart AI உதவியாளர். நான் பயிர் நோய்கள், உரங்கள், நீர்ப்பாசனம் மற்றும் விவசாய ஆலோசனையில் உதவ முடியும். நீங்கள் என்ன தெரிந்துகொள்ள விரும்புகிறீர்கள்?"
        
        if any(word in message for word in ['நோய்', 'பிரச்சனை', 'வியாதி']):
            return "நான் பயிர் நோய்களை அடையாளம் காண முடியும்! தயவுசெய்து நோய் கண்டறிதல் அம்சத்தைப் பயன்படுத்தி பாதிக்கப்பட்ட இலையின் தெளிவான புகைப்படத்தை பதிவேற்றவும். நான் 38+ வெவ்வேறு தாவர நோய்களை அடையாளம் கண்டு சிகிச்சை பரிந்துரைகளை வழங்க முடியும்."
        
        return "உங்கள் விவசாய கேள்விகளுக்கு உதவ நான் இங்கு இருக்கிறேன். நீங்கள் கேட்கலாம்:\n• பயிர் நோய்கள் மற்றும் சிகிச்சை\n• உர பரிந்துரைகள்\n• நீர்ப்பாசனம்\n• பூச்சி கட்டுப்பாடு\n• வானிலை முன்னறிவிப்பு\n• சந்தை விலைகள்"

# Global instance
ai_chatbot = AIAgriChatbot()
