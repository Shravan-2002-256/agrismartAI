import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { FiCamera, FiCloud, FiTrendingUp, FiActivity, FiAward, FiZap } from 'react-icons/fi';
import { toast } from 'react-toastify';
import Layout from '../components/common/Layout';
import Loader from '../components/common/Loader';
import FarmHealthScore from '../components/dashboard/FarmHealthScore';
import ExportReportButton from '../components/common/ExportReportButton';
import ProgressBar from '../components/common/ProgressBar';
import SearchBar from '../components/common/SearchBar';
import MiniChart from '../components/common/MiniChart';
import Tooltip from '../components/common/Tooltip';
import { diseaseService, userService } from '../services/apiService';
import { translateCropName } from '../utils/translationHelpers';
import { useCountUp } from '../hooks/useCountUp';
import { featureDescriptions } from '../utils/featureDescriptions';

const Dashboard = () => {
  const { t } = useTranslation();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);
  const [recentDetections, setRecentDetections] = useState([]);
  const [crops, setCrops] = useState([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [statsData, historyData, cropsData] = await Promise.all([
        diseaseService.getStats(),
        diseaseService.getHistory(5),
        userService.getCrops(),
      ]);

      console.log('📊 Stats Data:', statsData);
      console.log('📊 Stats total_detections:', statsData?.data?.total_detections);
      
      setStats(statsData.data || {});
      setRecentDetections(historyData.data || []);
      setCrops(cropsData.data || []);
    } catch (error) {
      console.error('Dashboard fetch error:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    {
      icon: <FiCamera className="text-3xl" />,
      title: t('disease_detection'),
      description: t('detect_crop_diseases_desc'),
      link: '/disease-detection',
      gradient: 'from-green-500 to-emerald-600',
      tooltip: featureDescriptions.disease_detection
    },
    {
      icon: <FiCloud className="text-3xl" />,
      title: t('weather'),
      description: t('view_forecast_alerts_desc'),
      link: '/weather',
      gradient: 'from-blue-500 to-cyan-600',
      tooltip: featureDescriptions.weather
    },
    {
      icon: <FiTrendingUp className="text-3xl" />,
      title: t('market_prices'),
      description: t('check_prices_trends_desc'),
      link: '/market',
      gradient: 'from-purple-500 to-pink-600',
      tooltip: featureDescriptions.market
    },
  ];

  // Animated counters for impressive effect (use direct value for small numbers)
  const totalDetections = stats?.total_detections || 0;
  const healthyCrops = stats?.severity_distribution?.none || 0;
  const cropsCount = crops.length;

  if (loading) {
    return (
      <Layout>
        <Loader />
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-8 animate-fadeIn">
        {/* Header with welcome message */}
        <div className="flex items-center justify-between animate-fadeIn">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              {t('dashboard')}
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              {t('welcome_message')}
            </p>
          </div>
          <div className="hidden md:block">
            <div className="glass-card px-6 py-3">
              <div className="flex items-center gap-2 text-sm">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-gray-700 dark:text-gray-300">{t('all_systems_operational')}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Search Bar */}
        <div className="animate-fadeIn" style={{ animationDelay: '100ms' }}>
          <SearchBar placeholder={t('search_detections_insights')} />
        </div>

        {/* Enhanced Statistics Cards with Animated Counters */}
        <div className="grid md:grid-cols-3 gap-6 dashboard-stats">
          {/* Total Detections - with counter animation */}
          <div className="card-pro group hover:shadow-xl transition-all duration-300 bg-gradient-to-br from-green-50 to-emerald-50 dark:from-gray-800 dark:to-gray-800 border-l-4 border-l-green-500">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
                  {t('total_detections')}
                </p>
                <p className="text-4xl font-bold text-gray-900 dark:text-white mb-1">
                  {totalDetections}
                </p>
                {stats?.total_detections > 0 && (
                  <p className="text-sm text-gray-600 dark:text-gray-400 font-medium">
                    {t('total_disease_scans')}
                  </p>
                )}
              </div>
              <div className="p-4 bg-green-100 dark:bg-green-900/30 rounded-xl group-hover:scale-110 transition-transform duration-300">
                <FiActivity className="text-3xl text-green-600 dark:text-green-400" />
              </div>
            </div>
            <ProgressBar 
              value={stats?.total_detections || 0} 
              max={100} 
              variant="success"
              height="sm"
              showPercentage={false}
            />
          </div>

          {/* My Crops */}
          <div className="card-pro group hover:shadow-xl transition-all duration-300 bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-gray-800 dark:to-gray-800 border-l-4 border-l-blue-500">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
                  {t('my_crops')}
                </p>
                <p className="text-4xl font-bold text-gray-900 dark:text-white mb-1">
                  {cropsCount}
                </p>
                <p className="text-sm text-blue-600 dark:text-blue-400 font-medium">
                  {t('active_crops_monitored')}
                </p>
              </div>
              <div className="p-4 bg-blue-100 dark:bg-blue-900/30 rounded-xl group-hover:scale-110 transition-transform duration-300">
                <FiActivity className="text-3xl text-blue-600 dark:text-blue-400" />
              </div>
            </div>
            <ProgressBar 
              value={crops.length} 
              max={10} 
              variant="info"
              height="sm"
              showPercentage={false}
            />
          </div>

          {/* Healthy Crops */}
          <div className="card-pro group hover:shadow-xl transition-all duration-300 bg-gradient-to-br from-purple-50 to-pink-50 dark:from-gray-800 dark:to-gray-800 border-l-4 border-l-purple-500">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
                  {t('healthy_crops')}
                </p>
                <p className="text-4xl font-bold text-gray-900 dark:text-white mb-1">
                  {healthyCrops}
                </p>
                <p className="text-sm text-purple-600 dark:text-purple-400 font-medium">
                  {t('no_issues_detected')}
                </p>
              </div>
              <div className="p-4 bg-purple-100 dark:bg-purple-900/30 rounded-xl group-hover:scale-110 transition-transform duration-300">
                <FiAward className="text-3xl text-purple-600 dark:text-purple-400" />
              </div>
            </div>
            <ProgressBar 
              value={stats?.severity_distribution?.none || 0} 
              max={stats?.total_detections || 1} 
              variant="success"
              height="sm"
              showPercentage={false}
            />
          </div>
        </div>

        {/* Farm Health Score & Export */}
        <div className="grid md:grid-cols-2 gap-6">
          <FarmHealthScore />
          
          <div className="card">
            <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100 mb-4">{t('export_reports')}</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
              {t('download_comprehensive')}
            </p>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div>
                  <h4 className="font-semibold text-gray-800 dark:text-gray-100">{t('disease_report')}</h4>
                  <p className="text-xs text-gray-600 dark:text-gray-400">{t('detection_history_analytics')}</p>
                </div>
                <ExportReportButton reportType="disease" />
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div>
                  <h4 className="font-semibold text-gray-800 dark:text-gray-100">{t('farm_health_report')}</h4>
                  <p className="text-xs text-gray-600 dark:text-gray-400">{t('overall_health_recommendations')}</p>
                </div>
                <ExportReportButton reportType="farm-health" />
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions - Enhanced with gradients and animations */}
        <div className="animate-slideInLeft">
          <div className="flex items-center gap-3 mb-6">
            <FiZap className="text-3xl text-primary-600 dark:text-primary-400" />
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">{t('quick_actions')}</h2>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {quickActions.map((action, index) => (
              <Tooltip key={index} text={action.tooltip} position="top">
                <Link
                  to={action.link}
                  className="card-pro hover:scale-105 transition-all duration-300 group relative overflow-hidden"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  {/* Gradient Background on Hover */}
                  <div className={`absolute inset-0 bg-gradient-to-br ${action.gradient} opacity-0 group-hover:opacity-10 transition-opacity duration-300`} />
                  
                  <div className="relative">
                    <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${action.gradient} flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                      <div className="text-white">
                        {action.icon}
                      </div>
                    </div>
                    <h3 className="text-xl font-bold mb-2 text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                      {action.title}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">
                      {action.description}
                    </p>
                    
                    {/* Arrow indicator on hover */}
                    <div className="mt-4 flex items-center text-primary-600 dark:text-primary-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                      <span className="text-sm font-semibold">{t('get_started')}</span>
                      <svg className="w-4 h-4 ml-2 group-hover:translate-x-2 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                </Link>
              </Tooltip>
            ))}
          </div>
        </div>

        {/* Recent Detections */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold">{t('recent_diseases')}</h2>
            {recentDetections.length > 0 && (
              <Link to="/history" className="text-primary-600 hover:underline">
                {t('view_all')}
              </Link>
            )}
          </div>

          {recentDetections.length > 0 ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {recentDetections.map((detection) => (
                <div key={detection.id} className="card">
                  <img
                    src={`http://localhost:8000${detection.image_url}`}
                    alt="Detection"
                    className="w-full h-40 object-cover rounded-lg mb-3"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      if (e.target.nextElementSibling) e.target.nextElementSibling.style.display = 'flex';
                    }}
                  />
                  <div 
                    className="w-full h-40 bg-gray-100 rounded-lg mb-3 items-center justify-center text-gray-400 hidden"
                    style={{ display: 'none' }}
                  >
                    <div className="text-center">
                      <FiCamera className="text-3xl text-gray-400 mx-auto mb-1" />
                      <span className="text-xs">Image Unavailable</span>
                    </div>
                  </div>
                  <h3 className="font-semibold text-lg mb-1">
                    {detection.disease_detected}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {t('confidence')}: {detection.confidence >= 1 ? detection.confidence.toFixed(1) : (detection.confidence * 100).toFixed(1)}%
                  </p>
                  <span
                    className={`inline-block px-2 py-1 rounded text-xs mt-2 ${
                      detection.severity === 'high'
                        ? 'bg-red-100 text-red-800'
                        : detection.severity === 'moderate'
                        ? 'bg-yellow-100 text-yellow-800'
                        : detection.severity === 'low'
                        ? 'bg-blue-100 text-blue-800'
                        : 'bg-green-100 text-green-800'
                    }`}
                  >
                    {detection.severity || 'none'}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <div className="card bg-gradient-to-r from-green-50 to-blue-50 p-8 text-center">
              <FiCamera className="text-6xl text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">No Disease Detections Yet</h3>
              <p className="text-gray-600 mb-4">
                Upload your first crop image to detect diseases using AI
              </p>
              <Link
                to="/disease-detection"
                className="inline-block bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition"
              >
                Start Detection
              </Link>
            </div>
          )}
        </div>

        {/* My Crops */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold">{t('my_crops')}</h2>
            {crops.length > 0 && (
              <Link to="/profile" className="text-primary-600 hover:underline">
                {t('manage_crops')}
              </Link>
            )}
          </div>

          {crops.length > 0 ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
              {crops.map((crop) => (
                <div key={crop.id} className="card">
                  <h3 className="font-semibold text-lg capitalize">{translateCropName(crop.crop_type, t)}</h3>
                  {crop.variety && (
                    <p className="text-sm text-gray-600">{t('variety')}: {crop.variety}</p>
                  )}
                  {crop.area_size && (
                    <p className="text-sm text-gray-600">
                      {t('area')}: {crop.area_size} {t('acres')}
                    </p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="card bg-gradient-to-r from-yellow-50 to-green-50 p-8 text-center">
              <FiActivity className="text-6xl text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">{t('no_crops_added')}</h3>
              <p className="text-gray-600 mb-4">
                {t('add_crops_to_track')}
              </p>
              <Link
                to="/profile"
                className="inline-block bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition"
              >
                {t('add_crops')}
              </Link>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;
