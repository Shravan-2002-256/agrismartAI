// Real-time Notification Component
// Toast notifications with custom styling
// Auto-dismiss with progress bar

import { useEffect, useState } from 'react';
import { FiCheckCircle, FiAlertCircle, FiInfo, FiX } from 'react-icons/fi';

const NotificationToast = ({ type = 'info', message, duration = 4000, onClose }) => {
  const [progress, setProgress] = useState(100);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress(prev => {
        const newProgress = prev - (100 / (duration / 100));
        if (newProgress <= 0) {
          clearInterval(interval);
          onClose?.();
          return 0;
        }
        return newProgress;
      });
    }, 100);

    return () => clearInterval(interval);
  }, [duration, onClose]);

  const config = {
    success: {
      icon: FiCheckCircle,
      bgColor: 'bg-green-50 dark:bg-green-900/20',
      iconColor: 'text-green-600 dark:text-green-400',
      progressColor: 'bg-green-600'
    },
    error: {
      icon: FiAlertCircle,
      bgColor: 'bg-red-50 dark:bg-red-900/20',
      iconColor: 'text-red-600 dark:text-red-400',
      progressColor: 'bg-red-600'
    },
    warning: {
      icon: FiAlertCircle,
      bgColor: 'bg-yellow-50 dark:bg-yellow-900/20',
      iconColor: 'text-yellow-600 dark:text-yellow-400',
      progressColor: 'bg-yellow-600'
    },
    info: {
      icon: FiInfo,
      bgColor: 'bg-blue-50 dark:bg-blue-900/20',
      iconColor: 'text-blue-600 dark:text-blue-400',
      progressColor: 'bg-blue-600'
    }
  };

  const { icon: Icon, bgColor, iconColor, progressColor } = config[type] || config.info;

  return (
    <div className={`${bgColor} rounded-xl shadow-lg overflow-hidden animate-slideInRight max-w-sm`}>
      <div className="p-4 flex items-start gap-3">
        <Icon className={`${iconColor} flex-shrink-0 mt-0.5`} size={20} />
        <p className="flex-1 text-sm text-gray-900 dark:text-white">{message}</p>
        <button
          onClick={onClose}
          className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded transition-colors"
        >
          <FiX className="text-gray-600 dark:text-gray-400" size={16} />
        </button>
      </div>
      <div className="h-1 bg-gray-200 dark:bg-gray-700">
        <div
          className={`h-full ${progressColor} transition-all duration-100 ease-linear`}
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  );
};

// Notification Container
export const NotificationContainer = () => {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    // Listen for custom notification events
    const handleNotification = (event) => {
      const { type, message, duration } = event.detail;
      const id = Date.now() + Math.random();
      
      setNotifications(prev => [...prev, { id, type, message, duration }]);
    };

    window.addEventListener('agrismart-notification', handleNotification);
    return () => window.removeEventListener('agrismart-notification', handleNotification);
  }, []);

  const removeNotification = (id) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  return (
    <div className="fixed top-4 right-4 z-[200] space-y-3 pointer-events-none">
      <div className="pointer-events-auto space-y-3">
        {notifications.map(notification => (
          <NotificationToast
            key={notification.id}
            type={notification.type}
            message={notification.message}
            duration={notification.duration}
            onClose={() => removeNotification(notification.id)}
          />
        ))}
      </div>
    </div>
  );
};

// Helper function to show notifications
export const showNotification = (type, message, duration = 4000) => {
  const event = new CustomEvent('agrismart-notification', {
    detail: { type, message, duration }
  });
  window.dispatchEvent(event);
};

export default NotificationToast;
