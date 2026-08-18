import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { FiCloud, FiDroplet, FiWind, FiAlertTriangle, FiArrowLeft, FiSun, FiCloudRain, FiCloudSnow } from 'react-icons/fi';
import Layout from '../components/common/Layout';
import Loader from '../components/common/Loader';
import { weatherService } from '../services/apiService';
import { formatDate } from '../utils/helpers';

const Weather = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [weather, setWeather] = useState(null);
  const [location, setLocation] = useState({ lat: 28.6139, lon: 77.2090 }); // Default: Delhi

  useEffect(() => {
    // Get user's location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            lat: position.coords.latitude,
            lon: position.coords.longitude,
          });
        },
        (error) => {
          console.error('Error getting location:', error);
          fetchWeather(location.lat, location.lon);
        }
      );
    } else {
      fetchWeather(location.lat, location.lon);
    }
  }, []);

  useEffect(() => {
    if (location.lat && location.lon) {
      fetchWeather(location.lat, location.lon);
    }
  }, [location]);

  const fetchWeather = async (lat, lon) => {
    try {
      const response = await weatherService.getForecast(lat, lon);
      setWeather(response.data);
    } catch (error) {
      toast.error('Failed to fetch weather data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <Loader />
      </Layout>
    );
  }

  if (!weather) {
    return (
      <Layout>
        <div className="text-center py-12">
          <p className="text-gray-600">{t('failed_to_load_weather')}</p>
        </div>
      </Layout>
    );
  }

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

        <h1 className="text-3xl font-bold">{t('weather')}</h1>

        {/* Current Weather */}
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">{t('current_weather')}</h2>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600">{weather.location}</p>
              <div className="flex items-center space-x-4 mt-2">
                <span className="text-5xl font-bold">{Math.round(weather.current.temp)}°C</span>
                <div>
                  <p className="text-gray-700 capitalize">{weather.current.description}</p>
                  <div className="flex items-center space-x-4 text-sm text-gray-600 mt-2">
                    <span className="flex items-center">
                      <FiDroplet className="mr-1" />
                      {weather.current.humidity}%
                    </span>
                    <span className="flex items-center">
                      <FiWind className="mr-1" />
                      {weather.current.wind_speed} m/s
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div className="text-6xl text-gray-600">
              {weather.current.icon.includes('01') ? <FiSun className="text-yellow-500" /> :
               weather.current.icon.includes('02') ? <FiSun className="text-yellow-400" /> :
               weather.current.icon.includes('03') ? <FiCloud /> :
               weather.current.icon.includes('04') ? <FiCloud /> :
               weather.current.icon.includes('09') ? <FiCloudRain className="text-blue-500" /> :
               weather.current.icon.includes('10') ? <FiCloudRain className="text-blue-400" /> :
               weather.current.icon.includes('11') ? <FiCloudRain className="text-purple-500" /> :
               weather.current.icon.includes('13') ? <FiCloudSnow className="text-blue-300" /> : <FiCloud />}
            </div>
          </div>
        </div>

        {/* Alerts */}
        {weather.alerts && weather.alerts.length > 0 && (
          <div className="card bg-yellow-50 border-yellow-200">
            <div className="flex items-center mb-3">
              <FiAlertTriangle className="text-yellow-600 text-2xl mr-2" />
              <h2 className="text-xl font-semibold text-yellow-800">{t('alerts')}</h2>
            </div>
            <div className="space-y-3">
              {weather.alerts.map((alert, index) => (
                <div key={index} className="bg-white p-4 rounded-lg border border-yellow-200">
                  <h3 className="font-semibold text-yellow-800 mb-1">{alert.message}</h3>
                  <p className="text-sm text-gray-700">{alert.recommendation}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 7-Day Forecast */}
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">{t('forecast')}</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            {weather.forecast.map((day, index) => (
              <div key={index} className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                <p className="font-semibold mb-2">{formatDate(day.date)}</p>
                <div className="text-4xl text-gray-600 mb-2">
                  {day.icon.includes('01') ? <FiSun className="text-yellow-500" /> :
                   day.icon.includes('02') ? <FiSun className="text-yellow-400" /> :
                   day.icon.includes('03') ? <FiCloud /> :
                   day.icon.includes('09') ? <FiCloudRain className="text-blue-500" /> : <FiCloud />}
                </div>
                <p className="text-sm text-gray-600 capitalize mb-2">{day.description}</p>
                <div className="flex justify-between text-sm">
                  <span className="text-red-600">{day.temp_max}°</span>
                  <span className="text-blue-600">{day.temp_min}°</span>
                </div>
                <div className="text-xs text-gray-600 mt-2 space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="flex items-center">
                      <FiDroplet className="mr-1" />
                      {t('humidity')}
                    </span>
                    <span>{day.humidity}%</span>
                  </div>
                  {day.precipitation > 0 && (
                    <div className="flex items-center justify-between">
                      <span>{t('rain')}</span>
                      <span>{day.precipitation}mm</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Weather;
