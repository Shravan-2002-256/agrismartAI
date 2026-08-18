import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';
import { TrendingUp, TrendingDown, Minus, Activity } from 'lucide-react';

const FarmHealthScore = () => {
  const { t } = useTranslation();
  const [healthData, setHealthData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHealthScore();
  }, []);

  const fetchHealthScore = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/api/v1/farm-health/score', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setHealthData(response.data);
    } catch (error) {
      console.error('Error fetching health score:', error);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600 dark:text-green-400';
    if (score >= 60) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getScoreBgColor = (score) => {
    if (score >= 80) return 'bg-green-100 dark:bg-green-900/30';
    if (score >= 60) return 'bg-yellow-100 dark:bg-yellow-900/30';
    return 'bg-red-100 dark:bg-red-900/30';
  };

  const getScoreText = (score) => {
    if (score >= 80) return t('excellent');
    if (score >= 60) return t('good');
    if (score >= 40) return t('fair');
    return t('needs_attention');
  };

  const getTrendIcon = (trend) => {
    if (trend > 0) return <TrendingUp className="w-5 h-5 text-green-600" />;
    if (trend < 0) return <TrendingDown className="w-5 h-5 text-red-600" />;
    return <Minus className="w-5 h-5 text-gray-600" />;
  };

  if (loading) {
    return (
      <div className="card">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4"></div>
          <div className="h-32 bg-gray-200 dark:bg-gray-700 rounded"></div>
        </div>
      </div>
    );
  }

  const score = healthData?.overall_score || 0;
  const trend = healthData?.trend || 0;
  
  console.log('🏥 Farm Health Data:', healthData);
  console.log('🏥 Score:', score, 'Trend:', trend);

  return (
    <div className="card hover:shadow-lg transition-shadow duration-300">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100 flex items-center gap-2">
            <Activity className="w-5 h-5 text-primary-600 dark:text-primary-400" />
            {t('farm_health_score')}
          </h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {t('overall_farm_performance')}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {getTrendIcon(trend)}
          <span className={`text-sm font-medium ${trend >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {trend > 0 ? '+' : ''}{trend}%
          </span>
        </div>
      </div>

      {/* Score Gauge */}
      <div className="relative">
        <div className="flex items-center justify-center">
          <div className={`relative w-48 h-48 rounded-full ${getScoreBgColor(score)} flex items-center justify-center`}>
            <div className="absolute inset-0 rounded-full border-8 border-white dark:border-gray-800"></div>
            <div className="text-center z-10">
              <div className={`text-6xl font-bold ${getScoreColor(score)}`}>
                {score}
              </div>
              <div className="text-sm font-medium text-gray-600 dark:text-gray-300 mt-1">
                {getScoreText(score)}
              </div>
            </div>
            
            {/* Circular progress indicator */}
            <svg className="absolute inset-0 w-full h-full -rotate-90">
              <circle
                cx="96"
                cy="96"
                r="88"
                stroke="currentColor"
                strokeWidth="8"
                fill="none"
                className="text-gray-200 dark:text-gray-700"
              />
              <circle
                cx="96"
                cy="96"
                r="88"
                stroke="currentColor"
                strokeWidth="8"
                fill="none"
                strokeDasharray={`${(score / 100) * 552.92} 552.92`}
                className={score >= 80 ? 'text-green-500' : score >= 60 ? 'text-yellow-500' : 'text-red-500'}
                strokeLinecap="round"
              />
            </svg>
          </div>
        </div>

        {/* Breakdown */}
        <div className="mt-6 grid grid-cols-2 gap-4">
          <div className="text-center p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
            <div className="text-2xl font-bold text-green-600 dark:text-green-400">
              {healthData?.healthy_count || 0}
            </div>
            <div className="text-xs text-gray-600 dark:text-gray-300 mt-1">
              {t('healthy_crops')}
            </div>
          </div>
          <div className="text-center p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
              {healthData?.total_scans || 0}
            </div>
            <div className="text-xs text-gray-600 dark:text-gray-300 mt-1">
              {t('total_scans')}
            </div>
          </div>
          <div className="text-center p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
            <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
              {healthData?.active_crops || 0}
            </div>
            <div className="text-xs text-gray-600 dark:text-gray-300 mt-1">
              {t('active_crops')}
            </div>
          </div>
          <div className="text-center p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
            <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
              {healthData?.issues_detected !== undefined ? healthData.issues_detected : 0}
            </div>
            <div className="text-xs text-gray-600 dark:text-gray-300 mt-1">
              {t('issues_detected')}
            </div>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      {healthData?.recommendations && healthData.recommendations.length > 0 && (
        <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
          <h4 className="text-sm font-semibold text-blue-900 dark:text-blue-300 mb-2">
            {t('recommendations')}
          </h4>
          <ul className="text-sm text-blue-800 dark:text-blue-200 space-y-1">
            {healthData.recommendations.slice(0, 3).map((rec, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-blue-600 dark:text-blue-400">•</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FarmHealthScore;
