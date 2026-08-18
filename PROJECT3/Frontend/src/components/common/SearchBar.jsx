// Global Search Component
// Allows searching across detections, features, and content
// Built with debouncing for performance

import { useState, useEffect, useRef } from 'react';
import { FiSearch, FiX } from 'react-icons/fi';
import { useNavigate } from 'react-router-dom';

const SearchBar = ({ placeholder = "Search detections, insights, features...", onSearch }) => {
  const [query, setQuery] = useState('');
  const [isExpanded, setIsExpanded] = useState(false);
  const [results, setResults] = useState([]);
  const [showResults, setShowResults] = useState(false);
  const searchRef = useRef(null);
  const navigate = useNavigate();

  // Debounce search - performance optimization
  useEffect(() => {
    const timer = setTimeout(() => {
      if (query.length > 2) {
        performSearch(query);
      } else {
        setResults([]);
        setShowResults(false);
      }
    }, 300); // 300ms delay - feels responsive but not too eager

    return () => clearTimeout(timer);
  }, [query]);

  // Close results when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowResults(false);
        setIsExpanded(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const performSearch = async (searchQuery) => {
    // In a real app, this would call an API
    // For now, we'll simulate local search across common features
    const mockResults = [
      { type: 'feature', title: 'Disease Detection', path: '/disease-detection', icon: '🔬' },
      { type: 'feature', title: 'Weather Forecast', path: '/weather', icon: '🌤️' },
      { type: 'feature', title: 'Market Prices', path: '/market', icon: '💰' },
      { type: 'feature', title: 'Chatbot Assistant', path: '/chatbot', icon: '💬' },
      { type: 'recent', title: 'Tomato Blight Detection', path: '/history', icon: '📊' },
      { type: 'recent', title: 'Potato Disease Analysis', path: '/history', icon: '📊' },
    ].filter(item => 
      item.title.toLowerCase().includes(searchQuery.toLowerCase())
    );

    setResults(mockResults.slice(0, 5)); // Limit to 5 results
    setShowResults(mockResults.length > 0);
  };

  const handleResultClick = (result) => {
    navigate(result.path);
    setQuery('');
    setShowResults(false);
    setIsExpanded(false);
  };

  const handleClear = () => {
    setQuery('');
    setResults([]);
    setShowResults(false);
  };

  return (
    <div ref={searchRef} className="relative">
      <div className={`relative transition-all duration-300 ${isExpanded ? 'w-full md:w-96' : 'w-64'}`}>
        <FiSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => setIsExpanded(true)}
          placeholder={placeholder}
          className="w-full pl-12 pr-10 py-2.5 rounded-xl border-2 border-gray-200 dark:border-gray-600 
                     focus:border-primary-500 dark:focus:border-primary-400 transition-all duration-200
                     bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        />
        {query && (
          <button
            onClick={handleClear}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 
                       dark:hover:text-gray-300 transition-colors"
          >
            <FiX size={18} />
          </button>
        )}
      </div>

      {/* Search Results Dropdown */}
      {showResults && (
        <div className="absolute top-full mt-2 w-full bg-white dark:bg-gray-800 rounded-xl shadow-2xl 
                        border border-gray-200 dark:border-gray-700 max-h-96 overflow-y-auto z-50
                        animate-fadeIn">
          <div className="p-2">
            {results.map((result, index) => (
              <button
                key={index}
                onClick={() => handleResultClick(result)}
                className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700
                           transition-colors duration-150 flex items-center gap-3 group"
              >
                <span className="text-2xl">{result.icon}</span>
                <div className="flex-1">
                  <p className="font-medium text-gray-900 dark:text-gray-100 group-hover:text-primary-600 
                                dark:group-hover:text-primary-400 transition-colors">
                    {result.title}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 capitalize">{result.type}</p>
                </div>
              </button>
            ))}
          </div>
          
          {results.length === 0 && query && (
            <div className="p-6 text-center text-gray-500 dark:text-gray-400">
              No results found for "{query}"
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchBar;
