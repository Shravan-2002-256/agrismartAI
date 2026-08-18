// Tour Guide Component
// Interactive onboarding walkthrough for new users
// Highlights key features with step-by-step guide

import { useState, useEffect } from 'react';
import { FiX, FiChevronRight, FiChevronLeft } from 'react-icons/fi';

const TourGuide = ({ isOpen, onComplete }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isVisible, setIsVisible] = useState(false);

  const tourSteps = [
    {
      id: 'welcome',
      title: '👋 Welcome to AgriSmart AI!',
      description: 'Your intelligent farming companion. Let\'s take a quick tour to help you get started.',
      position: 'center',
      highlight: null
    },
    {
      id: 'dashboard',
      title: '📊 Dashboard Overview',
      description: 'View your farming stats, recent detections, and quick actions all in one place.',
      position: 'top',
      highlight: '.dashboard-stats'
    },
    {
      id: 'disease-detection',
      title: '🔬 Disease Detection',
      description: 'Upload crop images to instantly identify diseases with AI-powered analysis.',
      position: 'right',
      highlight: '[href="/disease-detection"]'
    },
    /* 🔒 HIDDEN FOR MID-VIVA
    {
      id: 'chatbot',
      title: '💬 AI Farming Assistant',
      description: 'Get instant answers to your farming questions from our intelligent chatbot.',
      position: 'right',
      highlight: '[href="/chatbot"]'
    },
    */
    {
      id: 'weather',
      title: '🌤️ Weather Forecasts',
      description: 'Check 7-day weather predictions to plan your farming activities.',
      position: 'right',
      highlight: '[href="/weather"]'
    },
    {
      id: 'history',
      title: '📜 Detection History',
      description: 'Review all your past disease detections with timeline and list views.',
      position: 'right',
      highlight: '[href="/history"]'
    },
    {
      id: 'complete',
      title: '🎉 You\'re All Set!',
      description: 'Start exploring AgriSmart AI and revolutionize your farming practices!',
      position: 'center',
      highlight: null
    }
  ];

  useEffect(() => {
    if (isOpen) {
      setIsVisible(true);
      // Mark tour as shown in localStorage
      localStorage.setItem('agrismart_tour_shown', 'true');
    }
  }, [isOpen]);

  if (!isVisible) return null;

  const currentTourStep = tourSteps[currentStep];
  const isFirstStep = currentStep === 0;
  const isLastStep = currentStep === tourSteps.length - 1;

  const handleNext = () => {
    if (isLastStep) {
      handleComplete();
    } else {
      setCurrentStep(prev => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (!isFirstStep) {
      setCurrentStep(prev => prev - 1);
    }
  };

  const handleSkip = () => {
    handleComplete();
  };

  const handleComplete = () => {
    setIsVisible(false);
    onComplete?.();
  };

  // Highlight element with spotlight effect
  useEffect(() => {
    if (currentTourStep.highlight) {
      const element = document.querySelector(currentTourStep.highlight);
      if (element) {
        element.classList.add('tour-spotlight');
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        return () => {
          element.classList.remove('tour-spotlight');
        };
      }
    }
  }, [currentStep, currentTourStep.highlight]);

  const getTooltipPosition = () => {
    if (currentTourStep.position === 'center') {
      return 'fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2';
    }
    // Default bottom-right for other positions
    return 'fixed bottom-6 right-6';
  };

  return (
    <>
      {/* Overlay */}
      <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] animate-fadeIn" />

      {/* Tour Tooltip */}
      <div className={`${getTooltipPosition()} z-[101] max-w-md w-full mx-4 animate-slideInUp`}>
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-primary-600 to-emerald-500 p-6 text-white">
            <div className="flex items-start justify-between mb-2">
              <h3 className="text-2xl font-bold">{currentTourStep.title}</h3>
              <button
                onClick={handleSkip}
                className="p-1 hover:bg-white/20 rounded-lg transition-colors"
              >
                <FiX size={20} />
              </button>
            </div>
            <p className="text-white/90 text-sm">{currentTourStep.description}</p>
          </div>

          {/* Progress Bar */}
          <div className="h-1 bg-gray-200 dark:bg-gray-700">
            <div
              className="h-full bg-primary-600 transition-all duration-300"
              style={{ width: `${((currentStep + 1) / tourSteps.length) * 100}%` }}
            />
          </div>

          {/* Footer */}
          <div className="p-6">
            <div className="flex items-center justify-between">
              {/* Step indicator */}
              <div className="flex items-center gap-2">
                {tourSteps.map((_, index) => (
                  <div
                    key={index}
                    className={`w-2 h-2 rounded-full transition-all duration-300 ${
                      index === currentStep
                        ? 'bg-primary-600 w-6'
                        : index < currentStep
                        ? 'bg-primary-400'
                        : 'bg-gray-300 dark:bg-gray-600'
                    }`}
                  />
                ))}
              </div>

              {/* Navigation buttons */}
              <div className="flex items-center gap-2">
                {!isFirstStep && (
                  <button
                    onClick={handlePrevious}
                    className="px-4 py-2 text-gray-600 dark:text-gray-400 hover:bg-gray-100 
                               dark:hover:bg-gray-700 rounded-lg transition-colors font-medium flex items-center gap-2"
                  >
                    <FiChevronLeft size={18} />
                    Back
                  </button>
                )}
                <button
                  onClick={handleNext}
                  className="px-6 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg 
                             transition-colors font-medium flex items-center gap-2"
                >
                  {isLastStep ? 'Get Started' : 'Next'}
                  {!isLastStep && <FiChevronRight size={18} />}
                </button>
              </div>
            </div>

            {/* Skip button */}
            {!isLastStep && (
              <button
                onClick={handleSkip}
                className="w-full mt-3 text-sm text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 
                           transition-colors"
              >
                Skip tour
              </button>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default TourGuide;
