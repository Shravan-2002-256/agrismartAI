import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import { ArrowLeft } from 'lucide-react';

const IrrigationCalculator = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    crop_type: 'tomato',
    soil_type: 'loamy',
    area_acres: '',
    growth_stage: 'mid',
    temperature: '',
    humidity: '',
    rainfall_last_week: 0,
    irrigation_efficiency: 75
  });

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const cropTypes = ['rice', 'wheat', 'corn', 'tomato', 'potato', 'cotton', 'sugarcane', 'banana', 'onion', 'cabbage'];
  const soilTypes = ['sandy', 'loamy', 'clay', 'silt'];
  const growthStages = ['initial', 'development', 'mid', 'late'];

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResults(null);

    try {
      // Validate irrigation efficiency
      const efficiency = parseFloat(formData.irrigation_efficiency);
      const efficiencyDecimal = (efficiency > 0 ? efficiency : 75) / 100;

      const response = await axios.post('http://localhost:8000/api/v1/irrigation/calculate', {
        ...formData,
        area_acres: parseFloat(formData.area_acres),
        temperature: parseFloat(formData.temperature),
        humidity: parseFloat(formData.humidity),
        rainfall_last_week: parseFloat(formData.rainfall_last_week),
        irrigation_efficiency: efficiencyDecimal
      });

      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.error || t('irrig_failed'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Back Button */}
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center gap-2 text-gray-600 hover:text-primary-600 transition-colors group mb-4"
        >
          <ArrowLeft className="group-hover:-translate-x-1 transition-transform" size={20} />
          <span className="font-medium">{t('back_to_dashboard')}</span>
        </button>

        <h1 className="text-4xl font-bold text-gray-800 mb-2">{t('irrig_title')}</h1>
        <p className="text-gray-600 mb-8">{t('irrig_subtitle')}</p>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold mb-6 text-blue-600">{t('irrig_enter_details')}</h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Crop Type */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">{t('irrig_crop_type')}</label>
                <select
                  name="crop_type"
                  value={formData.crop_type}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  {cropTypes.map(crop => (
                    <option key={crop} value={crop}>{crop.charAt(0).toUpperCase() + crop.slice(1)}</option>
                  ))}
                </select>
              </div>

              {/* Soil Type */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">{t('irrig_soil_type')}</label>
                <select
                  name="soil_type"
                  value={formData.soil_type}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  {soilTypes.map(soil => (
                    <option key={soil} value={soil}>{t(`soil_${soil}`)}</option>
                  ))}
                </select>
              </div>

              {/* Growth Stage */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">{t('irrig_growth_stage')}</label>
                <select
                  name="growth_stage"
                  value={formData.growth_stage}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  {growthStages.map(stage => (
                    <option key={stage} value={stage}>{t(`growth_${stage}`)}</option>
                  ))}
                </select>
              </div>

              {/* Area */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">{t('irrig_field_area')}</label>
                <input
                  type="number"
                  name="area_acres"
                  value={formData.area_acres}
                  onChange={handleInputChange}
                  step="0.1"
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., 2.5"
                />
              </div>

              {/* Temperature */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">{t('irrig_temperature')}</label>
                <input
                  type="number"
                  name="temperature"
                  value={formData.temperature}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., 28"
                />
              </div>

              {/* Humidity */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">{t('irrig_humidity')}</label>
                <input
                  type="number"
                  name="humidity"
                  value={formData.humidity}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., 65"
                />
              </div>

              {/* Rainfall */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">{t('irrig_rainfall')}</label>
                <input
                  type="number"
                  name="rainfall_last_week"
                  value={formData.rainfall_last_week}
                  onChange={handleInputChange}
                  step="0.1"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., 10"
                />
              </div>

              {/* Irrigation Efficiency */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('irrig_efficiency')} - {formData.irrigation_efficiency}%
                </label>
                <input
                  type="range"
                  name="irrigation_efficiency"
                  value={formData.irrigation_efficiency}
                  onChange={handleInputChange}
                  min="50"
                  max="95"
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-gray-500">
                  <span>{t('irrig_flood')}</span>
                  <span>{t('irrig_sprinkler')}</span>
                  <span>{t('irrig_drip')}</span>
                </div>
              </div>

              {error && (
                <div className="bg-red-50 text-red-600 px-4 py-3 rounded-lg">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50"
              >
                {loading ? t('irrig_calculating') : t('irrig_calculate_btn')}
              </button>
            </form>
          </div>

          {/* Results */}
          <div>
            {results && results.success && (
              <div className="space-y-6">
                {/* Summary Card */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h2 className="text-2xl font-semibold mb-4 text-green-600">{t('irrig_water_reqs')}</h2>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <p className="text-sm text-gray-600">{t('irrig_weekly_req')}</p>
                      <p className="text-2xl font-bold text-blue-600">
                        {results.calculations.water_volume_liters.toLocaleString()} L
                      </p>
                    </div>
                    <div className="bg-green-50 p-4 rounded-lg">
                      <p className="text-sm text-gray-600">{t('irrig_per_irrigation')}</p>
                      <p className="text-2xl font-bold text-green-600">
                        {results.recommendations.water_per_irrigation_liters.toLocaleString()} L
                      </p>
                    </div>
                    <div className="bg-purple-50 p-4 rounded-lg">
                      <p className="text-sm text-gray-600">{t('irrig_frequency')}</p>
                      <p className="text-2xl font-bold text-purple-600">
                        {t('irrig_every_days', { days: results.recommendations.irrigation_frequency_days })}
                      </p>
                    </div>
                    <div className="bg-yellow-50 p-4 rounded-lg">
                      <p className="text-sm text-gray-600">{t('irrig_depth')}</p>
                      <p className="text-2xl font-bold text-yellow-600">
                        {results.recommendations.irrigation_depth_mm} mm
                      </p>
                    </div>
                  </div>
                </div>

                {/* Schedule */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h3 className="text-xl font-semibold mb-4">{t('irrig_schedule')}</h3>
                  <div className="space-y-3">
                    {results.schedule.map((item, index) => (
                      <div key={index} className="flex items-center justify-between bg-gray-50 p-3 rounded-lg">
                        <div>
                          <span className="font-semibold">{t('irrig_day')} {item.day}</span>
                          <p className="text-sm text-gray-600">{item.notes}</p>
                        </div>
                        <span className="text-blue-600 font-bold">
                          {item.water_liters.toLocaleString()} L
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Tips */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h3 className="text-xl font-semibold mb-4">{t('irrig_tips')}</h3>
                  <ul className="space-y-2">
                    {results.tips.map((tip, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-green-500 mr-2">✓</span>
                        <span className="text-gray-700">{tip}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Technical Details */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h3 className="text-xl font-semibold mb-4">{t('irrig_tech_details')}</h3>
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div>
                      <p className="text-gray-600">{t('irrig_et0')}</p>
                      <p className="font-semibold">{results.calculations.et0_mm_per_day} mm/day</p>
                    </div>
                    <div>
                      <p className="text-gray-600">{t('irrig_kc')}</p>
                      <p className="font-semibold">{results.calculations.crop_coefficient_kc}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">{t('irrig_etc')}</p>
                      <p className="font-semibold">{results.calculations.crop_water_requirement_mm_per_day} mm/day</p>
                    </div>
                    <div>
                      <p className="text-gray-600">{t('irrig_system_eff')}</p>
                      <p className="font-semibold">{results.recommendations.irrigation_efficiency_percent}%</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {!results && (
              <div className="bg-white rounded-lg shadow-lg p-12 text-center">
                <p className="text-gray-500">{t('irrig_enter_msg')}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default IrrigationCalculator;
