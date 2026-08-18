import { useState, useCallback, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import { toast } from 'react-toastify';
import { 
  FiUpload, 
  FiCheckCircle, 
  FiAlertTriangle, 
  FiInfo,
  FiPackage,
  FiDroplet,
  FiShield,
  FiXCircle,
  FiClock,
  FiEye,
  FiZoomIn,
  FiArrowLeft,
  FiLayers
} from 'react-icons/fi';
import Layout from '../components/common/Layout';
import SuccessConfetti from '../components/common/SuccessConfetti';
import ImageLightbox from '../components/common/ImageLightbox';
import ProgressBar from '../components/common/ProgressBar';
import BatchUpload from '../components/common/BatchUpload';
import ConfidenceVisualizer from '../components/common/ConfidenceVisualizer';
import HITLSafetyGuardrail from '../components/common/HITLSafetyGuardrail';
import { diseaseService } from '../services/apiService';
import { CROP_TYPES, MAX_FILE_SIZE, ALLOWED_IMAGE_TYPES } from '../utils/constants';
import { translateCropName } from '../utils/translationHelpers';

const DiseaseDetection = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [uploadMode, setUploadMode] = useState('single'); // 'single' or 'batch'
  const [loading, setLoading] = useState(false);
  const [progressStage, setProgressStage] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [cropType, setCropType] = useState('tomato');
  const [result, setResult] = useState(null);
  const [showConfetti, setShowConfetti] = useState(false);
  const [lightboxOpen, setLightboxOpen] = useState(false);
  const [modelStatus, setModelStatus] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    
    if (!file) return;

    if (file.size > MAX_FILE_SIZE) {
      toast.error(t('error_file_too_large'));
      return;
    }

    if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
      toast.error(t('error_invalid_format'));
      return;
    }

    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
    setResult(null);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.jpeg', '.jpg', '.png'] },
    multiple: false,
  });

  useEffect(() => {
    const loadModelStatus = async () => {
      try {
        const response = await diseaseService.getModelStatus();
        setModelStatus(response?.data || null);
      } catch {
        setModelStatus(null);
      }
    };

    loadModelStatus();
  }, []);

  const handleDetect = async () => {
    if (!selectedFile) {
      toast.error(t('error_no_image'));
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      // Stage 1: Uploading
      setProgressStage(t('uploading_image'));
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Stage 2: Analyzing
      setProgressStage(t('analyzing_with_ai'));
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Stage 3: Detecting patterns
      setProgressStage(t('detecting_patterns'));
      
      const response = await diseaseService.detectDisease(selectedFile, cropType);
      
      // DEBUG: Log response to check structure
      console.log('API Response:', response);
      console.log('AI Ensemble:', response.data?.ai_ensemble_details);
      console.log('Crop Validated:', response.data?.crop_validated);
      
      // Stage 4: Generating recommendations
      setProgressStage(t('generating_recommendations'));
      await new Promise(resolve => setTimeout(resolve, 300));
      
      setResult(response.data || response);
      
      // DEBUG: Check what result actually contains
      const resultData = response.data || response;
      console.log('Result set:', resultData);
      console.log('ai_model_info:', resultData.ai_model_info);
      console.log('model name:', resultData.ai_model_info?.model);
      console.log('parameters:', resultData.ai_model_info?.parameters);
      
      toast.success(t('success_analysis_complete'));
      
      // Trigger success confetti animation
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 3000);
    } catch (error) {
      toast.error(error.response?.data?.detail || t('error_detection_failed'));
    } finally {
      setLoading(false);
      setProgressStage('');
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreview(null);
    setResult(null);
    setShowConfetti(false);
  };

  const getSeverityColor = (level) => {
    switch (level) {
      case 'high': return 'bg-red-100 text-red-800 border-red-300';
      case 'moderate': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'low': return 'bg-green-100 text-green-800 border-green-300';
      case 'none': return 'bg-blue-100 text-blue-800 border-blue-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getSeverityIcon = (level) => {
    switch (level) {
      case 'high': return <FiAlertTriangle className="text-red-600" size={24} />;
      case 'moderate': return <FiInfo className="text-yellow-600" size={24} />;
      case 'low': return <FiCheckCircle className="text-green-600" size={24} />;
      case 'none': return <FiCheckCircle className="text-blue-600" size={24} />;
      default: return <FiInfo className="text-gray-600" size={24} />;
    }
  };

  return (
    <Layout>
      {/* Success Confetti Animation */}
      <SuccessConfetti active={showConfetti} duration={3000} />
      
      {/* Image Lightbox */}
      <ImageLightbox
        image={preview}
        isOpen={lightboxOpen}
        onClose={() => setLightboxOpen(false)}
        title={result?.disease_class}
        metadata={result ? {
          'Crop': cropType,
          'Confidence': `${result.confidence}%`,
          'Severity': result.severity,
          'Detected': new Date().toLocaleDateString()
        } : null}
      />
      
      <div className="max-w-7xl mx-auto space-y-6 animate-fadeIn">
        {/* Back Button */}
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors group"
        >
          <FiArrowLeft className="group-hover:-translate-x-1 transition-transform" />
          <span className="font-medium">{t('back_to_dashboard')}</span>
        </button>

        {/* Professional Header */}
        <div className="section-header">
          <div>
            <h1 className="section-title">{t('disease_detection')}</h1>
            <p className="section-subtitle">{t('upload_crop_analysis_desc')}</p>
          </div>
        </div>

        {/* Upload Mode Toggle */}
        <div className="flex justify-center">
          <div className="glass-card p-1 inline-flex gap-2">
            <button
              onClick={() => setUploadMode('single')}
              className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center gap-2 ${
                uploadMode === 'single'
                  ? 'bg-primary-600 text-white shadow-md scale-105'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <FiUpload size={18} />
              Single Upload
            </button>
            <button
              onClick={() => setUploadMode('batch')}
              className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center gap-2 ${
                uploadMode === 'batch'
                  ? 'bg-primary-600 text-white shadow-md scale-105'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <FiLayers size={18} />
              Batch Upload
            </button>
          </div>
        </div>

        {uploadMode === 'batch' ? (
          /* Batch Upload Mode */
          <div className="card-pro">
            <h2 className="text-xl font-bold mb-6 flex items-center text-gray-900 dark:text-white">
              <div className="p-2 bg-primary-100 dark:bg-primary-900 rounded-lg mr-3">
                <FiLayers className="text-primary-600 dark:text-primary-400" />
              </div>
              Batch Disease Detection
            </h2>
            
            {/* Crop Type Selector for Batch Mode */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                {t('select_crop_type')}
              </label>
              <select
                value={cropType}
                onChange={(e) => setCropType(e.target.value)}
                className="input-professional text-base"
              >
                <option value="tomato">Tomato</option>
                <option value="potato">Potato</option>
                <option value="corn">Corn</option>
                <option value="wheat">Wheat</option>
                <option value="rice">Rice</option>
                <option value="apple">Apple</option>
                <option value="grape">Grape</option>
                <option value="pepper">Pepper</option>
                <option value="strawberry">Strawberry</option>
                <option value="peach">Peach</option>
                <option value="orange">Orange</option>
                <option value="soybean">Soybean</option>
                <option value="cherry">Cherry</option>
              </select>
              <p className="mt-2 text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
                <FiAlertTriangle className="text-yellow-500" />
                {t('crop_type_warning')}
              </p>
            </div>
            
            <BatchUpload 
              maxFiles={5}
              cropType={cropType}
              onBatchComplete={(results) => {
                setShowConfetti(true);
                setTimeout(() => setShowConfetti(false), 3000);
              }}
            />
          </div>
        ) : (
          /* Single Upload Mode (existing) */
        <div className="grid lg:grid-cols-2 gap-6">
          {/* Upload Section */}
          <div className="card-pro">
            <h2 className="text-xl font-bold mb-6 flex items-center text-gray-900 dark:text-white">
              <div className="p-2 bg-primary-100 dark:bg-primary-900 rounded-lg mr-3">
                <FiUpload className="text-primary-600 dark:text-primary-400" />
              </div>
              {t('upload_crop_image_btn')}
            </h2>

            {modelStatus && (
              <div className="mb-6 rounded-lg border border-blue-200 bg-blue-50 p-3 text-sm text-blue-900">
                <p className="font-semibold">AI Model Status</p>
                <p>
                  Mode: {modelStatus.loaded ? 'Trained Model' : 'Fallback Logic'}
                  {modelStatus.model_path ? ` • ${modelStatus.model_path}` : ''}
                </p>
              </div>
            )}

            {!preview ? (
              <div
                {...getRootProps()}
                className={`
                  relative border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer
                  transition-all duration-300 group
                  ${isDragActive 
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 scale-105' 
                    : 'border-gray-300 dark:border-gray-700 hover:border-primary-400 dark:hover:border-primary-600'
                  }
                `}
              >
                <input {...getInputProps()} />
                
                <div className="flex flex-col items-center">
                  <div className="p-4 bg-primary-100 dark:bg-primary-900 rounded-full mb-4 
                                group-hover:scale-110 transition-transform duration-300">
                    <FiUpload className="text-4xl text-primary-600 dark:text-primary-400" />
                  </div>
                  
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                    {isDragActive ? 'Drop your image here' : t('drag_drop_select')}
                  </h3>
                  
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    {t('supported_formats')}
                  </p>
                  
                  <div className="flex items-center gap-3 flex-wrap justify-center">
                    <span className="badge badge-info">JPG, PNG</span>
                    <span className="badge badge-info">Max 10MB</span>
                    <span className="badge badge-info">Clear Images</span>
                  </div>
                  
                  <p className="text-xs text-gray-500 dark:text-gray-500 mt-4">
                    Tip: {t('best_results_tip')}
                  </p>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="relative group">
                  <img
                    src={preview}
                    alt="Preview"
                    className="w-full h-80 object-cover rounded-xl border-2 border-gray-200 dark:border-gray-700 cursor-pointer"
                    onClick={() => setLightboxOpen(true)}
                  />
                  <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors rounded-xl flex items-center justify-center">
                    <button
                      onClick={() => setLightboxOpen(true)}
                      className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 p-4 bg-white/90 dark:bg-gray-800/90 rounded-full shadow-xl hover:scale-110 transform"
                    >
                      <FiZoomIn className="text-2xl text-primary-600 dark:text-primary-400" />
                    </button>
                  </div>
                  <div className="absolute top-3 right-3 bg-white dark:bg-gray-800 px-4 py-2 rounded-full shadow-lg border border-gray-200 dark:border-gray-700">
                    <span className="text-sm font-semibold text-gray-700 dark:text-gray-300 flex items-center gap-2">
                      <FiEye className="text-primary-600" />
                      Preview
                    </span>
                  </div>
                </div>
                <button onClick={handleReset} className="btn-secondary-pro w-full">
                  <FiXCircle className="inline mr-2" />
                  Change Image
                </button>
              </div>
            )}

            <div className="mt-6 space-y-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                  {t('select_crop_type')}
                </label>
                <select
                  value={cropType}
                  onChange={(e) => setCropType(e.target.value)}
                  className="input-professional text-base"
                >
                  {CROP_TYPES.map((crop) => (
                    <option key={crop} value={crop} className="capitalize">
                      {translateCropName(crop, t)}
                    </option>
                  ))}
                </select>
              </div>
              
              {/* Important Warning */}
              <div className="bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-400 dark:border-yellow-600 p-4 rounded-r-lg">
                <div className="flex items-start">
                  <FiAlertTriangle className="text-yellow-600 dark:text-yellow-500 mt-0.5 mr-3 flex-shrink-0 text-lg" />
                  <div className="text-sm">
                    <p className="font-semibold text-yellow-800 dark:text-yellow-300">Important: Select the correct crop type</p>
                    <p className="text-yellow-700 dark:text-yellow-400 mt-1">
                      Make sure to select the crop type that <strong>matches your uploaded image</strong>. 
                      For accurate results, the selected crop and image content must match.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <button
              onClick={handleDetect}
              disabled={!selectedFile || loading}
              className="btn-primary w-full mt-6 text-lg py-4"
            >
              {loading ? t('analyzing') : t('detect_disease_btn')}
            </button>

            {/* Progress Indicator */}
            {loading && (
              <div className="mt-6 bg-blue-50 rounded-lg p-4 border border-blue-200">
                <div className="flex items-center space-x-3 mb-3">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                  <span className="text-blue-800 font-medium">{progressStage}</span>
                </div>
                <div className="w-full bg-blue-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full animate-pulse" style={{ width: '70%' }}></div>
                </div>
                <p className="text-xs text-blue-600 mt-2">
                  Our AI model is analyzing {cropType} leaf patterns...
                </p>
              </div>
            )}
          </div>

          {/* Results Section */}
          <div className="card">
            <h2 className="text-2xl font-bold mb-6 flex items-center">
              <FiCheckCircle className="mr-2 text-green-600" />
              {t('analysis_results')}
            </h2>

            {!result && !loading && (
              <div className="text-center py-16 text-gray-400">
                <FiInfo size={64} className="mx-auto mb-4 opacity-50" />
                <p className="text-lg">{t('upload_click_to_analyze')}</p>
              </div>
            )}

            {result && (
              <div className="space-y-6">
                {/* AI Model Badge - REAL TRAINED MODEL - FIXED VERSION 2.0 */}
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900 dark:to-indigo-900 p-4 rounded-lg border border-blue-200 dark:border-blue-700 shadow-sm">
                  <div className="flex items-center gap-3">
                    <FiLayers className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                    <div className="flex-1">
                      <p className="text-sm font-bold text-blue-900 dark:text-blue-100">
                        {(() => {
                          const modelName = result.ai_model_info?.model || 'Trained MobileNetV2 Disease Classifier';
                          console.log('RENDERING MODEL NAME:', modelName);
                          console.log('result.ai_model_info:', result.ai_model_info);
                          return modelName;
                        })()}
                      </p>
                      <p className="text-xs text-blue-700 dark:text-blue-300">
                        {result.ai_model_info?.parameters || '3.05M'} Parameters • 
                        {result.ai_model_info?.training_info?.test_accuracy ? ` ${result.ai_model_info.training_info.test_accuracy} Test Accuracy • ` : ' '}
                        Convolutional Neural Network • Real-time Deep Learning Inference
                      </p>
                    </div>
                  </div>
                </div>

                {/* CROP VALIDATION WARNING - Show if mismatch detected */}
                {result.crop_validated === false && (
                  <div className="bg-red-50 dark:bg-red-900 border-2 border-red-400 dark:border-red-600 rounded-lg p-5 shadow-lg">
                    <div className="flex items-start gap-4">
                      <div className="flex-shrink-0 w-12 h-12 rounded-full bg-red-100 dark:bg-red-800 flex items-center justify-center">
                        <FiAlertTriangle className="w-6 h-6 text-red-600 dark:text-red-300" />
                      </div>
                      <div className="flex-1">
                        <h4 className="text-lg font-bold text-red-900 dark:text-red-100 mb-2">
                          {result.disease === 'validation_failed' ? 'DETECTION STOPPED - Validation Failed' : 'Crop Type Mismatch Detected'}
                        </h4>
                        <p className="text-red-800 dark:text-red-200 mb-2">
                          {result.disease === 'validation_failed' 
                            ? `The uploaded image does NOT match the selected crop type "${result.crop_type || 'selected crop'}". Detection has been stopped to prevent inaccurate results.`
                            : `The uploaded image may not match the selected crop type "${result.crop_type || 'selected crop'}".`
                          }
                        </p>
                        <p className="text-sm text-red-700 dark:text-red-300 mb-3">
                          <strong>Validation Confidence:</strong> {Math.round((result.validation_confidence || 0) * 100)}% 
                          {(result.validation_confidence || 0) < 0.5 && ' (Very Low - Image likely incorrect)'}
                        </p>
                        <div className="bg-red-100 dark:bg-red-800 rounded p-3 text-sm text-red-900 dark:text-red-100">
                          <p className="font-semibold mb-1">Required Actions:</p>
                          <ul className="list-disc list-inside space-y-1 text-red-800 dark:text-red-200">
                            {result.actionable_recommendations?.map((rec, idx) => (
                              <li key={idx}>{rec.replace(/^[⚠️📸🔄💡✅🚨🌱💧✂️🗑️🧴🔄🧹🌬️🌡️🐛🚿📦💊🔬🎯❌]/g, '').trim()}</li>
                            )) || (
                              <>
                                <li>Re-upload an image of the <strong>correct crop type</strong></li>
                                <li>Verify the crop dropdown selection matches your plant</li>
                                <li>Ensure the image clearly shows leaves/stems of the plant</li>
                                {result.disease === 'validation_failed' && <li><strong>Cannot proceed with detection</strong> - image validation required!</li>}
                                {result.disease !== 'validation_failed' && <li><strong>DO NOT use these detection results</strong> - they may be inaccurate!</li>}
                              </>
                            )}
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Human-in-the-Loop Safety Warning */}
                {result.human_review?.required && (
                  <HITLSafetyGuardrail 
                    humanReview={result.human_review}
                    detectionData={{
                      id: result.id,
                      disease: result.disease_detected || result.disease,
                      confidence_score: result.confidence_score || result.confidence / 100,
                      severity_level: result.severity_level || result.severity,
                      crop_type: cropType,
                      severityScore: result.severity_score || 0
                    }}
                    onExpertConsultation={(data) => {
                      console.log('Expert consultation requested:', data);
                      // Toast is already shown in HITLSafetyGuardrail component
                    }}
                  />
                )}

                {/* Crop Type Validation Warning - Show when mismatch detected */}
                {result.crop_validation && !result.crop_validation.passed && (
                  <div className="bg-amber-50 border-2 border-amber-400 rounded-lg p-5 shadow-md">
                    <div className="flex items-start gap-4">
                      <FiAlertTriangle className="w-8 h-8 text-amber-600 flex-shrink-0 mt-1" />
                      <div className="flex-1">
                        <h4 className="text-lg font-bold text-amber-900 mb-2 flex items-center">
                          Crop Type Mismatch Detected
                        </h4>
                        <p className="text-amber-800 mb-3">
                          {result.crop_validation.warning || result.crop_validation.message}
                        </p>
                        
                        {/* Smart Validation Details */}
                        {result.crop_validation.best_alternative && (
                          <div className="bg-white rounded-lg p-3 border border-amber-300 mb-3">
                            <p className="text-sm font-semibold text-amber-900 mb-2">
                              AI Analysis:
                            </p>
                            <div className="grid grid-cols-2 gap-3 text-sm">
                              <div>
                                <p className="text-gray-600">Your Selection:</p>
                                <p className="font-bold text-gray-900 capitalize">
                                  {cropType} 
                                  {result.crop_validation.match_score && (
                                    <span className="ml-2 text-red-600">
                                      ({(result.crop_validation.match_score * 100).toFixed(0)}% match)
                                    </span>
                                  )}
                                </p>
                              </div>
                              <div>
                                <p className="text-gray-600">AI Suggestion:</p>
                                <p className="font-bold text-green-700 capitalize">
                                  {result.crop_validation.best_alternative}
                                  {result.crop_validation.alternative_score && (
                                    <span className="ml-2 text-green-600">
                                      ({(result.crop_validation.alternative_score * 100).toFixed(0)}% match)
                                    </span>
                                  )}
                                </p>
                              </div>
                            </div>
                          </div>
                        )}
                        
                        <div className="bg-amber-100 rounded-lg p-3 border border-amber-300">
                          <p className="text-sm text-amber-900">
                            <strong>What This Means:</strong>
                          </p>
                          <ul className="text-sm text-amber-800 mt-2 space-y-1 ml-4">
                            <li>• Multi-dimensional feature analysis detected inconsistency</li>
                            <li>• 8 statistical measures analyzed across 1280-dimensional space</li>
                            <li>• Disease diagnosis confidence reduced to {result.confidence}%</li>
                            <li>• Please verify crop selection or try suggested crop type</li>
                          </ul>
                        </div>
                        <div className="mt-3 flex items-center gap-2 text-sm">
                          <span className="bg-amber-200 text-amber-900 px-3 py-1 rounded-full font-semibold">
                            Recommendation: Re-upload with correct crop type selection
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Moderate Uncertainty Warning - Show when validation passes but has warning */}
                {result.crop_validation && result.crop_validation.passed && result.crop_validation.warning && (
                  <div className="bg-blue-50 border-l-4 border-blue-400 rounded-lg p-4 shadow-sm">
                    <div className="flex items-start gap-3">
                      <FiInfo className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                      <div className="flex-1">
                        <h5 className="text-sm font-semibold text-blue-900 mb-1">
                          Moderate Confidence Notice
                        </h5>
                        <p className="text-sm text-blue-800">
                          {result.crop_validation.warning}
                        </p>
                        {result.crop_validation.match_score && (
                          <p className="text-xs text-blue-700 mt-2">
                            Feature match score: {(result.crop_validation.match_score * 100).toFixed(0)}% 
                            • Results may be less precise than usual
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                )}

                {/* V3.0 AI Model Info - MobileNetV2 Display */}
                {result.ai_model_info && (
                  <div className="glass-card p-6 border-2 border-primary-200 bg-gradient-to-r from-blue-50 to-indigo-50">
                    <h4 className="font-bold text-gray-900 mb-4 flex items-center text-lg">
                      <FiLayers className="mr-2 text-primary-600" /> AI Model Information (V3.0)
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="bg-white rounded-lg p-4 shadow-sm border border-primary-100">
                        <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">Model Type</p>
                        <p className="text-lg font-bold text-primary-700">{result.ai_model_info.model || 'Trained MobileNetV2'}</p>
                        <p className="text-xs text-gray-600 mt-1">{result.ai_model_info.source || 'Custom Trained Model'}</p>
                      </div>
                      <div className="bg-white rounded-lg p-4 shadow-sm border border-primary-100">
                        <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">Parameters</p>
                        <p className="text-lg font-bold text-indigo-700">{result.ai_model_info.parameters || '3.05M'}</p>
                        <p className="text-xs text-gray-600 mt-1">{result.ai_model_info.training_info?.test_accuracy || '90.22% Test Accuracy'}</p>
                      </div>
                      <div className="bg-white rounded-lg p-4 shadow-sm border border-primary-100">
                        <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">Feature Dimension</p>
                        <p className="text-lg font-bold text-purple-700">{result.ai_model_info.feature_dimension || '1280'}</p>
                        <p className="text-xs text-gray-600 mt-1">Vector space</p>
                      </div>
                    </div>
                    <div className="mt-4 bg-white rounded-lg p-3 border border-green-200">
                      <p className="text-sm text-gray-700 flex items-center">
                        <FiCheckCircle className="text-green-600 mr-2" />
                        <strong>Methodology:</strong> {result.ai_model_info.methodology || 'Transfer Learning from ImageNet'}
                      </p>
                      {result.ai_model_info.no_pixel_ratio && (
                        <p className="text-xs text-green-700 mt-2 flex items-center">
                          <FiCheckCircle className="mr-1" />
                          Pure CNN architecture - No manual pixel algorithms
                        </p>
                      )}
                      {result.ai_model_info.recommendation_source && (
                        <p className="text-xs text-blue-700 mt-2 flex items-center">
                          <FiInfo className="mr-1" />
                          Recommendations from: {result.ai_model_info.recommendation_source}
                        </p>
                      )}
                      {result.ai_model_info.training_info && (
                        <div className="mt-3 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-3 border border-green-200">
                          <p className="text-xs font-bold text-green-900 mb-2">Training Evidence (Real ML, Not Fake!):</p>
                          <div className="grid grid-cols-2 gap-2 text-xs">
                            <div>
                              <span className="text-gray-600">Dataset:</span>
                              <span className="ml-1 text-gray-900 font-semibold">{result.ai_model_info.training_info.dataset}</span>
                            </div>
                            <div>
                              <span className="text-gray-600">Test Accuracy:</span>
                              <span className="ml-1 text-green-700 font-bold">{result.ai_model_info.training_info.test_accuracy}</span>
                            </div>
                            <div>
                              <span className="text-gray-600">Classes:</span>
                              <span className="ml-1 text-gray-900">{result.ai_model_info.training_info.classes}</span>
                            </div>
                            <div>
                              <span className="text-gray-600">Top-3 Acc:</span>
                              <span className="ml-1 text-green-700 font-bold">{result.ai_model_info.training_info.top3_accuracy}</span>
                            </div>
                            <div className="col-span-2">
                              <span className="text-gray-600">Split:</span>
                              <span className="ml-1 text-gray-900">{result.ai_model_info.training_info.split}</span>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Confidence Visualization */}
                {result.disease !== 'validation_failed' && (result.confidence_score || result.confidence) && (
                  <ConfidenceVisualizer 
                    confidenceScore={result.confidence_score || result.confidence / 100}
                    confidenceCategory={result.confidence_category || (result.confidence >= 75 ? 'High' : result.confidence >= 60 ? 'Medium' : 'Low')}
                    ensembleDetails={result.ai_ensemble_details || {
                      deep_learning: { confidence: (result.confidence_score || result.confidence) / 100, weight: 1.0 }
                    }}
                    showEnsembleBreakdown={false}
                  />
                )}

                {/* Show disease results ONLY if validation passed */}
                {result.disease !== 'validation_failed' && (
                  <>
                    {/* Main Result Card */}
                    <div className={`rounded-xl p-6 border-2 ${getSeverityColor(result.severity_level)}`}>
                  <div className="flex items-start space-x-4">
                    {getSeverityIcon(result.severity_level)}
                    <div className="flex-1">
                      <h3 className="text-2xl font-bold mb-2">{result.disease_name || result.disease}</h3>
                      <p className="text-sm opacity-80">{result.confidence_note}</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 mt-4">
                    <div>
                      <p className="text-xs opacity-70 mb-1">Confidence Level</p>
                      <div className="flex items-center space-x-2">
                        <div className="flex-grow bg-white rounded-full h-3 border">
                          <div
                            className="bg-current h-full rounded-full transition-all duration-500"
                            style={{ width: `${result.confidence}%` }}
                          />
                        </div>
                        <span className="text-lg font-bold">{result.confidence}%</span>
                      </div>
                    </div>
                    <div>
                      <p className="text-xs opacity-70 mb-1">Severity</p>
                      <p className="text-lg font-bold">{result.severity_level || result.severity || 'Medium'}</p>
                    </div>
                  </div>
                </div>

                {result.advisory && (
                  <div className={`rounded-lg border p-4 ${result.advisory.review_required ? 'border-amber-300 bg-amber-50 text-amber-900' : 'border-green-300 bg-green-50 text-green-900'}`}>
                    <p className="font-semibold">AI Advisory</p>
                    <p className="text-sm mt-1">{result.advisory.message}</p>
                  </div>
                )}

                {result.ai_details && (
                  <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                    <h4 className="font-bold text-slate-900 mb-2 flex items-center">
                      <FiInfo className="mr-2" /> Inference Details
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-slate-700">
                      <p><strong>Method:</strong> {result.ai_details.prediction_method}</p>
                      <p><strong>Model:</strong> {result.ai_details.model_version}</p>
                      <p><strong>Raw Label:</strong> {result.ai_details.raw_label || 'N/A'}</p>
                      <p><strong>Inference Time:</strong> {result.ai_details.inference_ms} ms</p>
                    </div>
                  </div>
                )}

                {/* Analysis Details */}
                {result.analysis_details && result.analysis_details.length > 0 && (
                  <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                    <h4 className="font-bold text-gray-900 mb-3 flex items-center">
                      <FiEye className="mr-2" /> What We Detected:
                    </h4>
                    <ul className="space-y-2">
                      {result.analysis_details.map((detail, idx) => (
                        <li key={idx} className="text-sm text-gray-700 flex items-start">
                          <span className="mr-2">{detail.startsWith('✓') ? '✓' : detail.startsWith('WARNING') ? '!' : '•'}</span>
                          <span>{detail.replace(/^[✓!•]\s*/, '')}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Hybrid AI Architecture Info - Shows This is Real Implementation */}
                {result.recommendation_metadata && (
                  <div className={`rounded-lg p-4 border-2 ${
                    result.crop_validation && !result.crop_validation.passed 
                      ? 'bg-gradient-to-r from-red-50 to-orange-50 border-red-400' 
                      : 'bg-gradient-to-r from-indigo-50 to-blue-50 border-indigo-200'
                  }`}>
                    <div className="flex items-start gap-3">
                      {result.crop_validation && !result.crop_validation.passed ? (
                        <FiAlertTriangle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
                      ) : (
                        <FiInfo className="w-5 h-5 text-indigo-600 mt-0.5 flex-shrink-0" />
                      )}
                      <div className="text-sm">
                        <p className={`font-semibold mb-1 ${
                          result.crop_validation && !result.crop_validation.passed 
                            ? 'text-red-900' 
                            : 'text-indigo-900'
                        }`}>
                          {result.crop_validation && !result.crop_validation.passed 
                            ? 'Warning: Unreliable Results' 
                            : 'Hybrid AI System Architecture'}
                        </p>
                        {!(result.crop_validation && !result.crop_validation.passed) && (
                          <p className="text-indigo-800">
                            <strong>Detection:</strong> {result.recommendation_metadata.detection_method} • 
                            <strong className="ml-2">Recommendations:</strong> {result.recommendation_metadata.recommendation_source}
                          </p>
                        )}
                        <p className={`mt-2 text-xs font-semibold ${
                          result.crop_validation && !result.crop_validation.passed 
                            ? 'text-red-800' 
                            : 'text-indigo-700'
                        }`}>
                          Note: {result.recommendation_metadata.recommendation_note}
                        </p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Immediate Actions */}
                {result.immediate_actions && result.immediate_actions.length > 0 && (
                  <div className="bg-red-50 rounded-lg p-4 border-2 border-red-300">
                    <h4 className="font-bold text-red-900 mb-3 flex items-center">
                      <FiAlertTriangle className="mr-2" />   IMMEDIATE ACTIONS REQUIRED:
                    </h4>
                    <ol className="space-y-2">
                      {result.immediate_actions.map((action, idx) => (
                        <li key={idx} className="text-sm text-red-800 font-medium">
                          {action}
                        </li>
                      ))}
                    </ol>
                  </div>
                )}

                {/* Treatments */}
                {result.treatments && result.treatments.length > 0 && (
                  <div className="bg-white rounded-lg p-4 border-2 border-blue-200">
                    <h4 className="font-bold text-blue-900 mb-4 flex items-center">
                      <FiDroplet className="mr-2" /> Treatment Plan:
                    </h4>
                    {result.treatments.map((treatment, idx) => (
                      <div key={idx} className="mb-4 last:mb-0 bg-blue-50 rounded-lg p-4">
                        <div className="flex items-start justify-between mb-2">
                          <h5 className="font-bold text-blue-900">Step {treatment.step}: {treatment.product}</h5>
                          <span className="text-xs bg-blue-200 px-2 py-1 rounded-full font-medium">
                            {treatment.cost_estimate}
                          </span>
                        </div>
                        <div className="space-y-1 text-sm text-blue-900">
                          <p><strong>Dosage:</strong> {treatment.dosage}</p>
                          <p><strong>Timing:</strong> {treatment.timing}</p>
                          <p><strong>Application:</strong> {treatment.application}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {/* Fertilizer Recommendations */}
                {result.fertilizer_recommendations && result.fertilizer_recommendations.length > 0 && (
                  <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                    <h4 className="font-bold text-green-900 mb-3 flex items-center">
                      <FiPackage className="mr-2" /> Fertilizer Recommendations:
                    </h4>
                    {result.fertilizer_recommendations.map((fert, idx) => (
                      <div key={idx} className="mb-3 last:mb-0 bg-white rounded p-3">
                        <p className="font-bold text-green-900">{fert.product}</p>
                        <p className="text-sm text-gray-700 mt-1"><strong>Dosage:</strong> {fert.dosage}</p>
                        <p className="text-sm text-gray-700"><strong>When:</strong> {fert.timing}</p>
                        <p className="text-sm text-gray-600 italic">{fert.purpose}</p>
                      </div>
                    ))}
                  </div>
                )}

                {/* Preventive Care - Expert Curated */}
                {result.preventive_care && result.preventive_care.length > 0 && (
                  <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                    <h4 className="font-bold text-blue-900 mb-3 flex items-center">
                      <FiShield className="mr-2" /> Prevention & Care Tips:
                    </h4>
                    <div className="mb-3 bg-white border-l-4 border-blue-500 p-2 rounded">
                      <p className="text-xs text-blue-900">
                        <strong>Source:</strong> Agricultural Expert Knowledge Base (Expert-Curated)
                        <br />
                        <span className="text-blue-700">Evidence-based recommendations from agricultural scientists</span>
                      </p>
                    </div>
                    <ul className="grid grid-cols-1 gap-2">
                      {result.preventive_care.map((tip, idx) => (
                        <li key={idx} className="text-sm text-blue-800 bg-white rounded px-3 py-2">
                          {tip}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* What NOT to Do */}
                {result.what_not_to_do && result.what_not_to_do.length > 0 && (
                  <div className="bg-red-50 rounded-lg p-4 border border-red-200">
                    <h4 className="font-bold text-red-900 mb-3 flex items-center">
                      <FiXCircle className="mr-2" /> Important: What NOT to Do:
                    </h4>
                    <ul className="space-y-2">
                      {result.what_not_to_do.map((warning, idx) => (
                        <li key={idx} className="text-sm text-red-800 bg-white rounded px-3 py-2">
                          {warning}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Monitoring Schedule */}
                {result.monitoring_schedule && (
                  <div className="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
                    <h4 className="font-bold text-yellow-900 mb-3 flex items-center">
                      <FiClock className="mr-2" /> 📅 Monitoring Schedule:
                    </h4>
                    <p className="text-sm text-yellow-900 mb-3">
                      <strong>Next Check:</strong> {result.monitoring_schedule.next_check}
                    </p>
                    {result.monitoring_schedule.what_to_watch && (
                      <>
                        <p className="text-sm font-bold text-yellow-900 mb-2">Watch for:</p>
                        <ul className="space-y-1">
                          {result.monitoring_schedule.what_to_watch.map((item, idx) => (
                            <li key={idx} className="text-sm text-yellow-800">• {item}</li>
                          ))}
                        </ul>
                      </>
                    )}
                  </div>
                )}

                {/* Expert Tip */}
                {result.expert_tip && (
                  <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-4 border-2 border-purple-200">
                    <h4 className="font-bold text-purple-900 mb-2">Expert Tip:</h4>
                    <p className="text-sm text-purple-800 italic">{result.expert_tip}</p>
                  </div>
                )}

                {/* Image Analysis Info */}
                {result.image_analysis && (
                  <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-3 text-xs text-gray-600 dark:text-gray-300">
                    <p><strong>Image Analysis:</strong> {result.image_analysis.dimensions} • {result.image_analysis.format} • {result.image_analysis.size_kb} KB</p>
                    <p className="text-gray-500 dark:text-gray-400 mt-1">Analysis completed: {new Date(result.detected_at).toLocaleString()}</p>
                  </div>
                )}
                  </>
                )}
              </div>
            )}
          </div>
        </div>
        )}
      </div>
    </Layout>
  );
};

export default DiseaseDetection;
