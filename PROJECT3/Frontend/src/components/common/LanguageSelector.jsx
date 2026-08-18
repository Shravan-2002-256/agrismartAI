import { useState, useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { LANGUAGES } from '../../utils/constants';
import { FiGlobe, FiChevronDown } from 'react-icons/fi';

const LanguageSelector = () => {
  const { i18n } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const [currentLanguage, setCurrentLanguage] = useState(i18n.language);
  const dropdownRef = useRef(null);

  // Load saved language on mount
  useEffect(() => {
    const savedLanguage = localStorage.getItem('language');
    if (savedLanguage && savedLanguage !== i18n.language) {
      i18n.changeLanguage(savedLanguage);
      setCurrentLanguage(savedLanguage);
    }
  }, [i18n]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const changeLanguage = (langCode) => {
    i18n.changeLanguage(langCode);
    localStorage.setItem('language', langCode);
    setCurrentLanguage(langCode);
    setIsOpen(false);
    
    // Force re-render of all components
    window.dispatchEvent(new Event('languageChanged'));
  };

  const currentLangName = LANGUAGES.find(lang => lang.code === currentLanguage)?.nativeName || 'English';

  return (
    <div className="relative" ref={dropdownRef}>
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors border border-gray-300"
        aria-label="Select Language"
      >
        <FiGlobe className="text-lg" />
        <span className="text-sm font-medium">{currentLangName}</span>
        <FiChevronDown className={`text-sm transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-xl border border-gray-200 z-50 overflow-hidden">
          <div className="py-1">
            {LANGUAGES.map((lang) => (
              <button
                key={lang.code}
                onClick={() => changeLanguage(lang.code)}
                className={`w-full text-left px-4 py-3 hover:bg-primary-50 transition-colors flex items-center justify-between ${
                  currentLanguage === lang.code 
                    ? 'bg-primary-100 text-primary-700 font-semibold' 
                    : 'text-gray-700'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{lang.flag}</span>
                  <div>
                    <div className="font-medium">{lang.nativeName}</div>
                    <div className="text-xs text-gray-500">{lang.name}</div>
                  </div>
                </div>
                {currentLanguage === lang.code && (
                  <svg className="w-5 h-5 text-primary-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                )}
              </button>
            ))}
          </div>
          
          <div className="px-4 py-2 bg-gray-50 border-t border-gray-200">
            <p className="text-xs text-gray-500 text-center">
              Language applied to all features
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default LanguageSelector;
