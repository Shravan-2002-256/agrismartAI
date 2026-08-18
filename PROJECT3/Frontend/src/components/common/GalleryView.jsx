// Gallery View Component for History
// Masonry-style grid layout with hover effects
// Optimized for visual browsing of detections

import { useState } from 'react';
import { FiMaximize2 } from 'react-icons/fi';
import FavoriteButton from './FavoriteButton';

const GalleryView = ({ detections = [], onImageClick }) => {
  const [selectedId, setSelectedId] = useState(null);

  if (!detections || detections.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">🖼️</div>
        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
          No Detections Yet
        </h3>
        <p className="text-gray-600 dark:text-gray-400">
          Upload images to see them in gallery view
        </p>
      </div>
    );
  }

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'high':
        return 'border-red-500 bg-red-50 dark:bg-red-900/20';
      case 'moderate':
        return 'border-yellow-500 bg-yellow-50 dark:bg-yellow-900/20';
      case 'low':
        return 'border-green-500 bg-green-50 dark:bg-green-900/20';
      default:
        return 'border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900/20';
    }
  };

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 auto-rows-max">
      {detections.map((detection, index) => {
        const isSelected = selectedId === detection.id;
        
        return (
          <div
            key={detection.id}
            className={`group relative rounded-xl overflow-hidden border-2 transition-all duration-300 cursor-pointer
              ${isSelected ? 'ring-4 ring-primary-500 scale-105 z-10' : 'hover:scale-105 hover:shadow-xl'}
              ${getSeverityColor(detection.severity)}
              animate-fadeIn`}
            style={{ animationDelay: `${index * 50}ms` }}
            onClick={() => {
              setSelectedId(detection.id);
              onImageClick?.(detection);
            }}
          >
            {/* Image */}
            <div className="relative aspect-square overflow-hidden bg-gray-200 dark:bg-gray-700">
              <img
                src={`http://localhost:8000${detection.image_url}`}
                alt={detection.disease_detected}
                className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                onError={(e) => {
                  e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400"><rect fill="%23e5e7eb" width="400" height="400"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="system-ui" font-size="64">🖼️</text></svg>';
                }}
              />

              {/* Overlay */}
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent 
                            opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <div className="absolute bottom-0 left-0 right-0 p-4 text-white">
                  <h4 className="font-bold text-lg mb-1 line-clamp-1">
                    {detection.disease_detected || 'Unknown'}
                  </h4>
                  <p className="text-sm opacity-90">
                    {detection.confidence}% confidence
                  </p>
                </div>
              </div>

              {/* Quick Actions */}
              <div className="absolute top-2 right-2 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <FavoriteButton detectionId={detection.id} size={18} />
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onImageClick?.(detection);
                  }}
                  className="p-2 bg-white/90 dark:bg-gray-800/90 rounded-full hover:bg-white dark:hover:bg-gray-800 transition-colors"
                  title="View details"
                >
                  <FiMaximize2 className="text-gray-700 dark:text-gray-300" size={16} />
                </button>
              </div>

              {/* Confidence Badge */}
              <div className="absolute top-2 left-2">
                <div className={`px-3 py-1 rounded-full text-xs font-bold backdrop-blur-sm ${
                  detection.confidence >= 90 
                    ? 'bg-green-500/90 text-white'
                    : detection.confidence >= 70
                    ? 'bg-yellow-500/90 text-white'
                    : 'bg-red-500/90 text-white'
                }`}>
                  {detection.confidence}%
                </div>
              </div>
            </div>

            {/* Info Bar */}
            <div className="p-3 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-gray-900 dark:text-white text-sm truncate">
                    {detection.crop_type || 'Unknown Crop'}
                  </p>
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    {new Date(detection.detected_at).toLocaleDateString()}
                  </p>
                </div>
                
                {/* Severity Indicator */}
                {detection.severity && (
                  <div className={`ml-2 w-3 h-3 rounded-full flex-shrink-0 ${
                    detection.severity === 'high' 
                      ? 'bg-red-500 animate-pulse'
                      : detection.severity === 'moderate'
                      ? 'bg-yellow-500'
                      : 'bg-green-500'
                  }`} title={`${detection.severity} severity`} />
                )}
              </div>
            </div>

            {/* Selection Indicator */}
            {isSelected && (
              <div className="absolute inset-0 border-4 border-primary-500 rounded-xl pointer-events-none" />
            )}
          </div>
        );
      })}
    </div>
  );
};

export default GalleryView;
