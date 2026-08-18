import { useState, useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import Layout from '../components/common/Layout';
import VoiceInput from '../components/common/VoiceInput';
import { FiSend, FiMessageCircle, FiX, FiNavigation, FiExternalLink, FiArrowLeft, FiBook, FiCpu } from 'react-icons/fi';
import { chatService } from '../services/apiService';

const Chatbot = () => {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const messagesEndRef = useRef(null);

  // Language-specific suggestions
  const quickSuggestions = {
    en: [
      "How to detect crop diseases?",
      "Show me weather forecast",
      "What are current market prices?",
      "Fertilizer recommendations",
      "Irrigation tips"
    ],
    hi: [
      "फसल रोग कैसे पहचानें?",
      "मौसम का पूर्वानुमान दिखाएं",
      "वर्तमान बाजार मूल्य क्या हैं?",
      "उर्वरक सिफारिशें",
      "सिंचाई सुझाव"
    ],
    te: [
      "పంట వ్యాధులను ఎలా గుర్తించాలి?",
      "వాతావరణ సూచన చూపించు",
      "ప్రస్తుత మార్కెట్ ధరలు ఏమిటి?",
      "ఎరువుల సిఫార్సులు",
      "నీటిపారుదల చిట్కాలు"
    ],
    ta: [
      "பயிர் நோய்களை எப்படி கண்டறிவது?",
      "வானிலை முன்னறிவிப்பு காட்டு",
      "தற்போதைய சந்தை விலைகள் என்ன?",
      "உரம் பரிந்துரைகள்",
      "பாசன உதவிக்குறிப்புகள்"
    ]
  };

  // Welcome messages with quick actions
  const welcomeMessages = {
    en: {
      role: 'bot',
      content: "Hello! 👋 I'm your **AgriSmart AI assistant**. I can help you with:",
      type: 'card',
      quickActions: [
        { label: "🌤️ Weather Forecast", action: "weather" },
        { label: "💰 Market Prices", action: "prices" },
        { label: "🔍 Disease Detection", action: "disease" },
        { label: "🏠 Dashboard", action: "dashboard" }
      ],
      timestamp: new Date().toISOString()
    },
    hi: {
      role: 'bot',
      content: "नमस्ते! 👋 मैं आपका **AgriSmart AI सहायक** हूं। मैं इनमें मदद कर सकता हूं:",
      type: 'card',
      quickActions: [
        { label: "🌤️ मौसम पूर्वानुमान", action: "weather" },
        { label: "💰 बाजार मूल्य", action: "prices" },
        { label: "🔍 रोग पहचान", action: "disease" },
        { label: "🏠 डैशबोर्ड", action: "dashboard" }
      ],
      timestamp: new Date().toISOString()
    },
    te: {
      role: 'bot',
      content: "నమస్కారం! 👋 నేను మీ **AgriSmart AI సహాయకుడిని**। నేను వీటితో సహాయం చేయగలను:",
      type: 'card',
      quickActions: [
        { label: "🌤️ వాతావరణ సూచన", action: "weather" },
        { label: "💰 మార్కెట్ ధరలు", action: "prices" },
        { label: "🔍 వ్యాధి గుర్తింపు", action: "disease" },
        { label: "🏠 డాష్‌బోర్డ్", action: "dashboard" }
      ],
      timestamp: new Date().toISOString()
    },
    ta: {
      role: 'bot',
      content: "வணக்கம்! 👋 நான் உங்கள் **AgriSmart AI உதவியாளர்**। நான் இவற்றில் உதவ முடியும்:",
      type: 'card',
      quickActions: [
        { label: "🌤️ வானிலை முன்னறிவிப்பு", action: "weather" },
        { label: "💰 சந்தை விலைகள்", action: "prices" },
        { label: "🔍 நோய் கண்டறிதல்", action: "disease" },
        { label: "🏠 டாஷ்போர்டு", action: "dashboard" }
      ],
      timestamp: new Date().toISOString()
    }
  };

  useEffect(() => {
    // Initialize with welcome message
    const currentLang = i18n.language || 'en';
    setMessages([welcomeMessages[currentLang] || welcomeMessages['en']]);
    setSuggestions(quickSuggestions[currentLang] || quickSuggestions['en']);
  }, [i18n.language]);

  useEffect(() => {
    // Scroll to bottom when new message arrives
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (messageText = null) => {
    const message = messageText || inputMessage.trim();
    
    if (!message) return;

    // Add user message to chat
    const userMessage = {
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await chatService.sendMessage(message, i18n.language);
      
      // Add bot response to chat with rich content including RAG sources
      const botMessage = {
        role: 'bot',
        content: response.data.response || response.data.message,
        type: response.data.type || 'text',
        sources: response.data.sources || [], // RAG sources
        rag_enabled: response.data.rag_enabled || false,
        embedding_model: response.data.embedding_model || null,
        quickActions: response.data.quickActions || [],
        action: response.data.action || null,
        timestamp: response.data.timestamp || new Date().toISOString()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      toast.error('Failed to send message. Please try again.');
      console.error('Chat error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleActionClick = (action) => {
    // Map actions to routes
    const actionRoutes = {
      'dashboard': '/dashboard',
      'disease': '/disease-detection',
      'weather': '/weather',
      'prices': '/market-prices',
      'insights': '/insights',
      'history': '/history'
    };

    const route = actionRoutes[action];
    if (route) {
      navigate(route);
    }
  };

  const formatBotMessage = (content) => {
    // Format markdown-like syntax
    let formatted = content;
    
    // Bold text **text**
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Bullets • to proper list items
    formatted = formatted.replace(/•\s/g, '<br/>• ');
    
    // Line breaks
    formatted = formatted.replace(/\n/g, '<br/>');
    
    return formatted;
  };

  const handleSuggestionClick = (suggestion) => {
    handleSendMessage(suggestion);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Layout>
      <div className="max-w-5xl mx-auto h-[calc(100vh-180px)] flex flex-col">
        {/* Back Button */}
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors group mb-4"
        >
          <FiArrowLeft className="group-hover:-translate-x-1 transition-transform" />
          <span className="font-medium">{t('back_to_dashboard')}</span>
        </button>

        {/* Modern Header */}
        <div className="bg-gradient-to-r from-primary-600 to-emerald-600 text-white p-6 rounded-t-2xl shadow-lg">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-white/20 rounded-xl backdrop-blur-sm">
                <FiMessageCircle size={28} />
              </div>
              <div>
                <h1 className="text-2xl font-bold">{t('assistant_title')}</h1>
                <p className="text-primary-100 text-sm flex items-center gap-2">
                  <span className="w-2 h-2 bg-green-300 rounded-full animate-pulse"></span>
                  {t('online_status')}
                </p>
              </div>
            </div>
            {/* Close Button */}
            <button
              onClick={() => navigate('/dashboard')}
              className="p-2 hover:bg-white/20 rounded-full transition-all duration-200 hover:rotate-90"
              title="Close Chat"
            >
              <FiX size={24} />
            </button>
          </div>
        </div>

        {/* Chat Messages with Modern Design */}
        <div className="flex-1 bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-800 overflow-y-auto p-6 space-y-4 border-x border-gray-200 dark:border-gray-700">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}
            >
              {message.role === 'user' ? (
                <div className="chat-bubble-user">
                  <p className="text-sm leading-relaxed">{message.content}</p>
                  <p className="text-xs mt-2 opacity-75">
                    {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              ) : (
                <div className="max-w-[80%] space-y-3">
                  <div className="chat-bubble-bot">
                    {loading && index === messages.length - 1 ? (
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                        <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                      </div>
                    ) : (
                      <>
                        <div 
                          className="prose prose-sm max-w-none text-gray-800 dark:text-gray-200"
                          dangerouslySetInnerHTML={{ __html: formatBotMessage(message.content) }}
                        />
                        
                        {/* V3.0 RAG Sources Display */}
                        {message.sources && message.sources.length > 0 && (
                          <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
                            <p className="text-xs font-semibold text-blue-700 dark:text-blue-400 mb-2 flex items-center gap-1">
                              <FiBook className="text-sm" /> Sources (RAG-powered response):
                            </p>
                            <ul className="space-y-1">
                              {message.sources.map((source, idx) => (
                                <li key={idx} className="text-xs text-blue-600 dark:text-blue-300 flex items-start">
                                  <span className="mr-1">•</span>
                                  <span>
                                    {typeof source === 'string' 
                                      ? source 
                                      : `${source.title || 'Knowledge Base'} (${source.category || 'General'})`
                                    }
                                  </span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {/* V3.0 AI Model Info */}
                        {message.rag_enabled && message.embedding_model && (
                          <div className="mt-2 px-3 py-2 bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20 border border-indigo-200 dark:border-indigo-800 rounded-lg">
                            <p className="text-xs text-indigo-700 dark:text-indigo-400 flex items-center gap-1">
                              <FiCpu className="text-sm" />
                              <strong>AI Model:</strong> {message.embedding_model}
                              {message.embedding_model.includes('Ollama') && (
                                <span className="ml-2 px-2 py-0.5 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded-full text-xs">
                                  768-dim embeddings
                                </span>
                              )}
                            </p>
                          </div>
                        )}

                        <p className="text-xs mt-3 text-gray-500 dark:text-gray-400">
                          {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </p>

                        {/* Quick Action Buttons */}
                        {message.quickActions && message.quickActions.length > 0 && (
                          <div className="flex flex-wrap gap-2 mt-4 pt-3 border-t border-gray-200 dark:border-gray-700">
                            {message.quickActions.map((action, actionIndex) => (
                              <button
                                key={actionIndex}
                                onClick={() => handleActionClick(action.action)}
                                className="flex items-center space-x-2 px-4 py-2.5 bg-white dark:bg-gray-700 border-2 border-primary-500 dark:border-primary-600 text-primary-700 dark:text-primary-400 rounded-lg hover:bg-primary-50 dark:hover:bg-primary-900/30 transition-all duration-200 shadow-sm font-medium hover:scale-105"
                              >
                                <span className="text-sm">{action.label}</span>
                                <FiExternalLink className="text-xs" />
                              </button>
                            ))}
                          </div>
                        )}
                      </>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}

          {/* Typing Indicator */}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gradient-to-r from-gray-50 to-gray-100 border border-gray-200 rounded-lg p-4 shadow-md">
                <div className="flex space-x-2 items-center">
                  <span className="text-gray-600 text-sm">AI is thinking</span>
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Quick Suggestions */}
        {suggestions.length > 0 && messages.length <= 2 && (
          <div className="bg-gray-50 p-4 border-x border-gray-200">
            <p className="text-sm text-gray-600 mb-2 font-medium">
              {i18n.language === 'en' && "Quick suggestions:"}
              {i18n.language === 'hi' && "त्वरित सुझाव:"}
              {i18n.language === 'te' && "శీఘ్ర సూచనలు:"}
              {i18n.language === 'ta' && "விரைவு பரிந்துரைகள்:"}
            </p>
            <div className="flex flex-wrap gap-2">
              {suggestions.map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestionClick(suggestion)}
                  className="text-sm px-4 py-2 bg-white border border-primary-300 text-primary-700 rounded-full hover:bg-primary-50 hover:border-primary-500 transition"
                  disabled={loading}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input Area with Modern Design */}
        <div className="bg-white dark:bg-gray-800 border-t border-x border-gray-200 dark:border-gray-700 p-4 rounded-b-2xl shadow-lg">
          <div className="flex space-x-3">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={
                i18n.language === 'en' ? "Type your message..." :
                i18n.language === 'hi' ? "अपना संदेश लिखें..." :
                i18n.language === 'te' ? "మీ సందేశాన్ని టైప్ చేయండి..." :
                "உங்கள் செய்தியை தட்டச்சு செய்யவும்..."
              }
              rows="2"
              className="input-professional flex-1 resize-none text-sm"
              disabled={loading}
            />
            {/* Voice Input */}
            <VoiceInput 
              onTranscript={(transcript) => {
                setInputMessage(transcript);
                toast.success('Voice recognized!');
              }}
              language={i18n.language}
            />
            <button
              onClick={() => handleSendMessage()}
              disabled={loading || !inputMessage.trim()}
              className="btn-primary-pro flex items-center space-x-2 px-6 self-end"
            >
              <FiSend className={loading ? 'animate-pulse' : ''} />
              <span className="font-semibold">
                {i18n.language === 'en' && "Send"}
                {i18n.language === 'hi' && "भेजें"}
                {i18n.language === 'te' && "పంపు"}
                {i18n.language === 'ta' && "அனுப்பு"}
              </span>
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Chatbot;
