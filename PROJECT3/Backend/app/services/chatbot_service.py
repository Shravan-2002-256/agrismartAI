"""
Multi-lingual Chatbot Service (Rule-based with FAQ)
"""
import logging
from typing import Dict, List
import re

logger = logging.getLogger(__name__)

# Multi-language FAQ database
FAQ_DATABASE = {
    "en": {
        "greetings": {
            "patterns": ["hello", "hi", "hey", "good morning", "good evening"],
            "responses": [
                "Hello! I'm AgriSmart AI assistant. How can I help you today?",
                "Hi there! I'm here to help with your farming questions.",
                "Welcome! Ask me anything about crops, diseases, or farming practices."
            ]
        },
        "disease_query": {
            "patterns": ["disease", "sick", "problem", "leaves", "spots"],
            "responses": [
                "To detect crop diseases, please upload a clear image of the affected plant leaves. I can identify 38 different crop diseases!",
                "I can help identify crop diseases. Use the disease detection feature to upload an image of your crop."
            ]
        },
        "weather": {
            "patterns": ["weather", "rain", "temperature", "forecast"],
            "responses": [
                "Check the Weather section for a 7-day forecast and crop-specific alerts for your location.",
                "I provide weather forecasts tailored for farmers, including alerts for frost, heavy rain, and extreme heat."
            ]
        },
        "prices": {
            "patterns": ["price", "market", "sell", "cost"],
            "responses": [
                "Visit the Market Prices section to see current prices and 7-day predictions for various crops.",
                "I can show you market price trends and predictions to help you decide the best time to sell your crops."
            ]
        },
        "fertilizer": {
            "patterns": ["fertilizer", "nutrients", "npk", "manure"],
            "responses": [
                "Fertilizer needs depend on your crop type and soil condition. For tomatoes: Use balanced NPK (10-10-10) during growth, then high potassium for fruiting.",
                "I recommend getting a soil test first. Generally, organic compost improves soil health for all crops."
            ]
        },
        "irrigation": {
            "patterns": ["water", "irrigation", "watering"],
            "responses": [
                "Most vegetables need 1-2 inches of water per week. Water deeply but less frequently to encourage deep root growth.",
                "Drip irrigation is most efficient, saving up to 50% water compared to flood irrigation."
            ]
        },
        "pest": {
            "patterns": ["pest", "insect", "bug", "caterpillar"],
            "responses": [
                "For pest control, try neem oil spray (organic) or consult the disease detection for specific pests affecting your crops.",
                "Integrated Pest Management (IPM) combines biological, cultural, and chemical methods for best results."
            ]
        },
        "thank": {
            "patterns": ["thank", "thanks", "appreciate"],
            "responses": [
                "You're welcome! Feel free to ask more questions anytime.",
                "Happy to help! Good luck with your farming."
            ]
        }
    },
    "hi": {
        "greetings": {
            "patterns": ["नमस्ते", "हेलो", "हाय"],
            "responses": [
                "नमस्ते! मैं AgriSmart AI सहायक हूं। आज मैं आपकी कैसे मदद कर सकता हूं?",
                "नमस्कार! मैं खेती से संबंधित आपके सवालों में मदद के लिए हूं।"
            ]
        },
        "disease_query": {
            "patterns": ["रोग", "बीमारी", "समस्या", "पत्ते"],
            "responses": [
                "फसल रोगों का पता लगाने के लिए, कृपया प्रभावित पौधे की पत्तियों की स्पष्ट तस्वीर अपलोड करें।",
                "मैं 38 विभिन्न फसल रोगों की पहचान कर सकता हूं। रोग पहचान सुविधा का उपयोग करें।"
            ]
        },
        "weather": {
            "patterns": ["मौसम", "बारिश", "तापमान"],
            "responses": [
                "7 दिनों के मौसम पूर्वानुमान के लिए मौसम अनुभाग देखें।",
                "मैं किसानों के लिए मौसम पूर्वानुमान प्रदान करता हूं।"
            ]
        },
        "prices": {
            "patterns": ["कीमत", "मंडी", "बेचना", "दाम"],
            "responses": [
                "विभिन्न फसलों की वर्तमान कीमतें और भविष्यवाणियां देखने के लिए बाजार कीमत अनुभाग पर जाएं।",
                "मैं आपको बाजार मूल्य रुझान दिखा सकता हूं।"
            ]
        },
        "fertilizer": {
            "patterns": ["खाद", "उर्वरक", "पोषक"],
            "responses": [
                "खाद की आवश्यकता फसल के प्रकार और मिट्टी की स्थिति पर निर्भर करती है।",
                "मैं पहले मिट्टी परीक्षण कराने की सलाह देता हूं।"
            ]
        },
        "thank": {
            "patterns": ["धन्यवाद", "शुक्रिया"],
            "responses": [
                "आपका स्वागत है! किसी भी समय और सवाल पूछें।",
                "मदद करके खुशी हुई! आपकी खेती के लिए शुभकामनाएं।"
            ]
        }
    },
    "te": {
        "greetings": {
            "patterns": ["నమస్కారం", "హలో", "హాయ్"],
            "responses": [
                "నమస్కారం! నేను AgriSmart AI సహాయకుడిని। ఈరోజు నేను మీకు ఎలా సహాయం చేయగలను?",
                "స్వాగతం! వ్యవసాయ ప్రశ్నలతో సహాయం కోసం నేను ఇక్కడ ఉన్నాను."
            ]
        },
        "disease_query": {
            "patterns": ["వ్యాధి", "సమస్య", "ఆకులు", "మచ్చలు"],
            "responses": [
                "పంట వ్యాధులను గుర్తించడానికి, దయచేసి ప్రభావితమైన మొక్క ఆకుల స్పష్టమైన చిత్రాన్ని అప్‌లోడ్ చేయండి.",
                "నేను 38 వివిధ పంట వ్యాధులను గుర్తించగలను!"
            ]
        },
        "weather": {
            "patterns": ["వాతావరణం", "వర్షం", "ఉష్ణోగ్రత"],
            "responses": [
                "మీ ప్రాంతానికి 7-రోజుల సూచన కోసం వాతావరణ విభాగాన్ని చూడండి.",
                "నేను రైతులకు వాతావరణ సూచనలు అందిస్తాను."
            ]
        },
        "prices": {
            "patterns": ["ధర", "మార్కెట్", "అమ్మడం"],
            "responses": [
                "వివిధ పంటల ప్రస్తుత ధరలు చూడటానికి మార్కెట్ ధరల విభాగాన్ని సందర్శించండి.",
                "మీ పంటలను ఎప్పుడు అమ్మాలో నిర్ణయించడంలో సహాయపడే మార్కెట్ ధర ధోరణులను చూపించగలను."
            ]
        },
        "thank": {
            "patterns": ["ధన్యవాదాలు", "కృతజ్ఞతలు"],
            "responses": [
                "స్వాగతం! ఎప్పుడైనా మరిన్ని ప్రశ్నలు అడగండి.",
                "సహాయం చేయడానికి సంతోషం! మీ వ్యవసాయానికి శుభాకాంక్షలు."
            ]
        }
    },
    "ta": {
        "greetings": {
            "patterns": ["வணக்கம்", "ஹலோ", "ஹாய்"],
            "responses": [
                "வணக்கம்! நான் AgriSmart AI உதவியாளர். இன்று நான் உங்களுக்கு எப்படி உதவ முடியும்?",
                "வரவேற்பு! விவசாய கேள்விகளுக்கு உதவ நான் இங்கே இருக்கிறேன்."
            ]
        },
        "disease_query": {
            "patterns": ["நோய்", "பிரச்சனை", "இலைகள்", "புள்ளிகள்"],
            "responses": [
                "பயிர் நோய்களை கண்டறிய, பாதிக்கப்பட்ட செடியின் இலைகளின் தெளிவான படத்தை பதிவேற்றவும்.",
                "நான் 38 வெவ்வேறு பயிர் நோய்களை அடையாளம் காண முடியும்!"
            ]
        },
        "weather": {
            "patterns": ["வானிலை", "மழை", "வெப்பநிலை"],
            "responses": [
                "உங்கள் பகுதிக்கான 7 நாள் முன்னறிவிப்புக்கு வானிலை பகுதியைப் பார்க்கவும்.",
                "நான் விவசாயிகளுக்கு வானிலை முன்னறிவிப்புகளை வழங்குகிறேன்."
            ]
        },
        "prices": {
            "patterns": ["விலை", "சந்தை", "விற்பனை"],
            "responses": [
                "பல்வேறு பயிர்களின் தற்போதைய விலைகளைப் பார்க்க சந்தை விலை பகுதியைப் பார்வையிடவும்.",
                "உங்கள் பயிர்களை எப்போது விற்க வேண்டும் என்பதை தீர்மானிக்க சந்தை விலை போக்குகளைக் காட்ட முடியும்."
            ]
        },
        "thank": {
            "patterns": ["நன்றி", "கடமை"],
            "responses": [
                "வரவேற்கிறோம்! எந்த நேரத்திலும் கேள்விகளைக் கேளுங்கள்.",
                "உதவுவதில் மகிழ்ச்சி! உங்கள் விவசாயத்திற்கு வாழ்த்துக்கள்."
            ]
        }
    }
}

