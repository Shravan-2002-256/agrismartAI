import React from 'react';
import { FiSun, FiMoon } from 'react-icons/fi';
import { useTheme } from '../../contexts/ThemeContext';

const ThemeToggle = () => {
  const { isDark, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className="relative p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200"
      title={isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
      aria-label="Toggle theme"
    >
      {/* Sun icon (visible in dark mode) */}
      <FiSun 
        className={`w-5 h-5 text-gray-700 dark:text-yellow-400 transition-all duration-300 ${
          isDark ? 'rotate-0 scale-100' : 'rotate-90 scale-0 absolute'
        }`} 
      />
      
      {/* Moon icon (visible in light mode) */}
      <FiMoon 
        className={`w-5 h-5 text-gray-700 dark:text-yellow-400 transition-all duration-300 ${
          !isDark ? 'rotate-0 scale-100' : 'rotate-90 scale-0 absolute'
        }`} 
      />
    </button>
  );
};

export default ThemeToggle;
