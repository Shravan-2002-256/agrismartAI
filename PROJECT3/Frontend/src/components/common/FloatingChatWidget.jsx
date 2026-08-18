import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FiMessageCircle, FiX } from 'react-icons/fi';
import { useTranslation } from 'react-i18next';


const FloatingChatWidget = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useTranslation();
  const [isVisible, setIsVisible] = useState(true);

  // Don't show on chatbot page
  if (location.pathname === '/chatbot') {
    return null;
  }

  // Don't show on login/register pages
  if (location.pathname === '/login' || location.pathname === '/register' || location.pathname === '/') {
    return null;
  }

  if (!isVisible) {
    return (
      <button
        onClick={() => setIsVisible(true)}
        className="fixed bottom-4 right-4 z-50 p-4 bg-primary-600 text-white rounded-full shadow-lg hover:bg-primary-700 transition-all transform hover:scale-110"
        title={`${t('chat')} Assistant`}
        aria-label="Open Chat Assistant"
      >
        <FiMessageCircle className="w-6 h-6" />
      </button>
    );
  }

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <div className="relative">
        <button
          onClick={() => navigate('/chatbot')}
          className="flex items-center space-x-2 px-5 py-3 bg-gradient-to-r from-primary-600 to-green-600 text-white rounded-full shadow-2xl hover:shadow-3xl transform hover:scale-105 transition-all duration-300"
          title={`${t('chat')} Assistant`}
          aria-label="Open Chat Assistant"
        >
          <FiMessageCircle className="w-6 h-6 flex-shrink-0" />
          <span className="font-medium whitespace-nowrap">{t('chat')} AI</span>
        </button>
        
        <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
        
        <button
          onClick={(e) => {
            e.stopPropagation();
            setIsVisible(false);
          }}
          className="absolute -top-2 -left-2 p-1.5 bg-gray-600 text-white rounded-full hover:bg-gray-700 transition shadow-md"
          title={t('close')}
          aria-label="Close Chat Widget"
        >
          <FiX className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};

export default FloatingChatWidget;
