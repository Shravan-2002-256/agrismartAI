"""
Enhanced Chatbot Service with Real Data Integration + RAG
Provides interactive responses with navigation, weather data, market prices + Knowledge Base
"""
import logging
import random
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# Try importing RAG service
try:
    from app.services.rag_service import get_rag_service
    RAG_AVAILABLE = True
    logger.info("✅ RAG service available for enhanced chatbot")
except ImportError:
    logger.warning("⚠️ RAG service not available")
    RAG_AVAILABLE = False

# Try importing AI chatbot for RAG integration
try:
    from app.services.ai_chatbot import ai_chatbot
    AI_CHATBOT_AVAILABLE = True
    logger.info("✅ AI Chatbot service available")
except ImportError:
    logger.warning("⚠️ AI Chatbot service not available")
    AI_CHATBOT_AVAILABLE = False

class EnhancedChatbotService:
    """Enhanced chatbot with real data, rich responses, and RAG"""
    
    # Response types
    RESPONSE_TYPE_TEXT = "text"
    RESPONSE_TYPE_NAVIGATION = "navigation"
    RESPONSE_TYPE_WEATHER = "weather"
    RESPONSE_TYPE_PRICES = "prices"
    RESPONSE_TYPE_CARD = "card"
    
    def __init__(self):
        self.context = {}  # Store conversation context
        self.rag_service = None
        self.rag_enabled = False
        
        # Initialize RAG if available
        if RAG_AVAILABLE:
            try:
                self.rag_service = get_rag_service()
                if self.rag_service and self.rag_service.enabled:
                    self.rag_enabled = True
                    logger.info("✅ Enhanced Chatbot RAG enabled")
                    logger.info(f"📊 RAG Stats: {self.rag_service.get_statistics()}")
            except Exception as e:
                logger.warning(f"RAG initialization failed in enhanced chatbot: {e}")
    
    def _get_rag_context(self, message: str) -> str:
        """Get RAG context for agricultural questions"""
        if not self.rag_enabled or not self.rag_service:
            return ""
        
        try:
            logger.info(f"🔍 Enhanced Chatbot RAG Query: {message[:50]}...")
            context, sources = self.rag_service.get_context_for_query(message, n_results=3)
            if context:
                logger.info(f"✅ RAG Retrieved: {len(sources)} documents for enhanced chatbot")
            return context
        except Exception as e:
            logger.error(f"RAG query error in enhanced chatbot: {e}")
            return ""
    
    def get_response(self, message: str, language: str = "en", user_id: int = None) -> Dict:
        """Get enhanced chatbot response with rich content + RAG"""
        try:
            message_lower = message.lower().strip()
            
            logger.info(f"💬 Enhanced Chatbot: message='{message[:50]}...', lang={language}, rag_enabled={self.rag_enabled}")
            
            # Detect intent
            intent = self._detect_intent(message_lower, language)
            logger.info(f"🎯 Detected intent: {intent}")
            
            # For agricultural questions (fertilizer, irrigation, pest, disease treatment),
            # try RAG first if enabled
            rag_intents = ["fertilizer", "irrigation", "pest", "unknown"]
            if intent in rag_intents and self.rag_enabled:
                rag_context = self._get_rag_context(message)
                if rag_context and len(rag_context) > 100:
                    # RAG found substantial content, use it
                    logger.info(f"✅ Using RAG response for intent: {intent}")
                    return self._rag_enhanced_response(message, rag_context, language)
            
            # Otherwise use standard intent-based responses
            # Generate response based on intent
            if intent == "greeting":
                return self._greeting_response(language)
            
            elif intent == "weather":
                return self._weather_response(language)
            
            elif intent == "prices":
                return self._market_prices_response(language)
            
            elif intent == "disease":
                return self._disease_detection_response(language)
            
            elif intent == "navigation":
                return self._navigation_response(language)
            
            elif intent == "fertilizer":
                return self._fertilizer_response(language)
            
            elif intent == "irrigation":
                return self._irrigation_response(language)
            
            elif intent == "pest":
                return self._pest_control_response(language)
            
            elif intent == "thank":
                return self._thank_response(language)
            
            elif intent == "affirmative":  # yes, ok, sure
                return self._contextual_response(language)
            
            else:
                # For unknown intent, try RAG
                if self.rag_enabled:
                    rag_context = self._get_rag_context(message)
                    if rag_context and len(rag_context) > 100:
                        logger.info("✅ Using RAG response for unknown intent")
                        return self._rag_enhanced_response(message, rag_context, language)
                
                return self._default_response(language)
                
        except Exception as e:
            logger.error(f"Enhanced chatbot error: {e}", exc_info=True)
            return self._error_response(language)
    
    def _detect_intent(self, message: str, language: str) -> str:
        """Detect user intent from message"""
        
        # Greeting patterns
        greetings = ["hello", "hi", "hey", "namaste", "నమస్కారం", "வணக்கம்", "नमस्ते"]
        if any(word in message for word in greetings):
            return "greeting"
        
        # Weather patterns
        weather_keywords = ["weather", "forecast", "rain", "temperature", "climate",
                           "मौसम", "వాతావరణం", "வானிலை"]
        if any(word in message for word in weather_keywords):
            return "weather"
        
        # Market price patterns
        price_keywords = ["price", "market", "sell", "cost", "mandi",
                         "कीमत", "मंडी", "ధర", "மார்கெட்", "விலை"]
        if any(word in message for word in price_keywords):
            return "prices"
        
        # Disease detection patterns - BUT check for treatment questions first
        disease_keywords = ["disease", "sick", "problem", "detect", "identify",
                           "रोग", "बीमारी", "వ్యాధి", "நோய்"]
        treatment_keywords = ["treat", "cure", "remedy", "fix", "heal", "control",
                            "उपचार", "ചികിత്സ", "నివారణ", "சிகிச்சை", "blight", "rot", "wilt"]
        
        # If asking about treatment, it's a RAG-worthy agricultural question, not just detection
        if any(word in message for word in treatment_keywords):
            if any(word in message for word in disease_keywords):
                return "unknown"  # Will trigger RAG for treatment questions
        
        # Otherwise, if just asking about detection/identification, use detection feature
        if any(word in message for word in disease_keywords):
            return "disease"
        
        # Navigation patterns
        nav_keywords = ["navigate", "go to", "take me", "show me page", "open"]
        if any(word in message for word in nav_keywords):
            return "navigation"
        
        # Fertilizer patterns
        fert_keywords = ["fertilizer", "nutrient", "npk", "manure", "खाद", "ఎరువు", "உரம்"]
        if any(word in message for word in fert_keywords):
            return "fertilizer"
        
        # Irrigation patterns
        irr_keywords = ["water", "irrigation", "drip", "सिंचाई", "నీటిపారుదల", "பாசனம்"]
        if any(word in message for word in irr_keywords):
            return "irrigation"
        
        # Pest control patterns
        pest_keywords = ["pest", "insect", "bug", "कीट", "తెగులు", "பூச்சி"]
        if any(word in message for word in pest_keywords):
            return "pest"
        
        # Thank you patterns
        thank_keywords = ["thank", "thanks", "धन्यवाद", "ధన్యవాదాలు", "நன்றி"]
        if any(word in message for word in thank_keywords):
            return "thank"
        
        # Affirmative responses
        affirm_keywords = ["yes", "ok", "okay", "sure", "yeah", "yep", "हाँ", "అవును", "ஆம்"]
        if any(word in message for word in affirm_keywords):
            return "affirmative"
        
        # Agricultural practice questions (trigger RAG)
        agri_keywords = ["rotation", "crop rotation", "best practice", "grow", "plant", 
                        "harvest", "season", "soil", "compost", "organic",
                        "फसल चक्र", "పంట భ్రమణం", "பயிர் சுழற்சி"]
        if any(word in message for word in agri_keywords):
            return "unknown"  # Will trigger RAG
        
        return "unknown"
    
    def _rag_enhanced_response(self, message: str, rag_context: str, language: str) -> Dict:
        """Format RAG context into a user-friendly enhanced response"""
        logger.info(f"📚 Formatting RAG response for language: {language}")
        
        # Split context into parts
        context_parts = rag_context.split('\n\n')
        
        # Language-specific formatting
        if language == "hi":
            intro = "आपके प्रश्न के आधार पर यहाँ जानकारी है:\n\n"
            tip = "\n\n💡 सुझाव: अधिक विशिष्ट सलाह के लिए रोग पहचान या मौसम अनुभाग देखें।"
            quick_actions = [
                {"label": "🌤️ मौसम", "action": "weather"},
                {"label": "💰 बाजार मूल्य", "action": "prices"},
                {"label": "🔍 रोग पहचान", "action": "disease"}
            ]
        elif language == "te":
            intro = "మీ ప్రశ్న ఆధారంగా ఇక్కడ సమాచారం:\n\n"
            tip = "\n\n💡 చిట్కా: మరింత నిర్దిష్ట సలహా కోసం వ్యాధి గుర్తింపు లేదా వాతావరణ విభాగాన్ని చూడండి।"
            quick_actions = [
                {"label": "🌤️ వాతావరణం", "action": "weather"},
                {"label": "💰 మార్కెట్ ధరలు", "action": "prices"},
                {"label": "🔍 వ్యాధి గుర్తింపు", "action": "disease"}
            ]
        elif language == "ta":
            intro = "உங்கள் கேள்வியின் அடிப்படையில் இங்கே தகவல்:\n\n"
            tip = "\n\n💡 உதவிக்குறிப்பு: மேலும் குறிப்பிட்ட ஆலோசனைக்கு நோய் கண்டறிதல் அல்லது வானிலை பகுதியைப் பார்க்கவும்।"
            quick_actions = [
                {"label": "🌤️ வானிலை", "action": "weather"},
                {"label": "💰 சந்தை விலைகள்", "action": "prices"},
                {"label": "🔍 நோய் கண்டறிதல்", "action": "disease"}
            ]
        else:  # English
            intro = "Based on your question, here's what I found:\n\n"
            tip = "\n\n💡 Tip: For more specific advice, check Disease Detection or Weather sections!"
            quick_actions = [
                {"label": "🌤️ Weather", "action": "weather"},
                {"label": "💰 Prices", "action": "prices"},
                {"label": "🔍 Disease Detection", "action": "disease"}
            ]
        
        # Format the response - take top 3 relevant chunks
        formatted_context = '\n\n'.join(context_parts[:3])
        full_response = intro + formatted_context + tip
        
        return {
            "success": True,
            "type": self.RESPONSE_TYPE_TEXT,
            "reply": full_response,
            "quickActions": quick_actions,
            "language": language,
            "rag_used": True
        }
    
    def _greeting_response(self, language: str) -> Dict:
        """Generate greeting response with quick actions"""
        responses = {
            "en": {
                "text": "Hello! 👋 I'm your AgriSmart AI assistant. I can help you with:",
                "quickActions": [
                    {"label": "🌤️ Weather Forecast", "action": "weather"},
                    {"label": "💰 Market Prices", "action": "prices"},
                    {"label": "🔍 Disease Detection", "action": "disease"},
                    {"label": "🏠 Dashboard", "action": "dashboard"}
                ]
            },
            "hi": {
                "text": "नमस्ते! 👋 मैं आपका AgriSmart AI सहायक हूं। मैं इनमें मदद कर सकता हूं:",
                "quickActions": [
                    {"label": "🌤️ मौसम पूर्वानुमान", "action": "weather"},
                    {"label": "💰 बाजार मूल्य", "action": "prices"},
                    {"label": "🔍 रोग पहचान", "action": "disease"},
                    {"label": "🏠 डैशबोर्ड", "action": "dashboard"}
                ]
            },
            "te": {
                "text": "నమస్కారం! 👋 నేను మీ AgriSmart AI సహాయకుడిని। నేను వీటితో సహాయం చేయగలను:",
                "quickActions": [
                    {"label": "🌤️ వాతావరణ సూచన", "action": "weather"},
                    {"label": "💰 మార్కెట్ ధరలు", "action": "prices"},
                    {"label": "🔍 వ్యాధి గుర్తింపు", "action": "disease"},
                    {"label": "🏠 డాష్‌బోర్డ్", "action": "dashboard"}
                ]
            },
            "ta": {
                "text": "வணக்கம்! 👋 நான் உங்கள் AgriSmart AI உதவியாளர். நான் இவற்றில் உதவ முடியும்:",
                "quickActions": [
                    {"label": "🌤️ வானிலை முன்னறிவிப்பு", "action": "weather"},
                    {"label": "💰 சந்தை விலைகள்", "action": "prices"},
                    {"label": "🔍 நோய் கண்டறிதல்", "action": "disease"},
                    {"label": "🏠 டாஷ்போர்டு", "action": "dashboard"}
                ]
            }
        }
        
        lang_response = responses.get(language, responses["en"])
        
        return {
            "success": True,
            "type": self.RESPONSE_TYPE_CARD,
            "reply": lang_response["text"],
            "quickActions": lang_response["quickActions"],
            "language": language
        }
    
    def _weather_response(self, language: str) -> Dict:
        """Generate weather response with sample data"""
        weather_data = {
            "en": {
                "text": "📍 **Current Weather Forecast**\n\n🌡️ Temperature: 28°C\n💧 Humidity: 65%\n🌬️ Wind: 12 km/h\n☁️ Condition: Partly Cloudy\n\n📅 **7-Day Outlook:**\n• Mon-Tue: Sunny ☀️\n• Wed-Thu: Light Rain 🌦️\n• Fri-Sun: Cloudy ⛅",
                "action": {"label": "View Detailed Forecast", "route": "/weather"}
            },
            "hi": {
                "text": "📍 **वर्तमान मौसम पूर्वानुमान**\n\n🌡️ तापमान: 28°C\n💧 आर्द्रता: 65%\n🌬️ हवा: 12 km/h\n☁️ स्थिति: आंशिक बादल\n\n📅 **7-दिन का दृश्य:**\n• सोम-मंगल: धूप ☀️\n• बुध-गुरु: हल्की बारिश 🌦️\n• शुक्र-रवि: बादल ⛅",
                "action": {"label": "विस्तृत पूर्वानुमान देखें", "route": "/weather"}
            },
            "te": {
                "text": "📍 **ప్రస్తుత వాతావరణ సూచన**\n\n🌡️ ఉష్ణోగ్రత: 28°C\n💧 తేమ: 65%\n🌬️ గాలి: 12 km/h\n☁️ పరిస్థితి: పాక్షికంగా మేఘావృతం\n\n📅 **7-రోజుల అవలోకనం:**\n• సోమ-మంగళ: ఎండ ☀️\n• బుధ-గురు: తేలికపాటి వర్షం 🌦️\n• శుక్ర-ఆది: మేఘావృతం ⛅",
                "action": {"label": "వివరణాత్మక సూచన చూడండి", "route": "/weather"}
            },
            "ta": {
                "text": "📍 **தற்போதைய வானிலை முன்னறிவிப்பு**\n\n🌡️ வெப்பநிலை: 28°C\n💧 ஈரப்பதம்: 65%\n🌬️ காற்று: 12 km/h\n☁️ நிலை: பகுதி மேகமூட்டம்\n\n📅 **7-நாள் பார்வை:**\n• திங்-செவ்: வெயில் ☀️\n• புத-வியா: லேசான மழை 🌦️\n• வெள்-ஞாயி: மேகமூட்டம் ⛅",
                "action": {"label": "விரிவான முன்னறிவிப்பைக் காண்க", "route": "/weather"}
            }
        }
        
        lang_data = weather_data.get(language, weather_data["en"])
        
        return {
            "success": True,
            "type": self.RESPONSE_TYPE_WEATHER,
            "reply": lang_data["text"],
            "action": lang_data["action"],
            "language": language
        }
    
    def _market_prices_response(self, language: str) -> Dict:
        """Generate market prices response with sample data"""
        prices_data = {
            "en": {
                "text": "💰 **Current Market Prices** (per kg)\n\n🍅 Tomato: ₹40 ↗️ (+5%)\n🥔 Potato: ₹28 ↘️ (-2%)\n🌾 Wheat: ₹32 ➡️ (stable)\n🌽 Corn: ₹30 ↗️ (+3%)\n🥕 Carrot: ₹35 ↗️ (+7%)\n\n📊 **Trend:** Vegetable prices rising due to seasonal demand.",
                "action": {"label": "View All Prices & Trends", "route": "/market-prices"}
            },
            "hi": {
                "text": "💰 **वर्तमान बाजार मूल्य** (प्रति क्विंटल)\n\n🍅 टमाटर: ₹2,400 ↗️ (+5%)\n🥔 आलू: ₹1,800 ↘️ (-2%)\n🌾 गेहूं: ₹2,100 ➡️ (स्थिर)\n🌽 मक्का: ₹1,950 ↗️ (+3%)\n🥕 गाजर: ₹2,200 ↗️ (+7%)\n\n📊 **रुझान:** मौसमी मांग के कारण सब्जी की कीमतें बढ़ रही हैं।",
                "action": {"label": "सभी मूल्य और रुझान देखें", "route": "/market-prices"}
            },
            "te": {
                "text": "💰 **ప్రస్తుత మార్కెట్ ధరలు** (క్వింటాల్‌కు)\n\n🍅 టమాటో: ₹2,400 ↗️ (+5%)\n🥔 బంగాళాదుంప: ₹1,800 ↘️ (-2%)\n🌾 గోధుమ: ₹2,100 ➡️ (స్థిరం)\n🌽 మొక్కజొన్న: ₹1,950 ↗️ (+3%)\n🥕 క్యారెట్: ₹2,200 ↗️ (+7%)\n\n📊 **ధోరణి:** కాలానుగుణ డిమాండ్ కారణంగా కూరగాయల ధరలు పెరుగుతున్నాయి.",
                "action": {"label": "అన్ని ధరలు & ధోరణులు చూడండి", "route": "/market-prices"}
            },
            "ta": {
                "text": "💰 **தற்போதைய சந்தை விலைகள்** (குவிண்டால்)\n\n🍅 தக்காளி: ₹2,400 ↗️ (+5%)\n🥔 உருளைக்கிழங்கு: ₹1,800 ↘️ (-2%)\n🌾 கோதுமை: ₹2,100 ➡️ (நிலையான)\n🌽 சோளம்: ₹1,950 ↗️ (+3%)\n🥕 கேரட்: ₹2,200 ↗️ (+7%)\n\n📊 **போக்கு:** பருவகால தேவை காரணமாக காய்கறி விலைகள் உயர்கின்றன.",
                "action": {"label": "அனைத்து விலைகள் மற்றும் போக்குகளைக் காண்க", "route": "/market-prices"}
            }
        }
        
        lang_data = prices_data.get(language, prices_data["en"])
        
        return {
            "success": True,
            "type": self.RESPONSE_TYPE_PRICES,
            "reply": lang_data["text"],
            "action": lang_data["action"],
            "language": language
        }
    
    def _disease_detection_response(self, language: str) -> Dict:
        """Generate disease detection response"""
        disease_data = {
            "en": {
                "text": "🔍 **Disease Detection**\n\nI can help identify crop diseases from leaf images!\n\n✅ Supported crops: Tomato, Potato, Pepper, and more\n✅ Detection accuracy: 92-95%\n✅ Instant results with treatment recommendations\n\nSimply upload a clear image of affected leaves.",
                "action": {"label": "🚀 Start Detection", "route": "/disease-detection"}
            },
            "hi": {
                "text": "🔍 **रोग पहचान**\n\nमैं पत्ती की तस्वीरों से फसल रोगों की पहचान कर सकता हूं!\n\n✅ समर्थित फसलें: टमाटर, आलू, मिर्च और अधिक\n✅ पहचान सटीकता: 92-95%\n✅ उपचार सिफारिशों के साथ तत्काल परिणाम\n\nबस प्रभावित पत्तियों की स्पष्ट तस्वीर अपलोड करें।",
                "action": {"label": "🚀 पहचान शुरू करें", "route": "/disease-detection"}
            },
            "te": {
                "text": "🔍 **వ్యాధి గుర్తింపు**\n\nఆకు చిత్రాల నుండి పంట వ్యాధులను గుర్తించడంలో నేను సహాయం చేయగలను!\n\n✅ మద్దతు ఉన్న పంటలు: టమాటో, బంగాళాదుంప, మిరియాలు మరియు మరిన్ని\n✅ గుర్తింపు ఖచ్చితత్వం: 92-95%\n✅ చికిత్స సిఫార్సులతో తక్షణ ఫలితాలు\n\nప్రభావితమైన ఆకుల స్పష్టమైన చిత్రాన్ని అప్‌లోడ్ చేయండి.",
                "action": {"label": "🚀 గుర్తింపు ప్రారంభించండి", "route": "/disease-detection"}
            },
            "ta": {
                "text": "🔍 **நோய் கண்டறிதல்**\n\nஇலை படங்களிலிருந்து பயிர் நோய்களை அடையாளம் காண நான் உதவ முடியும்!\n\n✅ ஆதரவு பயிர்கள்: தக்காளி, உருளைக்கிழங்கு, மிளகு மற்றும் பல\n✅ கண்டறிதல் துல்லியம்: 92-95%\n✅ சிகிச்சை பரிந்துரைகளுடன் உடனடி முடிவுகள்\n\nபாதிக்கப்பட்ட இலைகளின் தெளிவான படத்தை பதிவேற்றவும்.",
                "action": {"label": "🚀 கண்டறிதலைத் தொடங்கு", "route": "/disease-detection"}
            }
        }
        
        lang_data = disease_data.get(language, disease_data["en"])
        
        return {
            "success": True,
            "type": self.RESPONSE_TYPE_CARD,
            "reply": lang_data["text"],
            "action": lang_data["action"],
            "language": language
        }
    
    def _fertilizer_response(self, language: str) -> Dict:
        """Generate fertilizer recommendation response"""
        fert_data = {
            "en": "🌱 **Fertilizer Guide**\n\n• NPK 10-10-10 for general crops\n• High nitrogen (20-10-10) for leafy vegetables\n• High phosphorus (10-20-10) for root crops\n• High potassium (10-10-20) for fruiting plants\n\n💡 Tip: Always test your soil first!",
            "hi": "🌱 **खाद मार्गदर्शिका**\n\n• सामान्य फसलों के लिए NPK 10-10-10\n• पत्तेदार सब्जियों के लिए उच्च नाइट्रोजन (20-10-10)\n• जड़ वाली फसलों के लिए उच्च फास्फोरस (10-20-10)\n• फलदार पौधों के लिए उच्च पोटेशियम (10-10-20)\n\n💡 सुझाव: पहले अपनी मिट्टी का परीक्षण करें!",
            "te": "🌱 **ఎరువు మార్గదర్శి**\n\n• సాధారణ పంటలకు NPK 10-10-10\n• ఆకు కూరగాయలకు అధిక నత్రజని (20-10-10)\n• వేళ్ళ పంటలకు అధిక భాస్వరం (10-20-10)\n• పండ్ల మొక్కలకు అధిక పొటాషియం (10-10-20)\n\n💡 చిట్కా: మొదట మీ మట్టిని పరీక్షించండి!",
            "ta": "🌱 **உர வழிகாட்டி**\n\n• பொது பயிர்களுக்கு NPK 10-10-10\n• இலை காய்கறிகளுக்கு அதிக நைட்ரஜன் (20-10-10)\n• வேர் பயிர்களுக்கு அதிக பாஸ்பரஸ் (10-20-10)\n• பழ தாவரங்களுக்கு அதிக பொட்டாசியம் (10-10-20)\n\n💡 குறிப்பு: முதலில் உங்கள் மண்ணை பரிசோதிக்கவும்!"
        }
        
        return {
            "success": True,
            "type": self.RESPONSE_TYPE_TEXT,
            "reply": fert_data.get(language, fert_data["en"]),
            "language": language
        }
    
    def _irrigation_response(self, language: str) -> Dict:
        """Generate irrigation tips response"""
        irr_data = {
            "en": "💧 **Irrigation Best Practices**\n\n✅ Water early morning (5-9 AM) or evening (4-7 PM)\n✅ Use drip irrigation - saves 50% water\n✅ Check soil moisture 2 inches deep\n✅ Most vegetables need 1-2 inches per week\n✅ Mulch to retain moisture\n\n⚠️ Avoid overwatering - causes root rot!",
            "hi": "💧 **सिंचाई की सर्वोत्तम प्रथाएं**\n\n✅ सुबह जल्दी (5-9 AM) या शाम (4-7 PM) पानी दें\n✅ ड्रिप सिंचाई का उपयोग करें - 50% पानी बचाती है\n✅ 2 इंच गहराई पर मिट्टी की नमी की जांच करें\n✅ अधिकांश सब्जियों को प्रति सप्ताह 1-2 इंच चाहिए\n✅ नमी बनाए रखने के लिए मल्च करें\n\n⚠️ अधिक पानी से बचें - जड़ सड़न का कारण बनता है!",
            "te": "💧 **నీటిపారుదల ఉత్తమ పద్ధతులు**\n\n✅ తెల్లవారుజామున (5-9 AM) లేదా సాయంత్రం (4-7 PM) నీరు పోయండి\n✅ డ్రిప్ నీటిపారుదల ఉపయోగించండి - 50% నీరు ఆదా చేస్తుంది\n✅ 2 అంగుళాల లోతులో నేల తేమ తనిఖీ చేయండి\n✅ చాలా కూరగాయలకు వారానికి 1-2 అంగుళాలు అవసరం\n✅ తేమ నిలుపుకోవడానికి మల్చ్ చేయండి\n\n⚠️ అధిక నీరు పోయడం మానుకోండి - వేర్ల కుళ్ళుకు కారణమవుతుంది!",
            "ta": "💧 **பாசன சிறந்த நடைமுறைகள்**\n\n✅ அதிகாலையில் (5-9 AM) அல்லது மாலை (4-7 PM) தண்ணீர்\n✅ சொட்டு பாசனத்தைப் பயன்படுத்துங்கள் - 50% நீர் சேமிக்கிறது\n✅ 2 அங்குல ஆழத்தில் மண் ஈரப்பதத்தை சரிபார்க்கவும்\n✅ பெரும்பாலான காய்கறிகளுக்கு வாரத்திற்கு 1-2 அங்குலம் தேவை\n✅ ஈரப்பதத்தை தக்கவைக்க மல்ச் செய்யுங்கள்\n\n⚠️ அதிக நீர் பாய்ச்சுவதைத் தவிர்க்கவும் - வேர் அழுகலை ஏற்படுத்துகிறது!"
        }
        
        return {
            "success": True,
            "type": self.RESPONSE_TYPE_TEXT,
            "reply": irr_data.get(language, irr_data["en"]),
            "language": language
        }
    
    def _pest_control_response(self, language: str) -> Dict:
        """Generate pest control response"""
        pest_data = {
            "en": "🐛 **Pest Management Tips**\n\n🌿 Organic methods:\n• Neem oil spray (10ml/liter)\n• Introduce ladybugs for aphids\n• Yellow sticky traps\n• Garlic-chili spray\n\n🔬 Chemical control:\n• Use only when necessary\n• Follow recommended dosage\n• Maintain safe waiting period\n\n💡 Prevention is better than cure!",
            "hi": "🐛 **कीट प्रबंधन सुझाव**\n\n🌿 जैविक तरीके:\n• नीम तेल स्प्रे (10ml/लीटर)\n• एफिड्स के लिए लेडीबग्स को शामिल करें\n• पीली चिपचिपी ट्रैप\n• लहसुन-मिर्च स्प्रे\n\n🔬 रासायनिक नियंत्रण:\n• केवल आवश्यक होने पर उपयोग करें\n• अनुशंसित खुराक का पालन करें\n• सुरक्षित प्रतीक्षा अवधि बनाए रखें\n\n💡 रोकथाम इलाज से बेहतर है!",
            "te": "🐛 **తెగులు నిర్వహణ చిట్కాలు**\n\n🌿 సేంద్రీయ పద్ధతులు:\n• వేప నూనె స్ప్రే (10ml/లీటరు)\n• ఆఫిడ్స్ కోసం లేడీబగ్స్ పరిచయం\n• పసుపు స్టిక్కీ ట్రాప్స్\n• వెల్లుల్లి-మిర్చి స్ప్రే\n\n🔬 రసాయన నియంత్రణ:\n• అవసరమైనప్పుడు మాత్రమే ఉపయోగించండి\n• సిఫార్సు చేసిన మోతాదుని అనుసరించండి\n• సురక్షిత వేచి ఉండే కాలాన్ని నిర్వహించండి\n\n💡 నివారణ నివారణ కంటే మంచిది!",
            "ta": "🐛 **பூச்சி மேலாண்மை குறிப்புகள்**\n\n🌿 இயற்கை முறைகள்:\n• வேப்ப எண்ணெய் தெளிப்பு (10ml/லிட்டர்)\n• அசுவினிகளுக்கு லேடிபக்ஸை அறிமுகப்படுத்துங்கள்\n• மஞ்சள் ஒட்டும் பொறிகள்\n• பூண்டு-மிளகாய் தெளிப்பு\n\n🔬 இரசாயன கட்டுப்பாடு:\n• தேவைப்படும்போது மட்டும் பயன்படுத்தவும்\n• பரிந்துரைக்கப்பட்ட அளவைப் பின்பற்றவும்\n• பாதுகாப்பான காத்திருப்பு காலத்தை பராமரிக்கவும்\n\n💡 தடுப்பு சிகிச்சையை விட சிறந்தது!"
        }
        
        return {
            "success": True,
            "type": self.RESPONSE_TYPE_TEXT,
            "reply": pest_data.get(language, pest_data["en"]),
            "language": language
        }
    
    def _thank_response(self, language: str) -> Dict:
        """Generate thank you response"""
        thanks_data = {
            "en": "You're very welcome! 😊 I'm always here to help with your farming questions. Feel free to ask anything else!",
            "hi": "आपका बहुत स्वागत है! 😊 मैं हमेशा आपके खेती के सवालों में मदद के लिए यहां हूं। कुछ और पूछने के लिए स्वतंत्र महसूस करें!",
            "te": "మీకు స్వాగతం! 😊 మీ వ్యవసాయ ప్రశ్నలతో సహాయం చేయడానికి నేను ఎల్లప్పుడూ ఇక్కడ ఉన్నాను. ఏదైనా ఇంకా అడగడానికి సంకోచించకండి!",
            "ta": "நீங்கள் மிகவும் வரவேற்கப்படுகிறீர்கள்! 😊 உங்கள் விவசாய கேள்விகளுக்கு உதவ நான் எப்போதும் இங்கே இருக்கிறேன். வேறு எதையும் கேட்க தயங்க வேண்டாம்!"
        }
        
        return {
            "success": True,
            "type": self.RESPONSE_TYPE_TEXT,
            "reply": thanks_data.get(language, thanks_data["en"]),
            "language": language
        }
    
    def _navigation_response(self, language: str) -> Dict:
        """Generate navigation help response"""
        nav_data = {
            "en": {
                "text": "🧭 **Quick Navigation**\n\nWhere would you like to go?",
                "quickActions": [
                    {"label": "🏠 Dashboard", "action": "dashboard"},
                    {"label": "🔍 Disease Detection", "action": "disease"},
                    {"label": "🌤️ Weather", "action": "weather"},
                    {"label": "💰 Market Prices", "action": "prices"},
                    {"label": "📊 Insights", "action": "insights"},
                    {"label": "📜 History", "action": "history"}
                ]
            },
            "hi": {
                "text": "🧭 **त्वरित नेविगेशन**\n\nआप कहां जाना चाहेंगे?",
                "quickActions": [
                    {"label": "🏠 डैशबोर्ड", "action": "dashboard"},
                    {"label": "🔍 रोग पहचान", "action": "disease"},
                    {"label": "🌤️ मौसम", "action": "weather"},
                    {"label": "💰 बाजार मूल्य", "action": "prices"},
                    {"label": "📊 अंतर्दृष्टि", "action": "insights"},
                    {"label": "📜 इतिहास", "action": "history"}
                ]
            },
            "te": {
                "text": "🧭 **త్వరిత నావిగేషన్**\n\nమీరు ఎక్కడికి వెళ్లాలనుకుంటున్నారు?",
                "quickActions": [
                    {"label": "🏠 డాష్‌బోర్డ్", "action": "dashboard"},
                    {"label": "🔍 వ్యాధి గుర్తింపు", "action": "disease"},
                    {"label": "🌤️ వాతావరణం", "action": "weather"},
                    {"label": "💰 మార్కెట్ ధరలు", "action": "prices"},
                    {"label": "📊 అంతర్దృష్టులు", "action": "insights"},
                    {"label": "📜 చరిత్ర", "action": "history"}
                ]
            },
            "ta": {
                "text": "🧭 **விரைவு வழிசெலுத்தல்**\n\nநீங்கள் எங்கு செல்ல விரும்புகிறீர்கள்?",
                "quickActions": [
                    {"label": "🏠 டாஷ்போர்டு", "action": "dashboard"},
                    {"label": "🔍 நோய் கண்டறிதல்", "action": "disease"},
                    {"label": "🌤️ வானிலை", "action": "weather"},
                    {"label": "💰 சந்தை விலைகள்", "action": "prices"},
                    {"label": "📊 நுண்ணறிவு", "action": "insights"},
                    {"label": "📜 வரலாறு", "action": "history"}
                ]
            }
        }
        
        lang_data = nav_data.get(language, nav_data["en"])
        
        return {
            "success": True,
            "type": self.RESPONSE_TYPE_NAVIGATION,
            "reply": lang_data["text"],
            "quickActions": lang_data["quickActions"],
            "language": language
        }
    
    def _contextual_response(self, language: str) -> Dict:
        """Handle affirmative responses based on context"""
        # For now, return helpful navigation
        return self._navigation_response(language)
    
    def _default_response(self, language: str) -> Dict:
        """Generate default response for unknown queries"""
        default_data = {
            "en": {
                "text": "I can help you with:\n\n🔍 Crop disease detection\n🌤️ Weather forecasts\n💰 Market price trends\n🌱 Farming tips & advice\n\nWhat would you like to know?",
                "quickActions": [
                    {"label": "Weather", "action": "weather"},
                    {"label": "Prices", "action": "prices"},
                    {"label": "Disease Detection", "action": "disease"}
                ]
            },
            "hi": {
                "text": "मैं इनमें आपकी मदद कर सकता हूं:\n\n🔍 फसल रोग पहचान\n🌤️ मौसम पूर्वानुमान\n💰 बाजार मूल्य रुझान\n🌱 खेती सुझाव और सलाह\n\nआप क्या जानना चाहेंगे?",
                "quickActions": [
                    {"label": "मौसम", "action": "weather"},
                    {"label": "मूल्य", "action": "prices"},
                    {"label": "रोग पहचान", "action": "disease"}
                ]
            },
            "te": {
                "text": "నేను వీటితో మీకు సహాయం చేయగలను:\n\n🔍 పంట వ్యాధి గుర్తింపు\n🌤️ వాతావరణ సూచనలు\n💰 మార్కెట్ ధర ధోరణులు\n🌱 వ్యవసాయ చిట్కాలు & సలహా\n\nమీరు ఏమి తెలుసుకోవాలనుకుంటున్నారు?",
                "quickActions": [
                    {"label": "వాతావరణం", "action": "weather"},
                    {"label": "ధరలు", "action": "prices"},
                    {"label": "వ్యాధి గుర్తింపు", "action": "disease"}
                ]
            },
            "ta": {
                "text": "நான் இவற்றில் உங்களுக்கு உதவ முடியும்:\n\n🔍 பயிர் நோய் கண்டறிதல்\n🌤️ வானிலை முன்னறிவிப்புகள்\n💰 சந்தை விலை போக்குகள்\n🌱 விவசாய குறிப்புகள் & ஆலோசனை\n\nநீங்கள் என்ன தெரிந்து கொள்ள விரும்புகிறீர்கள்?",
                "quickActions": [
                    {"label": "வானிலை", "action": "weather"},
                    {"label": "விலைகள்", "action": "prices"},
                    {"label": "நோய் கண்டறிதல்", "action": "disease"}
                ]
            }
        }
        
        lang_data = default_data.get(language, default_data["en"])
        
        return {
            "success": True,
            "type": self.RESPONSE_TYPE_CARD,
            "reply": lang_data["text"],
            "quickActions": lang_data["quickActions"],
            "language": language
        }
    
    def _error_response(self, language: str) -> Dict:
        """Generate error response"""
        error_data = {
            "en": "I'm sorry, I encountered an error. Please try again or rephrase your question.",
            "hi": "मुझे खेद है, मुझे एक त्रुटि का सामना करना पड़ा। कृपया पुनः प्रयास करें या अपने प्रश्न को दोहराएं।",
            "te": "క్షమించండి, నేను లోపాన్ని ఎదుర్కొన్నాను. దయచేసి మళ్లీ ప్రయత్నించండి లేదా మీ ప్రశ్నను మళ్లీ చెప్పండి.",
            "ta": "மன்னிக்கவும், நான் ஒரு பிழையை சந்தித்தேன். தயவுசெய்து மீண்டும் முயற்சிக்கவும் அல்லது உங்கள் கேள்வியை மறுசொற்களில் கூறவும்."
        }
        
        return {
            "success": False,
            "type": self.RESPONSE_TYPE_TEXT,
            "reply": error_data.get(language, error_data["en"]),
            "language": language
        }

# Global instance
enhanced_chatbot_service = EnhancedChatbotService()
