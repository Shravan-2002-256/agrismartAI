import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { FiTrendingUp, FiTrendingDown, FiMinus, FiArrowLeft, FiCloudRain } from 'react-icons/fi';
import Layout from '../components/common/Layout';
import Loader from '../components/common/Loader';
import { marketService } from '../services/apiService';
import { CROP_TYPES } from '../utils/constants';
import { formatCurrency, formatDate } from '../utils/helpers';
import { translateCropName } from '../utils/translationHelpers';

const MarketPrices = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [selectedCrop, setSelectedCrop] = useState('tomato');
  const [priceData, setPriceData] = useState(null);

  useEffect(() => {
    fetchPrices(selectedCrop);
  }, [selectedCrop]);

  const fetchPrices = async (crop) => {
    setLoading(true);
    try {
      const response = await marketService.getPrices(crop);
      // Extract data from nested structure
      const data = response.data?.data || response.data || {};
      setPriceData(data);
    } catch (error) {
      toast.error('Failed to fetch market prices');
    } finally {
      setLoading(false);
    }
  };

  const getTrendIcon = (trend) => {
    if (trend === 'rising') return <FiTrendingUp className="text-green-600" />;
    if (trend === 'falling') return <FiTrendingDown className="text-red-600" />;
    return <FiMinus className="text-gray-600" />;
  };

  const getTrendColor = (trend) => {
    if (trend === 'rising') return 'text-green-600';
    if (trend === 'falling') return 'text-red-600';
    return 'text-gray-600';
  };

  if (loading) {
    return (
      <Layout>
        <Loader />
      </Layout>
    );
  }

  if (!priceData) {
    return (
      <Layout>
        <div className="text-center py-12">
          <p className="text-gray-600">{t('failed_to_load_market_prices')}</p>
        </div>
      </Layout>
    );
  }

  // Prepare chart data with null safety
  const chartData = [
    ...(priceData.historical_prices || []).map(item => ({
      date: formatDate(item.date),
      actual: item.price,
      type: 'historical'
    })),
    ...(priceData.predictions || []).map(item => ({
      date: formatDate(item.date),
      predicted: item.predicted_price,
      type: 'prediction'
    }))
  ];

  return (
    <Layout>
      <div className="space-y-6">
        {/* Back Button */}
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors group"
        >
          <FiArrowLeft className="group-hover:-translate-x-1 transition-transform" />
          <span className="font-medium">{t('back_to_dashboard')}</span>
        </button>

        <h1 className="text-3xl font-bold">{t('market_prices')}</h1>

        {/* Crop Selector */}
        <div className="card">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t('select_crop')}
          </label>
          <select
            value={selectedCrop}
            onChange={(e) => setSelectedCrop(e.target.value)}
            className="input-field max-w-xs"
          >
            {CROP_TYPES.map((crop) => (
              <option key={crop} value={crop} className="capitalize">
                {translateCropName(crop, t)}
              </option>
            ))}
          </select>
        </div>

        {/* V3.0 LSTM Model Info Display */}
        {priceData.model_info && (
          <div className="glass-card p-6 border-2 border-indigo-200 bg-gradient-to-r from-indigo-50 to-purple-50">
            <h4 className="font-bold text-gray-900 mb-4 flex items-center text-lg">
              <FiTrendingUp className="mr-2 text-indigo-600" /> AI Forecasting Model (V3.0 - Weather-Aware)
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-white rounded-lg p-4 shadow-sm border border-indigo-100">
                <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">{t('model_type')}</p>
                <p className="text-lg font-bold text-indigo-700">{priceData.model_info.type || priceData.forecasting_method || 'LSTM'}</p>
                <p className="text-xs text-gray-600 mt-1">{t('neural_network')}</p>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm border border-indigo-100">
                <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">{t('architecture')}</p>
                <p className="text-sm font-bold text-purple-700">{priceData.model_info.layers || '64→ 64→32→7'}</p>
                <p className="text-xs text-gray-600 mt-1">{t('lstm_layers')}</p>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm border border-indigo-100">
                <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">{t('lookback_period')}</p>
                <p className="text-lg font-bold text-blue-700">{priceData.model_info.lookback_days || '30'} {t('days')}</p>
                <p className="text-xs text-gray-600 mt-1">{t('historical_data')}</p>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm border border-indigo-100">
                <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">{t('forecast_horizon')}</p>
                <p className="text-lg font-bold text-green-700">{priceData.model_info.forecast_days || '7'} {t('days_ahead')}</p>
                <p className="text-xs text-gray-600 mt-1">Ahead prediction</p>
              </div>
            </div>
            
            {/* Weather Integration Badge */}
            {priceData.model_info.weather_integrated && (
              <div className="mt-4 bg-gradient-to-r from-blue-50 to-green-50 rounded-lg p-4 border-2 border-green-300">
                <div className="flex items-center mb-2">
                  <FiCloudRain className="text-blue-600 mr-2 text-xl" />
                  <h5 className="font-bold text-green-800">{t('weather_integration_enabled')}</h5>
                </div>
                <p className="text-sm text-gray-700 mb-2">
                  <strong>Features:</strong> {priceData.model_info.features || 'Price + Humidity + Rainfall + Temperature'}
                </p>
                <p className="text-xs text-gray-600">
                  This model considers weather conditions (humidity, rainfall, temperature) alongside historical prices to predict price changes during extreme weather events like heavy monsoons, droughts, or heat waves.
                </p>
              </div>
            )}
            
            <div className="mt-4 bg-white rounded-lg p-3 border border-blue-200">
              <p className="text-sm text-gray-700">
                <strong>Methodology:</strong> Long Short-Term Memory (LSTM) neural networks capture temporal patterns and market volatility better than traditional forecasting methods. This multivariate model learns from 30 days of historical price data combined with weather conditions to predict the next 7 days with confidence intervals.
              </p>
            </div>
          </div>
        )}

        {/* Current Price */}
        <div className="grid md:grid-cols-2 gap-6">
          <div className="card">
            <h2 className="text-lg font-semibold mb-2">{t('current_price')}</h2>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-4xl font-bold text-primary-600">
                  {formatCurrency(priceData.current_price)}
                </p>
                <p className="text-sm text-gray-600 mt-1">{t('per_kg')}</p>
              </div>
              <div className={`flex items-center space-x-2 ${getTrendColor(priceData.trend)}`}>
                {getTrendIcon(priceData.trend)}
                <span className="text-lg font-semibold capitalize">
                  {priceData.trend === 'rising' ? t('rising') :
                   priceData.trend === 'falling' ? t('falling') :
                   t('stable')}
                </span>
              </div>
            </div>
          </div>

          <div className="card bg-blue-50 border-blue-200">
            <h2 className="text-lg font-semibold mb-2 text-blue-800">{t('price_trend')}</h2>
            <p className="text-gray-700">
              {priceData.trend === 'rising' ? t('price_trend_rising_desc') :
               priceData.trend === 'falling' ? t('price_trend_falling_desc') :
               t('price_trend_desc')}
            </p>
          </div>
        </div>

        {/* Price Chart */}
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">{t('price_history_forecast')}</h2>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                tick={{ fontSize: 12 }}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="actual" 
                stroke="#16a34a" 
                strokeWidth={2}
                name={t('actual_price')}
                dot={{ r: 3 }}
              />
              <Line 
                type="monotone" 
                dataKey="predicted" 
                stroke="#2563eb" 
                strokeWidth={2}
                strokeDasharray="5 5"
                name={t('predicted_price')}
                dot={{ r: 3 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Predictions Table */}
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">{t('seven_day_predictions')}</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">{t('date')}</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">{t('predicted_price_label')}</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">{t('uncertainty')}</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {priceData.predictions && priceData.predictions.length > 0 ? (
                  priceData.predictions.map((pred, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm">{formatDate(pred.date)}</td>
                      <td className="px-4 py-3 text-sm font-semibold text-primary-600">
                        {formatCurrency(pred.predicted_price)}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600">
                        ±{((1 - pred.confidence) * 100).toFixed(1)}%
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="3" className="px-4 py-8 text-center text-gray-500">
                      No price predictions available
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default MarketPrices;
