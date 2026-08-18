// Batch Upload Component for Disease Detection
// Allows uploading multiple images at once
// Shows individual progress for each image

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { FiUploadCloud, FiX, FiCheckCircle, FiAlertCircle } from 'react-icons/fi';
import { toast } from 'react-toastify';
import { diseaseService } from '../../services/apiService';

const BatchUpload = ({ onBatchComplete, maxFiles = 5, cropType = 'tomato' }) => {
  const [uploadQueue, setUploadQueue] = useState([]);

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    if (acceptedFiles.length + uploadQueue.length > maxFiles) {
      toast.warning(`Maximum ${maxFiles} images allowed`);
      return;
    }

    // Add files to queue with initial state
    const newFiles = acceptedFiles.map((file, index) => ({
      id: Date.now() + index,
      file,
      preview: URL.createObjectURL(file),
      status: 'pending', // pending, uploading, success, error
      progress: 0,
      result: null
    }));

    setUploadQueue(prev => [...prev, ...newFiles]);

    // Handle rejected files
    if (rejectedFiles.length > 0) {
      toast.error(`${rejectedFiles.length} file(s) rejected. Check file type and size.`);
    }
  }, [uploadQueue, maxFiles]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    maxSize: 10485760, // 10MB
    multiple: true
  });

  const removeFile = (id) => {
    setUploadQueue(prev => prev.filter(item => item.id !== id));
  };

  const processUploads = async () => {
    // Process each image with REAL AI detection
    for (let i = 0; i < uploadQueue.length; i++) {
      const item = uploadQueue[i];
      
      if (item.status !== 'pending') continue;

      try {
        // Update to uploading
        setUploadQueue(prev => prev.map(f => 
          f.id === item.id ? { ...f, status: 'uploading', progress: 0 } : f
        ));

        // Progress updates
        setUploadQueue(prev => prev.map(f => 
          f.id === item.id ? { ...f, progress: 30 } : f
        ));

        // REAL API CALL - Disease Detection
        const response = await diseaseService.detectDisease(item.file, cropType);

        setUploadQueue(prev => prev.map(f => 
          f.id === item.id ? { ...f, progress: 100 } : f
        ));

        // Extract data from nested response
        const data = response.data || response;
        
        // Update with real results
        setUploadQueue(prev => prev.map(f => 
          f.id === item.id ? { 
            ...f, 
            status: 'success',
            result: {
              disease: data.disease || 'Unknown',
              confidence: Math.round(data.confidence || 0),  // Already percentage
              severity: data.severity_level || 'N/A'
            }
          } : f
        ));

        toast.success(`${item.file.name} analyzed successfully!`);

      } catch (error) {
        console.error(`Error processing ${item.file.name}:`, error);
        setUploadQueue(prev => prev.map(f => 
          f.id === item.id ? { 
            ...f, 
            status: 'error',
            result: {
              error: error.message || 'Detection failed'
            }
          } : f
        ));
        toast.error(`Failed: ${item.file.name}`);
      }

      // Small delay between requests
      await new Promise(resolve => setTimeout(resolve, 500));
    }

    toast.success('Batch detection complete!');
    onBatchComplete?.(uploadQueue);
  };

  const clearAll = () => {
    uploadQueue.forEach(item => {
      URL.revokeObjectURL(item.preview);
    });
    setUploadQueue([]);
  };

  return (
    <div className="space-y-4">
      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 cursor-pointer
          ${isDragActive 
            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' 
            : 'border-gray-300 dark:border-gray-600 hover:border-primary-400 dark:hover:border-primary-500'
          }`}
      >
        <input {...getInputProps()} />
        <FiUploadCloud className="mx-auto text-5xl text-gray-400 mb-3" />
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
          {isDragActive ? 'Drop images here' : 'Batch Upload Images'}
        </h3>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          Drop up to {maxFiles} images or click to select<br />
          <span className="text-xs">JPG, PNG • Max 10MB each</span>
        </p>
      </div>

      {/* Upload Queue */}
      {uploadQueue.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="font-semibold text-gray-900 dark:text-white">
              Queued Images ({uploadQueue.length}/{maxFiles})
            </h4>
            <div className="flex gap-2">
              {uploadQueue.some(item => item.status === 'pending') && (
                <button
                  onClick={processUploads}
                  disabled={uploadQueue.some(item => item.status === 'uploading')}
                  className="btn-primary-pro text-sm px-4 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                   Process All ({uploadQueue.filter(item => item.status === 'pending').length})
                </button>
              )}
              <button
                onClick={clearAll}
                className="text-sm text-gray-500 hover:text-red-600 transition-colors font-medium"
              >
                Clear All
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-3">
            {uploadQueue.map((item) => (
              <div key={item.id} className="glass-card p-4 flex items-center gap-4">
                {/* Image Preview */}
                <img
                  src={item.preview}
                  alt="Preview"
                  className="w-20 h-20 object-cover rounded-lg border-2 border-gray-200 dark:border-gray-700"
                />

                {/* Info */}
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-gray-900 dark:text-white truncate">
                    {item.file.name}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    {(item.file.size / 1024 / 1024).toFixed(2)} MB
                  </p>

                  {/* Progress Bar */}
                  {item.status === 'uploading' && (
                    <div className="mt-2">
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 overflow-hidden">
                        <div
                          className="h-full bg-primary-600 transition-all duration-300"
                          style={{ width: `${item.progress}%` }}
                        />
                      </div>
                      <p className="text-xs text-gray-500 mt-1">{item.progress}%</p>
                    </div>
                  )}

                  {/* Result */}
                  {item.status === 'success' && item.result && (
                    <div className="mt-2 flex items-center gap-2 text-sm">
                      <span className="text-green-600 dark:text-green-400 font-medium">
                        {item.result.disease}
                      </span>
                      <span className="text-gray-500">•</span>
                      <span className="text-gray-600 dark:text-gray-400">
                        {item.result.confidence}% confidence
                      </span>
                    </div>
                  )}

                  {/* Error */}
                  {item.status === 'error' && item.result && (
                    <div className="mt-2 text-sm text-red-600 dark:text-red-400">
                      Error: {item.result.error}
                    </div>
                  )}
                </div>

                {/* Status Icon */}
                <div className="flex-shrink-0">
                  {item.status === 'pending' && (
                    <button
                      onClick={() => removeFile(item.id)}
                      className="p-2 hover:bg-red-100 dark:hover:bg-red-900/30 rounded-full transition-colors"
                    >
                      <FiX className="text-red-600" />
                    </button>
                  )}
                  {item.status === 'uploading' && (
                    <div className="animate-spin text-primary-600">⏳</div>
                  )}
                  {item.status === 'success' && (
                    <FiCheckCircle className="text-green-600 text-2xl" />
                  )}
                  {item.status === 'error' && (
                    <FiAlertCircle className="text-red-600 text-2xl" />
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default BatchUpload;
