import React from 'react';
import { Link } from 'react-router-dom';
import { 
  FiInbox, 
  FiAlertCircle, 
  FiImage, 
  FiMessageSquare, 
  FiTrendingUp,
  FiSearch,
  FiFile
} from 'react-icons/fi';

const EmptyState = ({ 
  icon: Icon = FiInbox, 
  title, 
  description, 
  actionLabel, 
  actionLink, 
  actionOnClick,
  type = 'default' 
}) => {
  const iconColors = {
    default: 'text-gray-400',
    warning: 'text-yellow-500',
    info: 'text-blue-500',
    success: 'text-green-500',
    primary: 'text-primary-500',
  };

  const bgColors = {
    default: 'bg-gray-100 dark:bg-gray-800',
    warning: 'bg-yellow-100 dark:bg-yellow-900/20',
    info: 'bg-blue-100 dark:bg-blue-900/20',
    success: 'bg-green-100 dark:bg-green-900/20',
    primary: 'bg-primary-100 dark:bg-primary-900/20',
  };

  return (
    <div className="text-center py-16 px-4">
      <div className={`inline-flex p-6 ${bgColors[type]} rounded-full mb-6`}>
        <Icon className={`text-5xl ${iconColors[type]}`} />
      </div>
      
      <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
        {title}
      </h3>
      
      {description && (
        <p className="text-gray-600 dark:text-gray-400 mb-6 max-w-md mx-auto">
          {description}
        </p>
      )}
      
      {(actionLabel && (actionLink || actionOnClick)) && (
        actionLink ? (
          <Link to={actionLink} className="btn-primary-pro inline-flex items-center">
            {actionLabel}
          </Link>
        ) : (
          <button onClick={actionOnClick} className="btn-primary-pro">
            {actionLabel}
          </button>
        )
      )}
    </div>
  );
};

// Preset empty states for common scenarios
export const NoDetectionsState = ({ t }) => (
  <EmptyState
    icon={FiImage}
    type="primary"
    title={t ? t('no_detections_title') : 'No Detections Yet'}
    description={t ? t('no_detections_desc') : 'Upload your first crop image to get started with AI-powered disease detection'}
    actionLabel={t ? t('start_detecting') : 'Start Detecting'}
    actionLink="/disease-detection"
  />
);

export const NoHistoryState = ({ t }) => (
  <EmptyState
    icon={FiFile}
    type="info"
    title={t ? t('no_history_title') : 'No History Found'}
    description={t ? t('no_history_desc') : 'Your detection history will appear here once you start analyzing crops'}
    actionLabel={t ? t('detect_now') : 'Detect Now'}
    actionLink="/disease-detection"
  />
);

export const NoSearchResultsState = ({ t, query }) => (
  <EmptyState
    icon={FiSearch}
    type="warning"
    title={t ? t('no_results_title') : 'No Results Found'}
    description={
      query 
        ? `We couldn't find anything matching "${query}". Try different keywords.`
        : 'No results match your search criteria. Try adjusting your filters.'
    }
  />
);

export const ErrorState = ({ t, message, onRetry }) => (
  <EmptyState
    icon={FiAlertCircle}
    type="warning"
    title={t ? t('error_title') : 'Something Went Wrong'}
    description={message || (t ? t('error_desc') : 'We encountered an error. Please try again.')}
    actionLabel={t ? t('retry') : 'Retry'}
    actionOnClick={onRetry}
  />
);

export const NoChatHistoryState = ({ t }) => (
  <EmptyState
    icon={FiMessageSquare}
    type="primary"
    title={t ? t('no_chat_title') : 'Start a Conversation'}
    description={t ? t('no_chat_desc') : 'Ask me anything about farming, crops, diseases, or best practices'}
  />
);

export const NoMarketDataState = ({ t }) => (
  <EmptyState
    icon={FiTrendingUp}
    type="info"
    title={t ? t('no_market_data') : 'No Market Data Available'}
    description={t ? t('no_market_data_desc') : 'Market prices will be displayed here once data is available'}
  />
);

export default EmptyState;
