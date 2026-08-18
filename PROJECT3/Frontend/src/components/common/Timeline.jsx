// Timeline Component for Detection History
// Custom vertical timeline showing detection events chronologically
// Designed to feel hand-crafted with attention to detail

import React from 'react';
import { FiCheckCircle, FiAlertTriangle, FiXCircle, FiInfo } from 'react-icons/fi';

const Timeline = ({ items }) => {
  const getStatusIcon = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'high':
        return { icon: FiXCircle, color: 'text-red-500', bg: 'bg-red-100 dark:bg-red-900/30' };
      case 'moderate':
      case 'medium':
        return { icon: FiAlertTriangle, color: 'text-yellow-500', bg: 'bg-yellow-100 dark:bg-yellow-900/30' };
      case 'low':
        return { icon: FiCheckCircle, color: 'text-green-500', bg: 'bg-green-100 dark:bg-green-900/30' };
      case 'none':
        return { icon: FiCheckCircle, color: 'text-blue-500', bg: 'bg-blue-100 dark:bg-blue-900/30' };
      default:
        return { icon: FiInfo, color: 'text-gray-500', bg: 'bg-gray-100 dark:bg-gray-900/30' };
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 60) return `${diffMins} min${diffMins !== 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
    
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  return (
    <div className="relative">
      {/* Vertical Line */}
      <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-gradient-to-b from-primary-500 via-emerald-400 to-transparent" />

      {/* Timeline Items */}
      <div className="space-y-8">
        {items.map((item, index) => {
          const statusConfig = getStatusIcon(item.severity);
          const Icon = statusConfig.icon;

          return (
            <div 
              key={item.id || index} 
              className="relative flex items-start gap-6 animate-fadeIn"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {/* Icon Circle */}
              <div className={`relative z-10 flex-shrink-0 w-16 h-16 ${statusConfig.bg} rounded-full flex items-center justify-center shadow-lg border-4 border-white dark:border-gray-900`}>
                <Icon className={`text-2xl ${statusConfig.color}`} />
              </div>

              {/* Content Card */}
              <div className="flex-1 glass-card p-6 hover:shadow-2xl transition-all duration-300 group">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="text-lg font-bold text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                      {item.disease_class || item.title}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      {item.crop_type && <span className="capitalize">{item.crop_type} • </span>}
                      {formatDate(item.detected_at || item.timestamp || item.created_at)}
                    </p>
                  </div>
                  
                  {item.confidence && (
                    <div className="text-right">
                      <div className="text-2xl font-bold text-primary-600 dark:text-primary-400">
                        {item.confidence}%
                      </div>
                      <div className="text-xs text-gray-500">Confidence</div>
                    </div>
                  )}
                </div>

                {/* Image Preview if available */}
                {item.image_url && (
                  <div className="mt-4 mb-3">
                    <img 
                      src={`http://localhost:8000${item.image_url}`}
                      alt={item.disease_class || item.title || 'Detection'}
                      className="w-full h-40 object-cover rounded-lg border-2 border-gray-200 dark:border-gray-700"
                      onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextElementSibling.style.display = 'flex';
                      }}
                    />
                    <div 
                      className="w-full h-40 bg-gray-100 dark:bg-gray-700 rounded-lg border-2 border-gray-200 dark:border-gray-700 items-center justify-center text-gray-400 hidden"
                      style={{ display: 'none' }}
                    >
                      <div className="text-center">
                        <span className="text-3xl mb-1 block">🖼️</span>
                        <span className="text-xs">Image Unavailable</span>
                      </div>
                    </div>
                  </div>
                )}

                {/* Description or Treatment */}
                {(item.description || item.treatment_recommendation) && (
                  <p className="text-sm text-gray-700 dark:text-gray-300 mt-3 line-clamp-2">
                    {item.description || item.treatment_recommendation}
                  </p>
                )}

                {/* Severity Badge */}
                {item.severity && (
                  <div className="mt-4 flex items-center gap-2">
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      item.severity === 'high' ? 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-200' :
                      item.severity === 'moderate' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-200' :
                      item.severity === 'low' ? 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-200' :
                      'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-200'
                    }`}>
                      {item.severity.toUpperCase()} Severity
                    </span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* End Marker */}
      {items.length > 0 && (
        <div className="relative flex items-center gap-6 mt-8">
          <div className="relative z-10 flex-shrink-0 w-16 h-16 bg-gray-200 dark:bg-gray-700 rounded-full flex items-center justify-center shadow-lg border-4 border-white dark:border-gray-900">
            <div className="text-xl">🌱</div>
          </div>
          <div className="text-gray-500 dark:text-gray-400 text-sm italic">
            Start of your farming journey with AgriSmart AI
          </div>
        </div>
      )}
    </div>
  );
};

export default Timeline;
