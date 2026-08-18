import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import axios from 'axios';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Activity, TrendingUp, AlertTriangle, CheckCircle, Calendar, MapPin, ArrowLeft } from 'lucide-react';
import ExportReportButton from '../components/common/ExportReportButton';

const DiseaseAnalytics = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [trends, setTrends] = useState(null);
  const [history, setHistory] = useState([]);
  const [treatmentEffectiveness, setTreatmentEffectiveness] = useState(null);
  const [fieldAnalysis, setFieldAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState(30);

  const getToken = () => localStorage.getItem('token');

  useEffect(() => {
    fetchAnalytics();
  }, [period]);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const token = getToken();
      const headers = { Authorization: `Bearer ${token}` };

      const [trendsRes, historyRes, treatmentRes, fieldRes] = await Promise.all([
        axios.get(`http://localhost:8000/api/v1/disease-analytics/trends?days=${period}`, { headers }),
        axios.get(`http://localhost:8000/api/v1/disease-analytics/history?days=${period}&limit=50`, { headers }),
        axios.get('http://localhost:8000/api/v1/disease-analytics/treatment-effectiveness', { headers }),
        axios.get('http://localhost:8000/api/v1/disease-analytics/field-analysis', { headers })
      ]);

      if (trendsRes.data.success) setTrends(trendsRes.data.trends);
      if (historyRes.data.success) setHistory(historyRes.data.history);
      if (treatmentRes.data.success) setTreatmentEffectiveness(treatmentRes.data.effectiveness);
      if (fieldRes.data.success) setFieldAnalysis(fieldRes.data.field_analysis);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'];

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50 py-8 px-4 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading analytics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Back Button */}
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center gap-2 text-gray-600 hover:text-primary-600 transition-colors group mb-4"
        >
          <ArrowLeft className="group-hover:-translate-x-1 transition-transform" size={20} />
          <span className="font-medium">{t('back_to_dashboard')}</span>
        </button>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h1 className="text-4xl font-bold text-gray-800 dark:text-gray-100 mb-2">📊 {t('disease_analytics_title')}</h1>
              <p className="text-gray-600 dark:text-gray-400">{t('comprehensive_analysis')}</p>
            </div>
            <ExportReportButton reportType="analytics" customData={{ trends, history, period_days: period }} />
          </div>

          {/* Period Selector */}
          <div className="mt-4 flex gap-2">
            {[7, 30, 90].map(days => (
              <button
                key={days}
                onClick={() => setPeriod(days)}
                className={`px-4 py-2 rounded-lg font-medium transition ${
                  period === days
                    ? 'bg-blue-600 text-white'
                    : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                {days} Days
              </button>
            ))}
          </div>
        </div>

        {trends && (
          <>
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow-lg p-6">
                <div className="flex items-center justify-between mb-2">
                  <Activity className="w-8 h-8 text-blue-600" />
                  <span className="text-3xl font-bold text-blue-600">{trends.total_detections}</span>
                </div>
                <p className="text-gray-600 font-medium">{t('total_detections')}</p>
              </div>

              <div className="bg-white rounded-lg shadow-lg p-6">
                <div className="flex items-center justify-between mb-2">
                  <AlertTriangle className="w-8 h-8 text-orange-600" />
                  <span className="text-3xl font-bold text-orange-600">{trends.unique_diseases}</span>
                </div>
                <p className="text-gray-600 font-medium">{t('unique_diseases')}</p>
              </div>

              <div className="bg-white rounded-lg shadow-lg p-6">
                <div className="flex items-center justify-between mb-2">
                  <CheckCircle className="w-8 h-8 text-green-600" />
                  <span className="text-3xl font-bold text-green-600">{trends.health_score}</span>
                </div>
                <p className="text-gray-600 font-medium">{t('health_score')}</p>
              </div>

              <div className="bg-white rounded-lg shadow-lg p-6">
                <div className="flex items-center justify-between mb-2">
                  <TrendingUp className="w-8 h-8 text-purple-600" />
                  <span className="text-3xl font-bold text-purple-600">
                    {trends.diseased_scans}/{trends.total_detections}
                  </span>
                </div>
                <p className="text-gray-600 font-medium">{t('diseased_scans')}</p>
              </div>
            </div>

            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              {/* Most Common Diseases */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-xl font-bold mb-4 text-gray-800">{t('most_common_diseases')}</h2>
                {trends.most_common_diseases && trends.most_common_diseases.length > 0 ? (
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={trends.most_common_diseases}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="disease" angle={-45} textAnchor="end" height={100} />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="count" fill="#3B82F6" />
                    </BarChart>
                  </ResponsiveContainer>
                ) : (
                  <p className="text-gray-500 text-center py-8">{t('no_disease_data')}</p>
                )}
              </div>

              {/* Severity Distribution */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-xl font-bold mb-4 text-gray-800">{t('severity_distribution')}</h2>
                {trends.severity_distribution && Object.keys(trends.severity_distribution).length > 0 ? (
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={Object.entries(trends.severity_distribution).map(([key, value]) => ({
                          name: key.charAt(0).toUpperCase() + key.slice(1),
                          value: value.count
                        }))}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                        outerRadius={100}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {Object.keys(trends.severity_distribution).map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                ) : (
                  <p className="text-gray-500 text-center py-8">{t('no_severity_data')}</p>
                )}
              </div>

              {/* Monthly Trend */}
              <div className="bg-white rounded-lg shadow-lg p-6 lg:col-span-2">
                <h2 className="text-xl font-bold mb-4 text-gray-800">{t('detection_trend')}</h2>
                {trends.monthly_trend && trends.monthly_trend.length > 0 ? (
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={trends.monthly_trend}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="count" stroke="#3B82F6" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                ) : (
                  <p className="text-gray-500 text-center py-8">{t('no_trend_data')}</p>
                )}
              </div>
            </div>

            {/* Crop-wise Analysis */}
            <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
              <h2 className="text-xl font-bold mb-4 text-gray-800">Crop-wise Disease Analysis</h2>
              {trends.crop_wise_diseases && Object.keys(trends.crop_wise_diseases).length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {Object.entries(trends.crop_wise_diseases).map(([crop, data]) => (
                    <div key={crop} className="border border-gray-200 rounded-lg p-4">
                      <h3 className="font-bold text-lg mb-2 text-blue-600">{crop}</h3>
                      <div className="space-y-2 text-sm">
                        <p><span className="text-gray-600">Total Detections:</span> <span className="font-semibold">{data.total}</span></p>
                        <p><span className="text-gray-600">Unique Diseases:</span> <span className="font-semibold">{data.unique}</span></p>
                        <div>
                          <p className="text-gray-600 mb-1">Most Common:</p>
                          <ul className="list-disc list-inside space-y-1 text-gray-700">
                            {data.most_common.slice(0, 3).map(([disease, count], idx) => (
                              <li key={idx} className="truncate">{disease} ({count})</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-8">No crop data available</p>
              )}
            </div>

            {/* Treatment Effectiveness */}
            {treatmentEffectiveness && treatmentEffectiveness.total_treatments > 0 && (
              <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
                <h2 className="text-xl font-bold mb-4 text-gray-800">Treatment Effectiveness</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <p className="text-3xl font-bold text-blue-600">{treatmentEffectiveness.total_treatments}</p>
                    <p className="text-gray-600">Total Treatments</p>
                  </div>
                  <div className="text-center p-4 bg-green-50 rounded-lg">
                    <p className="text-3xl font-bold text-green-600">{treatmentEffectiveness.effective}</p>
                    <p className="text-gray-600">Effective</p>
                  </div>
                  <div className="text-center p-4 bg-red-50 rounded-lg">
                    <p className="text-3xl font-bold text-red-600">{treatmentEffectiveness.ineffective}</p>
                    <p className="text-gray-600">Ineffective</p>
                  </div>
                  <div className="text-center p-4 bg-purple-50 rounded-lg">
                    <p className="text-3xl font-bold text-purple-600">{treatmentEffectiveness.success_rate}%</p>
                    <p className="text-gray-600">Success Rate</p>
                  </div>
                </div>
              </div>
            )}

            {/* Detection History */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-bold mb-4 text-gray-800">Recent Detection History</h2>
              {history && history.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">Disease</th>
                        <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">Crop</th>
                        <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">Confidence</th>
                        <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">Severity</th>
                        <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">Date</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {history.slice(0, 10).map((detection) => (
                        <tr key={detection.id} className="hover:bg-gray-50">
                          <td className="px-4 py-3 text-sm">{detection.disease_name}</td>
                          <td className="px-4 py-3 text-sm">{detection.crop_type || 'N/A'}</td>
                          <td className="px-4 py-3 text-sm">
                            <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded">
                              {detection.confidence}%
                            </span>
                          </td>
                          <td className="px-4 py-3 text-sm">
                            <span className={`px-2 py-1 rounded ${
                              detection.severity === 'critical' ? 'bg-red-100 text-red-700' :
                              detection.severity === 'high' ? 'bg-orange-100 text-orange-700' :
                              detection.severity === 'moderate' ? 'bg-yellow-100 text-yellow-700' :
                              'bg-green-100 text-green-700'
                            }`}>
                              {detection.severity || 'N/A'}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-600">{detection.days_ago} days ago</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p className="text-gray-500 text-center py-8">No detection history available</p>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default DiseaseAnalytics;
