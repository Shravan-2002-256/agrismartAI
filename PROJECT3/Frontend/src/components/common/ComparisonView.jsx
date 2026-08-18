// Comparison View Component
// Side-by-side comparison of multiple detections
// Helps farmers analyze different disease patterns

import { useState } from 'react';
import { FiX, FiCheck } from 'react-icons/fi';

const ComparisonView = ({ detections, onClose }) => {
  const [selectedItems, setSelectedItems] = useState([]);

  const toggleSelection = (item) => {
    if (selectedItems.find(i => i.id === item.id)) {
      setSelectedItems(selectedItems.filter(i => i.id !== item.id));
    } else {
      if (selectedItems.length < 3) {
        setSelectedItems([...selectedItems, item]);
      }
    }
  };

  if (selectedItems.length === 0) {
    return (
      <div className="glass-card p-8 text-center">
        <div className="text-6xl mb-4">📊</div>
        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
          Select Detections to Compare
        </h3>
        <p className="text-gray-600 dark:text-gray-400 mb-6">
          Choose up to 3 detections to compare side-by-side
        </p>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4 max-h-96 overflow-y-auto">
          {detections?.slice(0, 6).map((detection) => (
            <button
              key={detection.id}
              onClick={() => toggleSelection(detection)}
              className="p-4 border-2 border-gray-200 dark:border-gray-600 rounded-xl 
                         hover:border-primary-500 dark:hover:border-primary-400 transition-all
                         text-left group"
            >
              <img
                src={`http://localhost:8000${detection.image_url}`}
                alt={detection.disease_detected}
                className="w-full h-32 object-cover rounded-lg mb-3"
              />
              <p className="font-semibold text-gray-900 dark:text-white text-sm truncate group-hover:text-primary-600">
                {detection.disease_detected}
              </p>
              <p className="text-xs text-gray-500">
                {detection.confidence}% • {detection.crop_type}
              </p>
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm p-4 overflow-y-auto">
      <div className="max-w-7xl mx-auto py-8">
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl">
          {/* Header */}
          <div className="border-b border-gray-200 dark:border-gray-700 p-6 flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                Comparison View
              </h2>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Comparing {selectedItems.length} detection{selectedItems.length > 1 ? 's' : ''}
              </p>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <FiX className="text-gray-600 dark:text-gray-400" size={24} />
            </button>
          </div>

          {/* Comparison Grid */}
          <div className="p-6">
            <div className={`grid gap-6 ${selectedItems.length === 2 ? 'md:grid-cols-2' : 'md:grid-cols-3'}`}>
              {selectedItems.map((item, index) => (
                <div key={item.id} className="space-y-4">
                  {/* Image */}
                  <div className="relative">
                    <img
                      src={`http://localhost:8000${item.image_url}`}
                      alt={item.disease_detected}
                      className="w-full h-48 object-cover rounded-xl border-2 border-gray-200 dark:border-gray-700"
                    />
                    <div className="absolute top-2 left-2 px-3 py-1 bg-primary-600 text-white rounded-full text-sm font-bold">
                      #{index + 1}
                    </div>
                  </div>

                  {/* Details */}
                  <div className="space-y-3">
                    <div>
                      <label className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">Disease</label>
                      <p className="font-bold text-gray-900 dark:text-white">{item.disease_detected || 'N/A'}</p>
                    </div>

                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">Confidence</label>
                        <p className="font-bold text-primary-600 dark:text-primary-400">{item.confidence}%</p>
                      </div>
                      <div>
                        <label className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">Severity</label>
                        <span className={`inline-block px-2 py-1 rounded-full text-xs font-bold
                          ${item.severity === 'high' ? 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-200' :
                            item.severity === 'moderate' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-200' :
                            'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-200'}`}>
                          {item.severity}
                        </span>
                      </div>
                    </div>

                    <div>
                      <label className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">Crop Type</label>
                      <p className="text-gray-900 dark:text-white capitalize">{item.crop_type || 'N/A'}</p>
                    </div>

                    <div>
                      <label className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">Date</label>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {new Date(item.detected_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>

                  <button
                    onClick={() => setSelectedItems(selectedItems.filter(i => i.id !== item.id))}
                    className="w-full py-2 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 
                               rounded-lg transition-colors font-medium"
                  >
                    Remove from comparison
                  </button>
                </div>
              ))}
            </div>

            {selectedItems.length < 3 && detections && (
              <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">Add more detections to compare:</p>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {detections
                    .filter(d => !selectedItems.find(s => s.id === d.id))
                    .slice(0, 4)
                    .map((detection) => (
                      <button
                        key={detection.id}
                        onClick={() => toggleSelection(detection)}
                        className="p-3 border border-gray-200 dark:border-gray-600 rounded-lg hover:border-primary-500 
                                   transition-colors text-left"
                      >
                        <img
                          src={`http://localhost:8000${detection.image_url}`}
                          alt={detection.disease_detected}
                          className="w-full h-20 object-cover rounded-lg mb-2"
                        />
                        <p className="text-xs font-semibold text-gray-900 dark:text-white truncate">
                          {detection.disease_detected}
                        </p>
                      </button>
                    ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ComparisonView;
