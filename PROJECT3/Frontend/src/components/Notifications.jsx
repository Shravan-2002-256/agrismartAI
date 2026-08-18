import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bell, X, Check, AlertCircle, Cloud, Bug, TrendingUp, Droplet, Calendar } from 'lucide-react';
import { useTranslation } from 'react-i18next';

const Notifications = () => {
  const { t } = useTranslation();
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [showDropdown, setShowDropdown] = useState(false);
  const [loading, setLoading] = useState(false);

  const getToken = () => localStorage.getItem('token');

  const fetchNotifications = async () => {
    try {
      const token = getToken();
      if (!token) return;

      const response = await axios.get('http://localhost:8000/api/v1/notifications/', {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (response.data.success) {
        setNotifications(response.data.notifications);
        setUnreadCount(response.data.notifications.filter(n => !n.is_read).length);
      }
    } catch (error) {
      console.error('Error fetching notifications:', error);
    }
  };

  const markAsRead = async (notificationId) => {
    try {
      const token = getToken();
      await axios.put(
        `http://localhost:8000/api/v1/notifications/${notificationId}/read`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchNotifications();
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  };

  const deleteNotification = async (notificationId, event) => {
    // Prevent triggering the card's onClick
    event?.stopPropagation();
    
    try {
      const token = getToken();
      await axios.delete(
        `http://localhost:8000/api/v1/notifications/${notificationId}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchNotifications();
    } catch (error) {
      console.error('Error deleting notification:', error);
    }
  };

  const markAllAsRead = async () => {
    try {
      const token = getToken();
      setLoading(true);
      await axios.put(
        'http://localhost:8000/api/v1/notifications/read-all',
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchNotifications();
    } catch (error) {
      console.error('Error marking all as read:', error);
    } finally {
      setLoading(false);
    }
  };

  const createTestNotification = async () => {
    try {
      const token = getToken();
      const testTypes = ['weather', 'disease', 'irrigation', 'price'];
      const randomType = testTypes[Math.floor(Math.random() * testTypes.length)];
      
      const testMessages = {
        weather: {
          title: '⛈️ Weather Alert',
          message: 'Heavy rainfall expected in next 24 hours. Postpone irrigation.',
          priority: 'high'
        },
        disease: {
          title: '🐛 Disease Alert',
          message: 'Late Blight detected in tomato field. Immediate treatment required.',
          priority: 'critical'
        },
        irrigation: {
          title: '💧 Irrigation Reminder',
          message: 'Your tomato field needs watering. Best time: 6-8 AM tomorrow.',
          priority: 'medium'
        },
        price: {
          title: '📈 Price Update',
          message: 'Tomato prices increased by 12%. Good time to sell.',
          priority: 'low'
        }
      };

      await axios.post(
        'http://localhost:8000/api/v1/notifications/test',
        { type: randomType, ...testMessages[randomType] },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      fetchNotifications();
    } catch (error) {
      console.error('Error creating test notification:', error);
    }
  };

  useEffect(() => {
    fetchNotifications();
    const interval = setInterval(fetchNotifications, 30000); // Poll every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const getIcon = (type) => {
    switch (type) {
      case 'weather': return <Cloud className="w-5 h-5" />;
      case 'disease': return <Bug className="w-5 h-5" />;
      case 'price': return <TrendingUp className="w-5 h-5" />;
      case 'irrigation': return <Droplet className="w-5 h-5" />;
      case 'harvest': return <Calendar className="w-5 h-5" />;
      default: return <Bell className="w-5 h-5" />;
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'critical': return 'bg-red-100 border-red-400 text-red-800';
      case 'high': return 'bg-orange-100 border-orange-400 text-orange-800';
      case 'medium': return 'bg-blue-100 border-blue-400 text-blue-800';
      case 'low': return 'bg-gray-100 border-gray-400 text-gray-800';
      default: return 'bg-blue-100 border-blue-400 text-blue-800';
    }
  };

  return (
    <div className="relative">
      {/* Bell Icon with Badge */}
      <button
        onClick={() => setShowDropdown(!showDropdown)}
        className="relative p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-full transition"
      >
        <Bell className="w-6 h-6" />
        {unreadCount > 0 && (
          <span className="absolute top-0 right-0 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
            {unreadCount}
          </span>
        )}
      </button>

      {/* Dropdown */}
      {showDropdown && (
        <div className="absolute right-0 mt-2 w-96 bg-white rounded-lg shadow-2xl border border-gray-200 z-50 max-h-[600px] overflow-hidden flex flex-col">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-green-600 text-white p-4">
            <div className="flex justify-between items-center">
              <div>
                <h3 className="font-bold text-lg">{t('notifications')}</h3>
                <p className="text-sm opacity-90">{unreadCount} unread</p>
              </div>
              <button
                onClick={() => setShowDropdown(false)}
                className="hover:bg-white/20 p-1 rounded"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Mark All Read Button */}
          {unreadCount > 0 && (
            <div className="px-4 py-2 border-b">
              <button
                onClick={markAllAsRead}
                disabled={loading}
                className="text-sm text-blue-600 hover:text-blue-800 font-medium flex items-center gap-2"
              >
                <Check className="w-4 h-4" />
                {t('mark_all_read')}
              </button>
            </div>
          )}

          {/* Test Notification Button (for testing) */}
          <div className="px-4 py-2 border-b bg-gray-50">
            <button
              onClick={createTestNotification}
              className="text-sm text-green-600 hover:text-green-800 font-medium flex items-center gap-2 w-full"
            >
              <Bell className="w-4 h-4" />
              🧪 Create Test Notification
            </button>
          </div>

          {/* Notifications List */}
          <div className="overflow-y-auto flex-1">
            {notifications.length === 0 ? (
              <div className="p-8 text-center text-gray-500">
                <Bell className="w-12 h-12 mx-auto mb-2 opacity-30" />
                <p>{t('no_notifications')}</p>
                <button
                  onClick={createTestNotification}
                  className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition text-sm font-medium"
                >
                  🧪 Create Test Notification
                </button>
              </div>
            ) : (
              <div className="divide-y">
                {notifications.map((notification) => (
                  <div
                    key={notification.id}
                    className={`p-4 hover:bg-gray-50 transition relative group ${
                      !notification.is_read ? 'bg-blue-50' : ''
                    }`}
                  >
                    <div className="flex gap-3">
                      {/* Icon */}
                      <div 
                        className={`p-2 rounded-full ${getPriorityColor(notification.priority)} cursor-pointer`}
                        onClick={() => !notification.is_read && markAsRead(notification.id)}
                      >
                        {getIcon(notification.type)}
                      </div>

                      {/* Content */}
                      <div 
                        className="flex-1 min-w-0 cursor-pointer"
                        onClick={() => !notification.is_read && markAsRead(notification.id)}
                      >
                        <div className="flex justify-between items-start mb-1">
                          <h4 className="font-semibold text-gray-800 text-sm pr-8">
                            {notification.title}
                          </h4>
                          {!notification.is_read && (
                            <span className="w-2 h-2 bg-blue-600 rounded-full flex-shrink-0"></span>
                          )}
                        </div>
                        <p className="text-sm text-gray-600 mb-2">
                          {notification.message}
                        </p>
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-gray-500">
                            {notification.time_ago}
                          </span>
                          <span className={`text-xs px-2 py-1 rounded ${
                            notification.priority === 'critical' ? 'bg-red-100 text-red-700' :
                            notification.priority === 'high' ? 'bg-orange-100 text-orange-700' :
                            notification.priority === 'medium' ? 'bg-blue-100 text-blue-700' :
                            'bg-gray-100 text-gray-700'
                          }`}>
                            {notification.priority}
                          </span>
                        </div>
                      </div>

                      {/* Close/Delete Button */}
                      <button
                        onClick={(e) => deleteNotification(notification.id, e)}
                        className="absolute top-2 right-2 p-1 rounded-full hover:bg-red-100 text-gray-400 hover:text-red-600 transition opacity-0 group-hover:opacity-100"
                        title="Delete notification"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Notifications;
