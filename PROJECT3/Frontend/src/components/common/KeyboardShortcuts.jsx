// Keyboard Shortcuts Handler
// Global keyboard shortcuts for quick navigation
// Press ? to see shortcuts overlay

import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiCommand, FiX } from 'react-icons/fi';

const KeyboardShortcuts = () => {
  const [showHelp, setShowHelp] = useState(false);
  const navigate = useNavigate();

  const shortcuts = [
    { key: 'Ctrl+K', action: 'Quick Search', description: 'Open search bar' },
    { key: 'Ctrl+D', action: 'Disease Detection', description: 'Go to detection page' },
    { key: 'Ctrl+H', action: 'History', description: 'View detection history' },
    { key: 'Ctrl+C', action: 'Chatbot', description: 'Open AI assistant' },
    { key: 'Ctrl+W', action: 'Weather', description: 'Check weather forecast' },
    { key: 'Ctrl+M', action: 'Market', description: 'View market prices' },
    { key: 'Ctrl+/', action: 'Dashboard', description: 'Return to dashboard' },
    { key: '?', action: 'Help', description: 'Show this help' },
    { key: 'Esc', action: 'Close', description: 'Close modals/overlays' },
  ];

  useEffect(() => {
    const handleKeyPress = (e) => {
      // Ignore if user is typing in input/textarea
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        return;
      }

      // Show/hide help with ?
      if (e.key === '?' && !e.ctrlKey && !e.metaKey) {
        e.preventDefault();
        setShowHelp(prev => !prev);
        return;
      }

      // Close with Esc
      if (e.key === 'Escape') {
        setShowHelp(false);
        return;
      }

      // Handle Ctrl/Cmd shortcuts
      if (e.ctrlKey || e.metaKey) {
        e.preventDefault();
        
        switch (e.key.toLowerCase()) {
          case 'k':
            // Focus search (implement search focus later)
            document.querySelector('input[type="text"]')?.focus();
            break;
          case 'd':
            navigate('/disease-detection');
            break;
          case 'h':
            navigate('/history');
            break;
          case 'c':
            navigate('/chatbot');
            break;
          case 'w':
            navigate('/weather');
            break;
          case 'm':
            navigate('/market');
            break;
          case '/':
            navigate('/dashboard');
            break;
        }
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [navigate]);

  if (!showHelp) return null;

  return (
    <div className="fixed inset-0 z-[100] bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 animate-fadeIn">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-2xl w-full max-h-[80vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 p-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-primary-100 dark:bg-primary-900/30 rounded-xl">
              <FiCommand className="text-primary-600 dark:text-primary-400 text-2xl" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                Keyboard Shortcuts
              </h2>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Navigate AgriSmart AI faster
              </p>
            </div>
          </div>
          <button
            onClick={() => setShowHelp(false)}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          >
            <FiX className="text-gray-600 dark:text-gray-400" size={24} />
          </button>
        </div>

        {/* Shortcuts List */}
        <div className="p-6 space-y-3">
          {shortcuts.map((shortcut, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-4 rounded-lg hover:bg-gray-50 
                         dark:hover:bg-gray-700/50 transition-colors group"
            >
              <div>
                <p className="font-semibold text-gray-900 dark:text-white group-hover:text-primary-600 
                              dark:group-hover:text-primary-400 transition-colors">
                  {shortcut.action}
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {shortcut.description}
                </p>
              </div>
              <kbd className="px-3 py-1.5 bg-gray-100 dark:bg-gray-700 border border-gray-300 
                             dark:border-gray-600 rounded-lg text-sm font-mono font-semibold 
                             text-gray-700 dark:text-gray-300 shadow-sm">
                {shortcut.key}
              </kbd>
            </div>
          ))}
        </div>

        {/* Footer Tip */}
        <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-900/50">
          <p className="text-xs text-center text-gray-500 dark:text-gray-400">
            💡 <strong>Tip:</strong> Press <kbd className="px-2 py-0.5 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded text-xs font-mono">?</kbd> anytime to toggle this help
          </p>
        </div>
      </div>
    </div>
  );
};

export default KeyboardShortcuts;
