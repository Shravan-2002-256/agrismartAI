// Animated Progress Bar Component
// Shows confidence scores and health metrics with smooth animations
// Custom gradient styling for visual appeal

import React from 'react';

const ProgressBar = ({ 
  value, 
  max = 100, 
  label, 
  showPercentage = true,
  variant = 'primary',
  animated = true,
  height = 'md'
}) => {
  const percentage = Math.min((value / max) * 100, 100);
  
  const variants = {
    primary: 'from-primary-500 to-emerald-400',
    success: 'from-green-500 to-emerald-400',
    warning: 'from-yellow-500 to-orange-400',
    danger: 'from-red-500 to-pink-500',
    info: 'from-blue-500 to-cyan-400',
  };
  
  const heights = {
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4',
  };
  
  return (
    <div className="w-full space-y-2">
      {label && (
        <div className="flex justify-between text-sm">
          <span className="font-medium text-gray-700 dark:text-gray-300">{label}</span>
          {showPercentage && (
            <span className="text-gray-600 dark:text-gray-400 font-semibold">
              {Math.round(percentage)}%
            </span>
          )}
        </div>
      )}
      
      <div className={`w-full bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden ${heights[height]}`}>
        <div 
          className={`${heights[height]} bg-gradient-to-r ${variants[variant]} rounded-full transition-all duration-1000 ease-out relative overflow-hidden`}
          style={{ width: `${percentage}%` }}
        >
          {animated && (
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer" />
          )}
        </div>
      </div>
    </div>
  );
};

export default ProgressBar;
