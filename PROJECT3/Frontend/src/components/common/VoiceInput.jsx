// Voice Input Component for Chatbot
// Uses Web Speech API for voice recognition
// Provides visual feedback during recording

import { useState, useEffect } from 'react';
import { FiMic, FiMicOff } from 'react-icons/fi';
import { toast } from 'react-toastify';

const VoiceInput = ({ onTranscript, language = 'en-US' }) => {
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState(null);
  const [isSupported, setIsSupported] = useState(false);

  useEffect(() => {
    // Check if browser supports speech recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (SpeechRecognition) {
      const recognitionInstance = new SpeechRecognition();
      recognitionInstance.continuous = false;
      recognitionInstance.interimResults = false;
      
      // Map language codes
      const langMap = {
        'en': 'en-US',
        'hi': 'hi-IN',
        'te': 'te-IN',
        'ta': 'ta-IN'
      };
      
      recognitionInstance.lang = langMap[language] || language;

      recognitionInstance.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        onTranscript?.(transcript);
        setIsListening(false);
      };

      recognitionInstance.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
        
        if (event.error === 'no-speech') {
          toast.error('No speech detected. Please try again.');
        } else if (event.error === 'not-allowed') {
          toast.error('Microphone access denied.');
        } else {
          toast.error('Voice recognition failed. Please try again.');
        }
      };

      recognitionInstance.onend = () => {
        setIsListening(false);
      };

      setRecognition(recognitionInstance);
      setIsSupported(true);
    } else {
      setIsSupported(false);
    }
  }, [language, onTranscript]);

  const toggleListening = () => {
    if (!recognition) return;

    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      try {
        recognition.start();
        setIsListening(true);
      } catch (error) {
        console.error('Failed to start recognition:', error);
        toast.error('Failed to start voice input');
      }
    }
  };

  if (!isSupported) {
    return null; // Don't show button if not supported
  }

  return (
    <button
      onClick={toggleListening}
      className={`p-3 rounded-full transition-all duration-300 ${
        isListening
          ? 'bg-red-600 hover:bg-red-700 text-white animate-pulse'
          : 'bg-gray-100 dark:bg-gray-700 hover:bg-primary-100 dark:hover:bg-primary-900/30 text-gray-600 dark:text-gray-400'
      }`}
      title={isListening ? 'Stop recording' : 'Start voice input'}
    >
      {isListening ? (
        <FiMicOff size={20} />
      ) : (
        <FiMic size={20} />
      )}
    </button>
  );
};

export default VoiceInput;
