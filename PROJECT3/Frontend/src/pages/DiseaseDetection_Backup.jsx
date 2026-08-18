import { useState, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { useDropzone } from 'react-dropzone';
import { toast } from 'react-toastify';
import { FiUpload } from 'react-icons/fi';
import Layout from '../components/common/Layout';
import Loader from '../components/common/Loader';
import { diseaseService } from '../services/apiService';
import { CROP_TYPES, MAX_FILE_SIZE, ALLOWED_IMAGE_TYPES } from '../utils/constants';

const DiseaseDetection = () => {
  const { t } = useTranslation();
  const [loading, setLoading] = useState(false);
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

    try {
      const response = await diseaseService.detectDisease(selectedFile, cropType);
      setResult(response.data || response);
      toast.success('Disease detected successfully!');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Detection failed');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreview(null);
    setResult(null);
  };

  return (
    <Layout>
      <div className="max-w-4xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold">{t('disease_detection')}</h1>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Upload Section */}
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">{t('upload_image')}</h2>

            {!preview ? (
              <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition ${
                  isDragActive
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-300 hover:border-primary-500'
                }`}
              >
                <input {...getInputProps()} />
                <FiUpload className="mx-auto text-4xl text-gray-400 mb-4" />
                <p className="text-gray-600">
                  {isDragActive
                    ? 'Drop the image here'
                    : 'Drag & drop an image, or click to select'}
                </p>
                <p className="text-sm text-gray-500 mt-2">
                  Max file size: 10MB (JPG, JPEG, PNG)
                </p>
              </div>
            ) : (
              <div>
                <img
                  src={preview}
                  alt="Preview"
                  className="w-full h-64 object-cover rounded-lg mb-4"
                />
                <button onClick={handleReset} className="btn-secondary w-full">
                  Change Image
                </button>
              </div>
            )}

            <div className="mt-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {t('crop_type')}
              </label>
              <select
                value={cropType}
                onChange={(e) => setCropType(e.target.value)}
                className="input-field"
              >
                {CROP_TYPES.map((crop) => (
                  <option key={crop} value={crop} className="capitalize">
                    {crop}
                  </option>
                ))}
              </select>
            </div>

            <button
              onClick={handleDetect}
              disabled={!selectedFile || loading}
              className="btn-primary w-full mt-4"
            >
              {loading ? t('loading') : t('detect_disease')}
            </button>
          </div>

          {/* Results Section */}
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Detection Results</h2>

            {loading ? (
              <Loader />
            ) : result ? (
              <div className="space-y-4">
                <div>
                  <h3 className="font-semibold text-lg mb-1">Disease:</h3>
                  <p className="text-gray-700">{result.disease}</p>
                </div>

                <div>
                  <h3 className="font-semibold text-lg mb-1">{t('confidence')}:</h3>
                  <div className="flex items-center space-x-2">
                    <div className="flex-grow bg-gray-200 rounded-full h-4">
                      <div
                        className="bg-primary-600 h-4 rounded-full"
                        style={{ width: `${result.confidence}%` }}
                      />
                    </div>
                    <span className="font-semibold">{result.confidence}%</span>
                  </div>
                </div>

                <div>
                  <h3 className="font-semibold text-lg mb-1">{t('severity')}:</h3>
                  <span
                    className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${
                      result.severity === 'high'
                        ? 'bg-red-100 text-red-800'
                        : result.severity === 'medium'
                        ? 'bg-yellow-100 text-yellow-800'
                        : result.severity === 'low'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-blue-100 text-blue-800'
                    }`}
                  >
                    {result.severity.toUpperCase()}
                  </span>
                </div>

                <div>
                  <h3 className="font-semibold text-lg mb-2">{t('recommendations')}:</h3>
                  <div className="space-y-2">
                    {result.recommendations.map((rec, index) => (
                      <div
                        key={index}
                        className="bg-gray-50 p-3 rounded-lg border border-gray-200"
                      >
                        <span className="font-semibold text-primary-600 capitalize">
                          {rec.type}:
                        </span>{' '}
                        {rec.treatment}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-gray-500 text-center py-12">
                Upload an image and click detect to see results
              </p>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default DiseaseDetection;
