import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { FiList, FiClock, FiArrowLeft, FiGrid, FiColumns, FiDownload, FiShare2, FiTrash2 } from 'react-icons/fi';
import Layout from '../components/common/Layout';
import Loader from '../components/common/Loader';
import Timeline from '../components/common/Timeline';
import GalleryView from '../components/common/GalleryView';
import FilterSort from '../components/common/FilterSort';
import ComparisonView from '../components/common/ComparisonView';
import ShareModal from '../components/common/ShareModal';
import EnhancedExport from '../components/common/EnhancedExport';
import Pagination from '../components/common/Pagination';
import FavoriteButton from '../components/common/FavoriteButton';
import { NoHistoryState } from '../components/common/EmptyState';
import { diseaseService } from '../services/apiService';
import { formatDateTime } from '../utils/helpers';
import { translateCropName, translateDiseaseName } from '../utils/translationHelpers';

const History = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [history, setHistory] = useState([]);
  const [viewMode, setViewMode] = useState('timeline'); // 'timeline', 'list', or 'gallery'
  const [filters, setFilters] = useState({
    cropType: 'all',
    severity: 'all',
    dateRange: 'all'
  });
  const [sortBy, setSortBy] = useState('newest');
  const [showComparison, setShowComparison] = useState(false);
  const [selectedForShare, setSelectedForShare] = useState(null);
  const [showExport, setShowExport] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 12;

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await diseaseService.getHistory(500); // Get more data for filtering
      setHistory(response.data || []);
    } catch (error) {
      toast.error('Failed to fetch detection history');
    } finally {
      setLoading(false);
    }
  };

  // Apply filters and sorting
  const getFilteredHistory = () => {
    let filtered = [...history];

    // Filter by crop type
    if (filters.cropType && filters.cropType !== 'all') {
      filtered = filtered.filter(item => item.crop_type === filters.cropType);
    }

    // Filter by severity
    if (filters.severity && filters.severity !== 'all') {
      filtered = filtered.filter(item => item.severity === filters.severity);
    }

    // Filter by date range
    if (filters.dateRange && filters.dateRange !== 'all') {
      const now = new Date();
      const filterDate = new Date();
      
      switch (filters.dateRange) {
        case 'today':
          filterDate.setHours(0, 0, 0, 0);
          break;
        case 'week':
          filterDate.setDate(now.getDate() - 7);
          break;
        case 'month':
          filterDate.setMonth(now.getMonth() - 1);
          break;
        case '3months':
          filterDate.setMonth(now.getMonth() - 3);
          break;
      }
      
      filtered = filtered.filter(item => new Date(item.detected_at) >= filterDate);
    }

    // Apply sorting
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'oldest':
          return new Date(a.detected_at) - new Date(b.detected_at);
        case 'confidence-high':
          return b.confidence - a.confidence;
        case 'confidence-low':
          return a.confidence - b.confidence;
        case 'severity':
          const severityOrder = { high: 3, moderate: 2, low: 1, none: 0 };
          return (severityOrder[b.severity] || 0) - (severityOrder[a.severity] || 0);
        case 'newest':
        default:
          return new Date(b.detected_at) - new Date(a.detected_at);
      }
    });

    return filtered;
  };

  const filteredHistory = getFilteredHistory();
  
  // Paginate
  const totalPages = Math.ceil(filteredHistory.length / itemsPerPage);
  const paginatedHistory = filteredHistory.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const handleDelete = async (detectionId) => {
    if (!window.confirm('Are you sure you want to delete this detection?')) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/v1/disease/history/${detectionId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      const data = await response.json();

      if (data.success) {
        toast.success('Detection deleted successfully');
        // Remove from local state
        setHistory(history.filter(h => h.id !== detectionId));
      } else {
        toast.error(data.message || 'Failed to delete detection');
      }
    } catch (error) {
      toast.error('Failed to delete detection');
    }
  };

  if (loading) {
    return (
      <Layout>
        <Loader />
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-6 animate-fadeIn">
        {/* Modals */}
        {showComparison && (
          <ComparisonView 
            detections={filteredHistory} 
            onClose={() => setShowComparison(false)} 
          />
        )}
        {selectedForShare && (
          <ShareModal 
            isOpen={true} 
            onClose={() => setSelectedForShare(null)} 
            detection={selectedForShare} 
          />
        )}
        {showExport && (
          <EnhancedExport 
            isOpen={true} 
            onClose={() => setShowExport(false)} 
            data={filteredHistory}
            filename="agrismart-detection-history"
          />
        )}

        {/* Back Button */}
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors group"
        >
          <FiArrowLeft className="group-hover:-translate-x-1 transition-transform" />
          <span className="font-medium">{t('back_to_dashboard')}</span>
        </button>

        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              {t('history')}
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              {filteredHistory.length} detection{filteredHistory.length !== 1 ? 's' : ''} found
            </p>
          </div>
          
          {/* Action Buttons */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowComparison(true)}
              disabled={filteredHistory.length < 2}
              className={`px-4 py-2 rounded-lg transition-colors flex items-center gap-2 font-medium ${
                filteredHistory.length < 2 
                  ? 'bg-gray-100 dark:bg-gray-700 text-gray-400 cursor-not-allowed'
                  : 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 hover:bg-blue-200 dark:hover:bg-blue-900/50'
              }`}
            >
              <FiColumns />
              Compare
            </button>
            <button
              onClick={() => setShowExport(true)}
              disabled={filteredHistory.length === 0}
              className={`px-4 py-2 rounded-lg transition-colors flex items-center gap-2 font-medium ${
                filteredHistory.length === 0 
                  ? 'bg-gray-100 dark:bg-gray-700 text-gray-400 cursor-not-allowed'
                  : 'bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 hover:bg-purple-200 dark:hover:bg-purple-900/50'
              }`}
            >
              <FiDownload />
              Export
            </button>
          </div>
        </div>

        {/* Filter & Sort */}
        {history.length > 0 && (
          <FilterSort 
            onFilterChange={(newFilters) => {
              setFilters(newFilters);
              setCurrentPage(1); // Reset to first page when filters change
            }} 
            onSortChange={(newSort) => {
              setSortBy(newSort);
              setCurrentPage(1); // Reset to first page when sort changes
            }} 
          />
        )}

        {/* View Toggle */}
        {history.length > 0 && (
          <div className="flex items-center justify-center glass-card p-1 w-fit mx-auto">
            <button
              onClick={() => setViewMode('timeline')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                viewMode === 'timeline'
                  ? 'bg-primary-500 text-white shadow-md'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
              }`}
            >
              <FiClock className="inline mr-2" />
              Timeline
            </button>
            <button
              onClick={() => setViewMode('gallery')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                viewMode === 'gallery'
                  ? 'bg-primary-500 text-white shadow-md'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
              }`}
            >
              <FiGrid className="inline mr-2" />
              Gallery
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                viewMode === 'list'
                  ? 'bg-primary-500 text-white shadow-md'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
              }`}
            >
              <FiList className="inline mr-2" />
              List
            </button>
          </div>
        )}

        {filteredHistory.length === 0 ? (
          <NoHistoryState t={t} />
        ) : (
          <div>
            {/* Render views based on mode */}
            {viewMode === 'timeline' && <Timeline items={paginatedHistory} />}
            
            {viewMode === 'gallery' && (
              <GalleryView 
                detections={paginatedHistory}
                onImageClick={(detection) => setSelectedForShare(detection)}
              />
            )}
            
            {viewMode === 'list' && (
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {paginatedHistory.map((detection) => (
                  <div key={detection.id} className="card hover:shadow-lg transition relative">
                    {/* Favorite Button */}
                    <div className="absolute top-4 right-4 z-10">
                      <FavoriteButton detectionId={detection.id} />
                    </div>

                    <img
                      src={`http://localhost:8000${detection.image_url}`}
                      alt={t('detected_crop')}
                      className="w-full h-48 object-cover rounded-lg mb-4"
                      onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextElementSibling.style.display = 'flex';
                      }}
                    />
                    <div 
                      className="w-full h-48 bg-gray-100 dark:bg-gray-700 rounded-lg mb-4 items-center justify-center text-gray-400 hidden"
                      style={{ display: 'none' }}
                    >
                      <div className="text-center">
                        <span className="text-4xl mb-2 block">🖼️</span>
                        <span className="text-sm">{t('image_not_available')}</span>
                      </div>
                    </div>

                    <h3 className="font-semibold text-lg mb-2 text-gray-800 dark:text-white">
                      {detection.disease_detected}
                    </h3>

                    {detection.crop_type && (
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-1 capitalize">
                        {t('crop_label')}: {translateCropName(detection.crop_type, t)}
                      </p>
                    )}

                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm text-gray-600 dark:text-gray-400">{t('confidence')}:</span>
                      <span className="font-semibold text-primary-600 dark:text-primary-400">
                        {detection.confidence >= 1 
                          ? detection.confidence.toFixed(1)
                          : (detection.confidence * 100).toFixed(1)}%
                      </span>
                    </div>

                    <div className="flex items-center justify-between mb-3">
                      <span className="text-sm text-gray-600 dark:text-gray-400">{t('severity')}:</span>
                      <span
                        className={`px-2 py-1 rounded text-xs font-semibold ${
                          detection.severity === 'high'
                            ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                            : detection.severity === 'moderate'
                            ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
                            : detection.severity === 'low'
                            ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400'
                            : 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                        }`}
                      >
                        {detection.severity === 'high' ? t('severity_high') :
                         detection.severity === 'moderate' ? t('severity_medium') :
                         detection.severity === 'low' ? t('severity_low') :
                         t('severity_none')}
                      </span>
                    </div>

                    <p className="text-xs text-gray-500 dark:text-gray-400 border-t dark:border-gray-700 pt-2 mb-3">
                      {formatDateTime(detection.detected_at)}
                    </p>

                    <div className="flex gap-2">
                      <button
                        onClick={() => setSelectedForShare(detection)}
                        className="flex-1 bg-primary-50 dark:bg-primary-900/30 hover:bg-primary-100 dark:hover:bg-primary-900/50 text-primary-600 dark:text-primary-400 font-semibold py-2 px-4 rounded-lg transition flex items-center justify-center gap-2"
                      >
                        <FiShare2 />
                        Share
                      </button>
                      <button
                        onClick={() => handleDelete(detection.id)}
                        className="flex-1 bg-red-50 dark:bg-red-900/30 hover:bg-red-100 dark:hover:bg-red-900/50 text-red-600 dark:text-red-400 font-semibold py-2 px-4 rounded-lg transition flex items-center justify-center gap-2"
                      >
                        <FiTrash2 />
                        {t('delete')}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="mt-8">
                <Pagination 
                  currentPage={currentPage}
                  totalPages={totalPages}
                  onPageChange={setCurrentPage}
                  itemsPerPage={itemsPerPage}
                  totalItems={filteredHistory.length}
                />
              </div>
            )}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default History;
