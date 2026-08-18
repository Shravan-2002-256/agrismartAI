// Filter and Sort Component for History Page
// Provides filtering by crop type, severity, and date range
// Custom implementation - no heavy libraries

import { useState } from 'react';
import { FiFilter, FiChevronDown } from 'react-icons/fi';

const FilterSort = ({ onFilterChange, onSortChange }) => {
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    cropType: 'all',
    severity: 'all',
    dateRange: 'all'
  });
  const [sortBy, setSortBy] = useState('newest');

  const cropOptions = [
    { value: 'all', label: 'All Crops' },
    { value: 'tomato', label: '🍅 Tomato' },
    { value: 'potato', label: '🥔 Potato' },
    { value: 'corn', label: '🌽 Corn' },
    { value: 'wheat', label: '🌾 Wheat' },
  ];

  const severityOptions = [
    { value: 'all', label: 'All Severities' },
    { value: 'high', label: '🔴 High' },
    { value: 'moderate', label: '🟡 Moderate' },
    { value: 'low', label: '🟢 Low' },
    { value: 'none', label: '⚪ None' },
  ];

  const dateRangeOptions = [
    { value: 'all', label: 'All Time' },
    { value: 'today', label: 'Today' },
    { value: 'week', label: 'This Week' },
    { value: 'month', label: 'This Month' },
    { value: '3months', label: 'Last 3 Months' },
  ];

  const sortOptions = [
    { value: 'newest', label: 'Newest First' },
    { value: 'oldest', label: 'Oldest First' },
    { value: 'confidence-high', label: 'Highest Confidence' },
    { value: 'confidence-low', label: 'Lowest Confidence' },
    { value: 'severity', label: 'Severity: High → Low' },
  ];

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilterChange?.(newFilters);
  };

  const handleSortChange = (value) => {
    setSortBy(value);
    onSortChange?.(value);
  };

  const resetFilters = () => {
    const defaultFilters = {
      cropType: 'all',
      severity: 'all',
      dateRange: 'all'
    };
    setFilters(defaultFilters);
    setSortBy('newest');
    onFilterChange?.(defaultFilters);
    onSortChange?.('newest');
  };

  const activeFilterCount = Object.values(filters).filter(v => v !== 'all').length;

  return (
    <div className="space-y-3">
      {/* Filter Toggle Button */}
      <div className="flex items-center gap-3 flex-wrap">
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="flex items-center gap-2 px-4 py-2 rounded-lg border-2 border-gray-200 
                     dark:border-gray-600 hover:border-primary-500 dark:hover:border-primary-400 
                     transition-all duration-200 bg-white dark:bg-gray-800"
        >
          <FiFilter className={activeFilterCount > 0 ? 'text-primary-600' : 'text-gray-500'} />
          <span className="font-medium text-gray-700 dark:text-gray-300">
            Filters {activeFilterCount > 0 && `(${activeFilterCount})`}
          </span>
          <FiChevronDown className={`transition-transform duration-200 ${showFilters ? 'rotate-180' : ''}`} />
        </button>

        {/* Sort Dropdown - Always visible */}
        <select
          value={sortBy}
          onChange={(e) => handleSortChange(e.target.value)}
          className="px-4 py-2 rounded-lg border-2 border-gray-200 dark:border-gray-600 
                     bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 font-medium
                     focus:border-primary-500 dark:focus:border-primary-400 transition-colors"
        >
          {sortOptions.map(option => (
            <option key={option.value} value={option.value}>{option.label}</option>
          ))}
        </select>

        {activeFilterCount > 0 && (
          <button
            onClick={resetFilters}
            className="text-sm text-gray-500 hover:text-primary-600 dark:hover:text-primary-400 
                       transition-colors font-medium"
          >
            Clear All
          </button>
        )}
      </div>

      {/* Expandable Filter Panel */}
      {showFilters && (
        <div className="glass-card p-4 animate-slideInLeft">
          <div className="grid md:grid-cols-3 gap-4">
            {/* Crop Filter */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                Crop Type
              </label>
              <select
                value={filters.cropType}
                onChange={(e) => handleFilterChange('cropType', e.target.value)}
                className="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 
                           bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                           focus:border-primary-500 dark:focus:border-primary-400 transition-colors"
              >
                {cropOptions.map(option => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            </div>

            {/* Severity Filter */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                Severity Level
              </label>
              <select
                value={filters.severity}
                onChange={(e) => handleFilterChange('severity', e.target.value)}
                className="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 
                           bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                           focus:border-primary-500 dark:focus:border-primary-400 transition-colors"
              >
                {severityOptions.map(option => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            </div>

            {/* Date Range Filter */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                Date Range
              </label>
              <select
                value={filters.dateRange}
                onChange={(e) => handleFilterChange('dateRange', e.target.value)}
                className="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 
                           bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                           focus:border-primary-500 dark:focus:border-primary-400 transition-colors"
              >
                {dateRangeOptions.map(option => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FilterSort;
