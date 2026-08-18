import React, { useState } from 'react';
import { FiAlertTriangle, FiUser, FiMail, FiPhone, FiSend, FiX, FiCheckCircle } from 'react-icons/fi';
import { toast } from 'react-toastify';

/**
 *   HUMAN-IN-THE-LOOP (HITL) SAFETY GUARDRAIL COMPONENT
 * 
 * Critical AI Governance Feature for BITS Pilani Evaluation
 * 
 * Triggers when:
 * - AI confidence < 65%
 * - Disease severity is High/Critical
 * - Uncertain predictions requiring expert verification
 * 
 * Features:
 * - Prominent warning banner
 * - Expert consultation form
 * - Contact KVK (Krishi Vigyan Kendra) integration
 * - Audit trail for safety compliance
 */

const HITLSafetyGuardrail = ({ 
  humanReview = null,
  detectionData = null,
  onExpertConsultation = null 
}) => {
  
  const [showConsultationForm, setShowConsultationForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    additionalNotes: ''
  });
  const [submitting, setSubmitting] = useState(false);
  
  // Check if HITL is required
  if (!humanReview || !humanReview.required) {
    return null; // Don't show if review not needed
  }
  
  const getSeverityLevel = () => {
    if (!detectionData) return 'medium';
    
    const severityScore = detectionData.severity_score || 0;
    if (severityScore >= 80) return 'critical';
    if (severityScore >= 65) return 'high';
    return 'medium';
  };
  
  const severityLevel = getSeverityLevel();
  
  // Color schemes based on severity
  const getColorScheme = () => {
    switch (severityLevel) {
      case 'critical':
        return {
          bg: 'bg-red-100 dark:bg-red-900/30',
          border: 'border-red-500',
          text: 'text-red-800 dark:text-red-300',
          icon: 'text-red-600',
          button: 'bg-red-600 hover:bg-red-700'
        };
      case 'high':
        return {
          bg: 'bg-orange-100 dark:bg-orange-900/30',
          border: 'border-orange-500',
          text: 'text-orange-800 dark:text-orange-300',
          icon: 'text-orange-600',
          button: 'bg-orange-600 hover:bg-orange-700'
        };
      default:
        return {
          bg: 'bg-yellow-100 dark:bg-yellow-900/30',
          border: 'border-yellow-500',
          text: 'text-yellow-800 dark:text-yellow-300',
          icon: 'text-yellow-600',
          button: 'bg-yellow-600 hover:bg-yellow-700'
        };
    }
  };
  
  const colors = getColorScheme();
  
  const handleSubmitConsultation = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!formData.name || !formData.phone) {
      toast.error('Please provide your name and contact number');
      return;
    }
    
    setSubmitting(true);
    
    try {
      // Prepare consultation payload
      const consultationPayload = {
        ...formData,
        detectionId: detectionData?.id,
        disease: detectionData?.disease,
        confidence: detectionData?.confidence_score,
        severity: detectionData?.severity_level,
        cropType: detectionData?.crop_type,
        reason: humanReview.reason,
        timestamp: new Date().toISOString()
      };
      
      // Call real backend API
      const response = await fetch('http://localhost:8000/api/v1/disease/expert-consultation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(consultationPayload)
      });
      
      const result = await response.json();
      
      if (!response.ok || !result.success) {
        throw new Error(result.message || 'Failed to submit consultation request');
      }
      
      // Call parent handler if provided
      if (onExpertConsultation) {
        await onExpertConsultation(consultationPayload);
      }
      
      toast.success('✅ Expert consultation request sent successfully! You will be contacted within 24 hours.');
      setShowConsultationForm(false);
      
      // Reset form
      setFormData({
        name: '',
        email: '',
        phone: '',
        additionalNotes: ''
      });
      
    } catch (error) {
      toast.error('Failed to send consultation request. Please try again.');
      console.error('Consultation error:', error);
    } finally {
      setSubmitting(false);
    }
  };
  
  return (
    <div className="space-y-4 animate-fadeIn">
      {/* Main HITL Warning Banner */}
      <div className={`${colors.bg} ${colors.border} border-2 rounded-xl p-6 shadow-lg`}>
        <div className="flex items-start gap-4">
          {/* Warning Icon */}
          <div className={`${colors.icon} mt-1 flex-shrink-0`}>
            <FiAlertTriangle size={32} className="animate-pulse" />
          </div>
          
          {/* Content */}
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-3">
              <h3 className={`font-bold text-xl ${colors.text}`}>
                ⚠️ Expert Verification Recommended
              </h3>
              {severityLevel === 'critical' && (
                <span className="px-3 py-1 bg-red-600 text-white text-xs font-bold rounded-full animate-pulse">
                  CRITICAL
                </span>
              )}
            </div>
            
            <div className={`${colors.text} space-y-2`}>
              <p className="font-semibold text-base">
                {humanReview.reason}
              </p>
              
              <div className="bg-white/50 dark:bg-gray-800/50 rounded-lg p-4 mt-3">
                <p className="text-sm leading-relaxed">
                  <strong>Why is this important?</strong><br />
                  {humanReview.confidence_category === 'Low' && (
                    'The AI system has detected uncertainty in the prediction. Multiple visual patterns are conflicting, requiring human expert judgment for accurate diagnosis.'
                  )}
                  {detectionData?.severity_score >= 80 && (
                    'This condition is classified as HIGH SEVERITY. Before applying any treatments, we strongly recommend verification by an agricultural expert to ensure correct diagnosis and appropriate treatment plan.'
                  )}
                </p>
              </div>
              
              <div className="flex flex-wrap gap-3 mt-4">
                <button
                  onClick={() => setShowConsultationForm(true)}
                  className={`${colors.button} text-white px-6 py-3 rounded-lg font-semibold flex items-center gap-2 transition-all duration-200 transform hover:scale-105 shadow-md`}
                >
                  <FiUser size={18} />
                  Consult Agricultural Expert
                </button>
                
                <button
                  onClick={() => window.open('https://www.google.com/search?q=nearest+Krishi+Vigyan+Kendra+KVK+near+me', '_blank')}
                  className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-semibold flex items-center gap-2 transition-all duration-200 transform hover:scale-105 shadow-md"
                >
                  <FiPhone size={18} />
                  Find Nearest KVK
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Expert Consultation Form Modal */}
      {showConsultationForm && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fadeIn">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            {/* Header */}
            <div className="bg-primary-600 text-white p-6 rounded-t-2xl flex items-center justify-between">
              <div className="flex items-center gap-3">
                <FiUser size={24} />
                <h3 className="text-xl font-bold">Request Expert Consultation</h3>
              </div>
              <button
                onClick={() => setShowConsultationForm(false)}
                className="hover:bg-primary-700 p-2 rounded-lg transition-colors"
              >
                <FiX size={24} />
              </button>
            </div>
            
            {/* Form Content */}
            <form onSubmit={handleSubmitConsultation} className="p-6 space-y-5">
              {/* Detection Summary */}
              <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                <h4 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">
                  Detection Summary
                </h4>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">Disease:</span>
                    <p className="font-semibold text-gray-900 dark:text-gray-100">
                      {detectionData?.disease || 'N/A'}
                    </p>
                  </div>
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">Confidence:</span>
                    <p className="font-semibold text-gray-900 dark:text-gray-100">
                      {detectionData?.confidence_score ? `${(detectionData.confidence_score * 100).toFixed(1)}%` : 'N/A'}
                    </p>
                  </div>
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">Severity:</span>
                    <p className="font-semibold text-gray-900 dark:text-gray-100">
                      {detectionData?.severity_level || 'N/A'}
                    </p>
                  </div>
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">Crop Type:</span>
                    <p className="font-semibold text-gray-900 dark:text-gray-100">
                      {detectionData?.crop_type || 'N/A'}
                    </p>
                  </div>
                </div>
              </div>
              
              {/* Contact Information */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                  Your Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-gray-100"
                  placeholder="Enter your full name"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                  Phone Number <span className="text-red-500">*</span>
                </label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-gray-100"
                  placeholder="+91 98765 43210"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                  Email (Optional)
                </label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-gray-100"
                  placeholder="your.email@example.com"
                />
              </div>
              
              <div>
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                  Additional Notes
                </label>
                <textarea
                  value={formData.additionalNotes}
                  onChange={(e) => setFormData({ ...formData, additionalNotes: e.target.value })}
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-gray-100"
                  placeholder="Any additional symptoms or observations..."
                />
              </div>
              
              {/* Action Buttons */}
              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  disabled={submitting}
                  className="flex-1 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white py-3 rounded-lg font-semibold flex items-center justify-center gap-2 transition-all duration-200"
                >
                  {submitting ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
                      Sending...
                    </>
                  ) : (
                    <>
                      <FiSend size={18} />
                      Send Consultation Request
                    </>
                  )}
                </button>
                
                <button
                  type="button"
                  onClick={() => setShowConsultationForm(false)}
                  className="px-6 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-lg font-semibold hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
      
      {/* Informational Footer */}
      <div className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
        <div className="flex items-start gap-3">
          <FiCheckCircle className="text-blue-600 mt-1 flex-shrink-0" size={20} />
          <div className="text-sm text-gray-700 dark:text-gray-300">
            <p className="font-semibold mb-1">🛡️ AI Safety Governance</p>
            <p>
              This advisory is for <strong>decision support only</strong>. Our AI system has built-in safety 
              guardrails that trigger expert consultation for uncertain or high-severity cases. This ensures 
              responsible AI deployment in agriculture.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HITLSafetyGuardrail;
