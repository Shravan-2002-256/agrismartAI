// Image Lightbox Component
// Simple custom lightbox for viewing detection images in detail
// No external dependencies - built from scratch

import React from 'react';
import { FiX, FiZoomIn, FiZoomOut, FiDownload } from 'react-icons/fi';

const ImageLightbox = ({ image, isOpen, onClose, title, metadata }) => {
  const [zoom, setZoom] = React.useState(1);
  
  if (!isOpen) return null;

  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = image;
    link.download = `agrismart-detection-${Date.now()}.jpg`;
    link.click();
  };

  const handleZoomIn = () => {
    setZoom(prev => Math.min(prev + 0.25, 3));
  };

  const handleZoomOut = () => {
    setZoom(prev => Math.max(prev - 0.25, 0.5));
  };

  return (
    <div 
      className="fixed inset-0 z-50 bg-black/90 backdrop-blur-sm flex items-center justify-center p-4 animate-fadeIn"
      onClick={onClose}
    >
      {/* Close Button */}
      <button
        onClick={onClose}
        className="absolute top-4 right-4 p-3 bg-white/10 hover:bg-white/20 rounded-full text-white transition-all duration-200 hover:rotate-90"
        title="Close (Esc)"
      >
        <FiX size={24} />
      </button>

      {/* Zoom Controls */}
      <div className="absolute top-4 left-4 flex gap-2">
        <button
          onClick={(e) => { e.stopPropagation(); handleZoomOut(); }}
          className="p-3 bg-white/10 hover:bg-white/20 rounded-full text-white transition-all"
          title="Zoom Out"
        >
          <FiZoomOut size={20} />
        </button>
        <button
          onClick={(e) => { e.stopPropagation(); handleZoomIn(); }}
          className="p-3 bg-white/10 hover:bg-white/20 rounded-full text-white transition-all"
          title="Zoom In"
        >
          <FiZoomIn size={20} />
        </button>
        <button
          onClick={(e) => { e.stopPropagation(); handleDownload(); }}
          className="p-3 bg-white/10 hover:bg-white/20 rounded-full text-white transition-all"
          title="Download Image"
        >
          <FiDownload size={20} />
        </button>
      </div>

      {/* Image Container */}
      <div 
        className="max-w-5xl max-h-[85vh] overflow-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <img
          src={image}
          alt={title}
          className="w-full h-auto rounded-lg shadow-2xl transition-transform duration-300"
          style={{ transform: `scale(${zoom})` }}
        />
        
        {/* Image Info */}
        {(title || metadata) && (
          <div className="mt-4 p-4 bg-white/10 backdrop-blur-md rounded-lg">
            {title && (
              <h3 className="text-xl font-bold text-white mb-2">{title}</h3>
            )}
            {metadata && (
              <div className="text-sm text-gray-300 space-y-1">
                {Object.entries(metadata).map(([key, value]) => (
                  <p key={key}>
                    <span className="font-semibold">{key}:</span> {value}
                  </p>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Zoom Level Indicator */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 px-4 py-2 bg-white/10 backdrop-blur-md rounded-full text-white text-sm">
        {Math.round(zoom * 100)}%
      </div>
    </div>
  );
};

export default ImageLightbox;
