import { useState, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
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
  FiEye
} from 'react-icons/fi';
import Layout from '../components/common/Layout';
import { diseaseService } from '../services/apiService';
import { CROP_TYPES, MAX_FILE_SIZE, ALLOWED_IMAGE_TYPES } from '../utils/constants';

const DiseaseDetection = () => {
  const { t } = useTranslation();
  const [loading, setLoading] = useState(false);
  const [progressStage, setProgressStage] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [cropType, setCropType] = useState('tomato');
  const [result, setResult] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    
    if (!file) return;

    if (file.size > MAX_FILE_SIZE) {
      toast.error('File size exceeds 10MB');
      return;
    }

    if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
      toast.error('Only JPG, JPEG, and PNG files are allowed');
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

  const handleDetect = async () => {
    if (!selectedFile) {
      toast.error('Please select an image first');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      // Stage 1: Uploading
      setProgressStage('Uploading image to server...');
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Stage 2: Analyzing
      setProgressStage('Analyzing image with AI model...');
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Stage 3: Detecting patterns
      setProgressStage('Detecting disease patterns...');
      
      const response = await diseaseService.detectDisease(selectedFile, cropType);
      
      // Stage 4: Generating recommendations
      setProgressStage('Generating comprehensive recommendations...');
      await new Promise(resolve => setTimeout(resolve, 300));
      
      setResult(response.data || response);
      toast.success('Analysis complete!');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Detection failed');
    } finally {
      setLoading(false);
      setProgressStage('');
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreview(null);
    setResult(null);
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
      <div className="max-w-7xl mx-auto space-y-6">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">{t('disease_detection')}</h1>
          <p className="text-gray-600">Upload a crop image for AI-powered disease analysis</p>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Upload Section */}
          <div className="card">
            <h2 className="text-2xl font-bold mb-6 flex items-center">
              <FiUpload className="mr-2 text-primary-600" />
              Upload Crop Image
            </h2>

            {!preview ? (
              <div
                {...getRootProps()}
                className={`border-3 border-dashed rounded-xl p-12 text-center cursor-pointer transition ${
                  isDragActive
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-300 hover:border-primary-500 hover:bg-gray-50'
                }`}
              >
                <input {...getInputProps()} />
                <FiUpload className="mx-auto text-6xl text-gray-400 mb-4" />
                <p className="text-lg text-gray-700 font-medium mb-2">
                  {isDragActive
                    ? 'Drop the image here'
                    : 'Drag & drop an image, or click to select'}
                </p>
                <p className="text-sm text-gray-500">
                  Supported: JPG, JPEG, PNG • Max size: 10MB
                </p>
                <p className="text-xs text-gray-400 mt-2">
                  For best results, capture clear, well-lit images of affected leaves
                </p>
              </div>
            ) : (
              <div>
                <div className="relative">
                  <img
                    src={preview}
                    alt="Preview"
                    className="w-full h-80 object-cover rounded-lg mb-4 border-2 border-gray-200"
                  />
                  <div className="absolute top-2 right-2 bg-white px-3 py-1 rounded-full shadow-md">
                    <span className="text-sm font-medium text-gray-700">Preview</span>
                  </div>
                </div>
                <button onClick={handleReset} className="btn-secondary w-full mb-4">
                  Change Image
                </button>
              </div>
            )}

            <div className="mt-6">
              <label className="block text-sm font-bold text-gray-700 mb-2">
                Select Crop Type:
              </label>
              <select
                value={cropType}
                onChange={(e) => setCropType(e.target.value)}
                className="input-field text-lg font-medium"
              >
                {CROP_TYPES.map((crop) => (
                  <option key={crop} value={crop} className="capitalize">
                    {crop.charAt(0).toUpperCase() + crop.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            <button
              onClick={handleDetect}
              disabled={!selectedFile || loading}
              className="btn-primary w-full mt-6 text-lg py-4"
            >
              {loading ? '🔍 Analyzing...' : 'Detect Disease'}
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
                  ⚡ Our AI model is analyzing {cropType} leaf patterns...
                </p>
              </div>
            )}
          </div>

          {/* Results Section */}
          <div className="card">
            <h2 className="text-2xl font-bold mb-6 flex items-center">
              <FiCheckCircle className="mr-2 text-green-600" />
              Analysis Results
            </h2>

            {!result && !loading && (
              <div className="text-center py-16 text-gray-400">
                <FiInfo size={64} className="mx-auto mb-4 opacity-50" />
                <p className="text-lg">Upload an image and click "Detect Disease" to see results</p>
              </div>
            )}

            {result && (
              <div className="space-y-6">
                {/* Main Result Card */}
                <div className={`rounded-xl p-6 border-2 ${getSeverityColor(result.severity_level)}`}>
                  <div className="flex items-start space-x-4">
                    {getSeverityIcon(result.severity_level)}
                    <div className="flex-1">
                      <h3 className="text-2xl font-bold mb-2">{result.disease}</h3>
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
                      <p className="text-lg font-bold">{result.severity}</p>
                    </div>
                  </div>
                </div>

                {/* Analysis Details */}
                {result.analysis_details && result.analysis_details.length > 0 && (
                  <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                    <h4 className="font-bold text-gray-900 mb-3 flex items-center">
                      <FiEye className="mr-2" /> What We Detected:
                    </h4>
                    <ul className="space-y-2">
                      {result.analysis_details.map((detail, idx) => (
                        <li key={idx} className="text-sm text-gray-700 flex items-start">
                          <span className="mr-2">{detail.startsWith('✓') ? '✓' : detail.startsWith('⚠️') ? '⚠️' : '•'}</span>
                          <span>{detail.replace(/^[✓⚠️•]\s*/, '')}</span>
                        </li>
                      ))}
                    </ul>
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
                      <FiDroplet className="mr-2" /> 💊 Treatment Plan:
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
                      <FiPackage className="mr-2" /> 🌱 Fertilizer Recommendations:
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

                {/* Preventive Care */}
                {result.preventive_care && result.preventive_care.length > 0 && (
                  <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                    <h4 className="font-bold text-blue-900 mb-3 flex items-center">
                      <FiShield className="mr-2" /> 🛡️ Prevention & Care Tips:
                    </h4>
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
                      <FiXCircle className="mr-2" /> ❌ Important: What NOT to Do:
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
                    <h4 className="font-bold text-purple-900 mb-2">💡 Expert Tip:</h4>
                    <p className="text-sm text-purple-800 italic">{result.expert_tip}</p>
                  </div>
                )}

                {/* Image Analysis Info */}
                {result.image_analysis && (
                  <div className="bg-gray-100 rounded-lg p-3 text-xs text-gray-600">
                    <p><strong>Image Analysis:</strong> {result.image_analysis.dimensions} • {result.image_analysis.format} • {result.image_analysis.size_kb} KB</p>
                    <p className="text-gray-500 mt-1">Analysis completed: {new Date(result.detected_at).toLocaleString()}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default DiseaseDetection;