# Suggestions by language
SUGGESTIONS = {
    "en": [
        "How to detect crop diseases?",
        "Show me weather forecast",
        "What are current market prices?",
        "Fertilizer recommendations",
        "Irrigation tips"
    ],
    "hi": [
        "फसल रोग कैसे पहचानें?",
        "मौसम का पूर्वानुमान दिखाएं",
        "वर्तमान बाजार मूल्य क्या हैं?",
        "उर्वरक सिफारिशें",
        "सिंचाई सुझाव"
    ],
    "te": [
        "పంట వ్యాధులను ఎలా గుర్తించాలి?",
        "వాతావరణ సూచన చూపించు",
        "ప్రస్తుత మార్కెట్ ధరలు ఏమిటి?",
        "ఎరువుల సిఫార్సులు",
        "నీటిపారుదల చిట్కాలు"
    ],
    "ta": [
        "பயிர் நோய்களை எப்படி கண்டறிவது?",
        "வானிலை முன்னறிவிப்பு காட்டு",
        "தற்போதைய சந்தை விலைகள் என்ன?",
        "உரம் பரிந்துரைகள்",
        "பாசன உதவிக்குறிப்புகள்"
    ]
}

class ChatbotService:
    def __init__(self):
        self.faq_db = FAQ_DATABASE
        self.suggestions = SUGGESTIONS
    
    def get_response(self, message: str, language: str = "en") -> Dict:
        """Get chatbot response for user message"""
        try:
            # Validate language
            if language not in self.faq_db:
                language = "en"
            
            # Normalize message
            message_lower = message.lower().strip()
            
            # Find matching FAQ category
            response_text = None
            faq_lang = self.faq_db[language]
            
            for category, data in faq_lang.items():
                for pattern in data["patterns"]:
                    if pattern in message_lower:
                        # Get random response from category
                        import random
                        response_text = random.choice(data["responses"])
                        break
                
                if response_text:
                    break
            
            # Default response if no match found
            if not response_text:
                default_responses = {
                    "en": "I can help you with crop disease detection, weather forecasts, market prices, and general farming advice. What would you like to know?",
                    "hi": "मैं फसल रोग पहचान, मौसम पूर्वानुमान, बाजार मूल्य और सामान्य कृषि सलाह में आपकी मदद कर सकता हूं। आप क्या जानना चाहेंगे?",
                    "te": "నేను పంట వ్యాధి గుర్తింపు, వాతావరణ సూచనలు, మార్కెట్ ధరలు మరియు సాధారణ వ్యవసాయ సలహాలతో మీకు సహాయం చేయగలను। మీరు ఏమి తెలుసుకోవాలనుకుంటున్నారు?",
                    "ta": "நான் பயிர் நோய் கண்டறிதல், வானிலை முன்னறிவிப்புகள், சந்தை விலைகள் மற்றும் பொது விவசாய ஆலோசனையில் உங்களுக்கு உதவ முடியும். நீங்கள் என்ன தெரிந்து கொள்ள விரும்புகிறீர்கள்?"
                }
                response_text = default_responses.get(language, default_responses["en"])
            
            return {
                "success": True,
                "reply": response_text,
                "suggestions": self.suggestions.get(language, self.suggestions["en"]),
                "language": language
            }
            
        except Exception as e:
            logger.error(f"Chatbot error: {e}")
            return {
                "success": False,
                "reply": "I'm sorry, I encountered an error. Please try again.",
                "suggestions": [],
                "language": language
            }
    
    @staticmethod
    def get_suggestions(language: str = "en") -> List[str]:
        """Get quick suggestion buttons for given language"""
        if language not in SUGGESTIONS:
            language = "en"
        return SUGGESTIONS[language]

# Global instance
chatbot_service = ChatbotService()
