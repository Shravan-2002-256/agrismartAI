import React from 'react';

const Logo = ({ size = "default", showText = true }) => {
  const sizes = {
    small: { container: "h-8", icon: "w-5 h-5", text: "text-base", subtext: "text-xs" },
    default: { container: "h-10", icon: "w-6 h-6", text: "text-lg", subtext: "text-xs" },
    large: { container: "h-16", icon: "w-8 h-8", text: "text-2xl", subtext: "text-sm" }
  };

  const currentSize = sizes[size];

  return (
    <div className={`flex items-center gap-2 ${currentSize.container}`}>
      {/* Logo Icon with 3D effect */}
      <div className="relative">
        {/* Shadow layer */}
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-500 to-green-600 rounded-lg rotate-3 opacity-20"></div>
        
        {/* Main logo container */}
        <div className="relative bg-gradient-to-br from-emerald-500 to-green-600 rounded-lg shadow-lg p-2">
          {/* Plant/Leaf SVG Icon */}
          <svg 
            className={`${currentSize.icon} text-white`}
            viewBox="0 0 24 24" 
            fill="currentColor"
          >
            <path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z"/>
          </svg>
        </div>
      </div>
      
      {/* Text */}
      {showText && (
        <div className="flex flex-col justify-center">
          <h1 className={`font-bold ${currentSize.text} leading-none text-gray-900 dark:text-white`}>
            AgriSmart
          </h1>
          <p className={`${currentSize.subtext} text-emerald-600 dark:text-emerald-400 font-medium leading-none mt-0.5`}>
            AI Assistant
          </p>
        </div>
      )}
    </div>
  );
};

export default Logo;
