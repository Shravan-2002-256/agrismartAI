import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import Layout from '../components/common/Layout';
import { 
  FiTrendingUp, 
  FiAlertTriangle, 
  FiCheckCircle, 
  FiInfo,
  FiChevronDown,
  FiChevronUp,
  FiDroplet,
  FiPackage,
  FiArrowLeft,
  FiShield,
  FiBarChart2
} from 'react-icons/fi';
import api from '../services/api';
import { translateCropName, translateDiseaseName } from '../utils/translationHelpers';

const Insights = () => {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [days, setDays] = useState(7);
  const [expandedCrops, setExpandedCrops] = useState({});

  useEffect(() => {
    fetchInsights();
  }, [days, i18n.language]);

  const fetchInsights = async () => {
    setLoading(true);
    try {
      const response = await api.get(`/insights/weekly?days=${days}&user_only=true&language=${i18n.language}`);
      if (response.data.success) {
        setInsights(response.data.data);
      } else {
        toast.error('Failed to load insights');
      }
    } catch (error) {
      console.error('Error fetching insights:', error);
      toast.error('Failed to load insights');
    } finally {
      setLoading(false);
    }
  };

  const toggleCropExpansion = (cropType) => {
    setExpandedCrops(prev => ({
      ...prev,
      [cropType]: !prev[cropType]
    }));
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'bg-red-100 text-red-800 border-red-300';
      case 'high': return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'moderate': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'low': return 'bg-green-100 text-green-800 border-green-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical':
      case 'high':
        return <FiAlertTriangle className="text-red-600" size={24} />;
      case 'moderate':
        return <FiInfo className="text-yellow-600" size={24} />;
      case 'low':
        return <FiCheckCircle className="text-green-600" size={24} />;
      default:
        return <FiInfo className="text-gray-600" size={24} />;
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-screen">
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Analyzing your data...</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (!insights || insights.total_detections === 0) {
    return (
      <Layout>
        <div className="max-w-7xl mx-auto">
          <div className="text-center py-12">
            <FiTrendingUp size={64} className="mx-auto text-gray-400 mb-4" />
            <h2 className="text-2xl font-bold text-gray-700 mb-2">{t('no_data_available')}</h2>
            <p className="text-gray-600 mb-6">
              Upload crop images to get weekly insights and disease pattern analysis.
            </p>
            <a href="/disease-detection" className="btn-primary">
              Upload Images
            </a>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-7xl mx-auto">
        {/* Back Button */}
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors group mb-4"
        >
          <FiArrowLeft className="group-hover:-translate-x-1 transition-transform" />
          <span className="font-medium">{t('back_to_dashboard')}</span>
        </button>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 flex items-center space-x-3">
                <FiTrendingUp className="text-primary-600" />
                <span>{t('weekly_insights_analytics')}</span>
              </h1>
              <p className="text-gray-600 mt-2">
                {insights.period} • {insights.total_detections} {t('detections_analyzed')}
              </p>
            </div>

            {/* Days Filter */}
            <div className="flex items-center space-x-2">
              <label className="text-sm text-gray-600">{t('period')}:</label>
              <select
                value={days}
                onChange={(e) => setDays(parseInt(e.target.value))}
                className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value={7}>{t('last_7_days')}</option>
                <option value={14}>{t('last_14_days')}</option>
                <option value={30}>{t('last_30_days')}</option>
                <option value={90}>{t('last_90_days')}</option>
              </select>
            </div>
          </div>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-primary-600">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">{t('total_uploads')}</p>
                <p className="text-3xl font-bold text-gray-900">{insights.total_detections}</p>
              </div>
              <FiTrendingUp size={40} className="text-primary-600" />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-600">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">{t('crop_types')}</p>
                <p className="text-3xl font-bold text-gray-900">{insights.total_crops}</p>
              </div>
              <FiPackage size={40} className="text-blue-600" />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-600">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">{t('health_status')}</p>
                <p className="text-lg font-bold text-gray-900">{insights.summary}</p>
              </div>
              <FiCheckCircle size={40} className="text-green-600" />
            </div>
          </div>
        </div>

        {/* Insights by Crop */}
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">{t('crop_wise_insights')}</h2>

          {insights.insights.map((cropInsight, index) => (
            <div key={index} className="bg-white rounded-lg shadow-lg border-2 border-gray-200 overflow-hidden">
              {/* Crop Header */}
              <div className={`p-6 ${getSeverityColor(cropInsight.severity)} border-b-2`}>
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-4 flex-1">
                    {getSeverityIcon(cropInsight.severity)}
                    <div className="flex-1">
                      <h3 className="text-2xl font-bold mb-2">
                        {cropInsight.crop_type.charAt(0).toUpperCase() + cropInsight.crop_type.slice(1)}
                      </h3>
                      <p className="text-sm font-medium mb-2">
                        {cropInsight.urgency === 'Keep monitoring' ? t('keep_monitoring') :
                         cropInsight.urgency === 'Action needed soon' ? t('action_needed_soon') :
                         cropInsight.urgency === 'Immediate action required' ? t('immediate_action_required') :
                         cropInsight.urgency}
                      </p>
                      <p className="text-base">{cropInsight.pattern_description}</p>
                    </div>
                  </div>
                  
                  <button
                    onClick={() => toggleCropExpansion(cropInsight.crop_type)}
                    className="ml-4 p-2 hover:bg-white/50 rounded-lg transition"
                  >
                    {expandedCrops[cropInsight.crop_type] ? (
                      <FiChevronUp size={24} />
                    ) : (
                      <FiChevronDown size={24} />
                    )}
                  </button>
                </div>

                {/* Quick Stats */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                  <div className="bg-white/80 rounded-lg p-3">
                    <p className="text-xs text-gray-600">{t('total_uploads')}</p>
                    <p className="text-xl font-bold">{cropInsight.total_uploads}</p>
                  </div>
                  <div className="bg-white/80 rounded-lg p-3">
                    <p className="text-xs text-gray-600">{t('diseased')}</p>
                    <p className="text-xl font-bold text-red-600">{cropInsight.diseased_count}</p>
                  </div>
                  <div className="bg-white/80 rounded-lg p-3">
                    <p className="text-xs text-gray-600">{t('disease_rate')}</p>
                    <p className="text-xl font-bold">{cropInsight.disease_rate}%</p>
                  </div>
                  <div className="bg-white/80 rounded-lg p-3">
                    <p className="text-xs text-gray-600">{t('primary_disease')}</p>
                    <p className="text-sm font-bold">{cropInsight.primary_disease.display_name}</p>
                  </div>
                </div>
              </div>

              {/* Expanded Details */}
              {expandedCrops[cropInsight.crop_type] && (
                <div className="p-6 bg-gray-50">
                  {/* Primary Disease Info */}
                  <div className="mb-6">
                    <h4 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
                      <FiAlertTriangle className="text-orange-600 mr-2" />
                      {t('primary_disease_label')} {translateDiseaseName(cropInsight.primary_disease.display_name, t)}
                    </h4>
                    <div className="bg-white rounded-lg p-4 border border-gray-200">
                      <p className="text-gray-700">
                        {t('detected_in_images', { count: cropInsight.primary_disease.count, percentage: cropInsight.primary_disease.percentage })}
                      </p>
                    </div>
                  </div>

                  {/* Causes */}
                  {cropInsight.causes && cropInsight.causes.length > 0 && (
                    <div className="mb-6">
                      <h4 className="text-lg font-bold text-gray-900 mb-3">
                        🔍 {t('common_causes')}
                      </h4>
                      <div className="bg-white rounded-lg p-4 border border-gray-200">
                        <ul className="list-disc list-inside space-y-2">
                          {cropInsight.causes.map((cause, idx) => (
                            <li key={idx} className="text-gray-700">{cause}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}

                  {/* Remedies */}
                  {cropInsight.remedies && cropInsight.remedies.length > 0 && (
                    <div className="mb-6">
                      <h4 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
                        <FiDroplet className="text-blue-600 mr-2" />
                        {t('treatment_remedies')}
                      </h4>
                      <div className="bg-white rounded-lg p-4 border border-green-200">
                        <ol className="list-decimal list-inside space-y-3">
                          {cropInsight.remedies.map((remedy, idx) => (
                            <li key={idx} className="text-gray-700 font-medium">{remedy}</li>
                          ))}
                        </ol>
                      </div>
                    </div>
                  )}

                  {/* Fertilizer Recommendations */}
                  {cropInsight.fertilizer_recommendations && cropInsight.fertilizer_recommendations.length > 0 && (
                    <div className="mb-6">
                      <h4 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
                        <FiPackage className="text-green-600 mr-2" />
                        {t('fertilizer_recommendations')}
                      </h4>
                      <div className="bg-white rounded-lg p-4 border border-blue-200">
                        <ul className="space-y-3">
                          {cropInsight.fertilizer_recommendations.map((fert, idx) => (
                            <li key={idx} className="flex items-start">
                              <span className="text-green-600 mr-2">✓</span>
                              <span className="text-gray-700">{fert}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}

                  {/* Prevention Tips */}
                  {cropInsight.prevention_tips && cropInsight.prevention_tips.length > 0 && (
                    <div className="mb-6">
                      <h4 className="text-lg font-bold text-gray-900 mb-3 flex items-center gap-2">
                        <FiShield className="text-yellow-600" /> {t('prevention_tips_label')}
                      </h4>
                      <div className="bg-white rounded-lg p-4 border border-yellow-200">
                        <ul className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {cropInsight.prevention_tips.map((tip, idx) => (
                            <li key={idx} className="flex items-start">
                              <span className="text-yellow-600 mr-2">•</span>
                              <span className="text-gray-700 text-sm">{tip}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}

                  {/* Other Diseases */}
                  {cropInsight.other_diseases && cropInsight.other_diseases.length > 0 && (
                    <div>
                      <h4 className="text-lg font-bold text-gray-900 mb-3">
                        📊 {t('other_diseases_detected')}
                      </h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {cropInsight.other_diseases.map((disease, idx) => (
                          <div key={idx} className="bg-white rounded-lg p-4 border border-gray-200">
                            <p className="font-semibold text-gray-900">{translateDiseaseName(disease.name, t)}</p>
                            <p className="text-sm text-gray-600">
                              {t('images_count', { count: disease.count, percentage: disease.percentage })}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Crop Breakdown */}
        {insights.crop_breakdown && insights.crop_breakdown.length > 0 && (
          <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <FiBarChart2 className="text-primary-600" /> {t('crop_distribution')}
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="bg-gray-100 border-b-2 border-gray-300">
                    <th className="px-4 py-3 text-left">{t('crop_type_header')}</th>
                    <th className="px-4 py-3 text-center">{t('total_uploads')}</th>
                    <th className="px-4 py-3 text-center">{t('healthy')}</th>
                    <th className="px-4 py-3 text-center">{t('diseased')}</th>
                    <th className="px-4 py-3 text-center">{t('disease_rate')}</th>
                  </tr>
                </thead>
                <tbody>
                  {insights.crop_breakdown.map((crop, idx) => (
                    <tr key={idx} className="border-b border-gray-200 hover:bg-gray-50">
                      <td className="px-4 py-3 font-semibold">
                        {translateCropName(crop.crop_type, t)}
                      </td>
                      <td className="px-4 py-3 text-center">{crop.total_uploads}</td>
                      <td className="px-4 py-3 text-center text-green-600 font-bold">
                        {crop.healthy_count}
                      </td>
                      <td className="px-4 py-3 text-center text-red-600 font-bold">
                        {crop.diseased_count}
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className={`px-3 py-1 rounded-full text-sm font-bold ${
                          crop.disease_rate >= 70 ? 'bg-red-100 text-red-800' :
                          crop.disease_rate >= 40 ? 'bg-orange-100 text-orange-800' :
                          crop.disease_rate >= 20 ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {crop.disease_rate}%
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default Insights;
