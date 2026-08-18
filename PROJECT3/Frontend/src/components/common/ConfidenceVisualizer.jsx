import React from 'react';
import { FiCheckCircle, FiAlertTriangle, FiAlertCircle } from 'react-icons/fi';

/**
 * 🎯 AI CONFIDENCE VISUALIZER COMPONENT
 * 
 * Displays AI prediction confidence with dynamic visual indicators
 * for BITS Pilani Capstone Evaluation
 * 
 * Features:
 * - Animated progress bar with color coding
 * - Confidence category badges
 * - Ensemble model breakdown
 * - Real-time confidence scoring
 */

const ConfidenceVisualizer = ({ 
  confidenceScore = 0.85, 
  confidenceCategory = "High",
  ensembleDetails = null,
  showEnsembleBreakdown = true 
}) => {
  
  // Convert to percentage if needed
  const confidencePercent = confidenceScore <= 1 ? confidenceScore * 100 : confidenceScore;
  
  // Determine color scheme based on confidence
  const getConfidenceColor = () => {
    if (confidencePercent >= 75) {
      return {
        bg: 'bg-green-100 dark:bg-green-900/20',
        border: 'border-green-500',
        text: 'text-green-700 dark:text-green-400',
        bar: 'bg-gradient-to-r from-green-500 to-emerald-600',
        icon: <FiCheckCircle className="text-green-600" size={24} />
      };
    } else if (confidencePercent >= 60) {
      return {
        bg: 'bg-yellow-100 dark:bg-yellow-900/20',
        border: 'border-yellow-500',
        text: 'text-yellow-700 dark:text-yellow-400',
        bar: 'bg-gradient-to-r from-yellow-500 to-amber-600',
        icon: <FiAlertTriangle className="text-yellow-600" size={24} />
      };
    } else {
      return {
        bg: 'bg-red-100 dark:bg-red-900/20',
        border: 'border-red-500',
        text: 'text-red-700 dark:text-red-400',
        bar: 'bg-gradient-to-r from-red-500 to-rose-600',
        icon: <FiAlertCircle className="text-red-600" size={24} />
      };
    }
  };
  
  const colors = getConfidenceColor();
  
  return (
    <div className="space-y-4">
      {/* Main Confidence Display */}
      <div className={`${colors.bg} ${colors.border} border-2 rounded-xl p-6 transition-all duration-300 hover:shadow-lg`}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            {colors.icon}
            <div>
              <h3 className="font-bold text-lg text-gray-900 dark:text-gray-100">
                AI Confidence Score
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Ensemble prediction reliability
              </p>
            </div>
          </div>
          
          {/* Confidence Badge */}
          <div className={`px-4 py-2 rounded-full ${colors.bg} ${colors.border} border ${colors.text} font-bold`}>
            {confidencePercent.toFixed(1)}%
          </div>
        </div>
        
        {/* Animated Progress Bar */}
        <div className="relative">
          <div className="w-full h-6 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden shadow-inner">
            <div 
              className={`h-full ${colors.bar} transition-all duration-1000 ease-out rounded-full flex items-center justify-end pr-3`}
              style={{ width: `${confidencePercent}%` }}
            >
              <span className="text-white text-xs font-bold drop-shadow-md">
                {confidenceCategory}
              </span>
            </div>
          </div>
          
          {/* Threshold Markers */}
          <div className="flex justify-between mt-2 text-xs text-gray-500 dark:text-gray-400">
            <span>0%</span>
            <span className="text-yellow-600">60% (Medium)</span>
            <span className="text-green-600">75% (High)</span>
            <span>100%</span>
          </div>
        </div>
      </div>
      
      {/* Ensemble Breakdown (Optional) */}
      {showEnsembleBreakdown && ensembleDetails && (
        <div className="glass-card p-5">
          <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-4 flex items-center gap-2">
            <FiAlertCircle className="text-primary-600" />
            AI Ensemble Model Breakdown
          </h4>
          
          <div className="space-y-3">
            {/* Deep Learning Model */}
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-700 dark:text-gray-300">
                  🧠 Deep Learning Model
                </span>
                <span className="font-semibold text-gray-900 dark:text-gray-100">
                  {((ensembleDetails.deep_learning?.confidence || ensembleDetails.dl_model_confidence || 0) * 100).toFixed(1)}%
                </span>
              </div>
              <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-blue-500 to-indigo-600 transition-all duration-700"
                  style={{ width: `${(ensembleDetails.deep_learning?.confidence || ensembleDetails.dl_model_confidence || 0) * 100}%` }}
                />
              </div>
            </div>
            
            {/* Computer Vision */}
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-700 dark:text-gray-300">
                  👁️ Computer Vision Analysis
                </span>
                <span className="font-semibold text-gray-900 dark:text-gray-100">
                  {((ensembleDetails.computer_vision?.confidence || ensembleDetails.cv_analysis_confidence || 0) * 100).toFixed(1)}%
                </span>
              </div>
              <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-purple-500 to-pink-600 transition-all duration-700"
                  style={{ width: `${(ensembleDetails.computer_vision?.confidence || ensembleDetails.cv_analysis_confidence || 0) * 100}%` }}
                />
              </div>
            </div>
            
            {/* Color Analysis */}
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-700 dark:text-gray-300">
                  🎨 Color Signature Analysis
                </span>
                <span className="font-semibold text-gray-900 dark:text-gray-100">
                  {((ensembleDetails.color_analysis?.confidence || ensembleDetails.color_analysis_confidence || 0) * 100).toFixed(1)}%
                </span>
              </div>
              <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-orange-500 to-red-600 transition-all duration-700"
                  style={{ width: `${(ensembleDetails.color_analysis?.confidence || ensembleDetails.color_analysis_confidence || 0) * 100}%` }}
                />
              </div>
            </div>
          </div>
          
          {/* Fusion Method Info */}
          <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <p className="text-xs text-gray-600 dark:text-gray-400">
              <span className="font-semibold">Fusion Method:</span> {ensembleDetails.fusion_method || ensembleDetails.ensemble_method || 'weighted_voting'}
            </p>
            <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
              <span className="font-semibold">Model Version:</span> {ensembleDetails.model_version || 'v2.0.0'}
            </p>
          </div>
        </div>
      )}
      
      {/* Confidence Interpretation */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <h4 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">
          💡 What does this mean?
        </h4>
        <p className="text-sm text-blue-800 dark:text-blue-400">
          {confidencePercent >= 75 ? (
            <>
              <strong>High Confidence:</strong> The AI model is very confident in this prediction. 
              All ensemble components agree on the diagnosis. Recommendations can be followed with confidence.
            </>
          ) : confidencePercent >= 60 ? (
            <>
              <strong>Medium Confidence:</strong> The AI model shows moderate confidence. 
              Consider the recommendations as guidance. Additional verification may be helpful.
            </>
          ) : (
            <>
              <strong>Low Confidence:</strong> The AI model has low confidence in this prediction. 
              Human expert verification is strongly recommended before taking action.
            </>
          )}
        </p>
      </div>
    </div>
  );
};

export default ConfidenceVisualizer;
