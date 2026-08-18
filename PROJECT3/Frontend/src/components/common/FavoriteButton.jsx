// Favorites System Component
// Mark detections as favorites for quick access
// Persistent storage using localStorage

import { useState, useEffect } from 'react';
import { FiStar } from 'react-icons/fi';
import { toast } from 'react-toastify';

// Hook to manage favorites
export const useFavorites = () => {
  const [favorites, setFavorites] = useState([]);

  useEffect(() => {
    // Load favorites from localStorage
    const stored = localStorage.getItem('agrismart_favorites');
    if (stored) {
      try {
        setFavorites(JSON.parse(stored));
      } catch (error) {
        console.error('Failed to load favorites:', error);
      }
    }
  }, []);

  const toggleFavorite = (detectionId) => {
    setFavorites(prev => {
      const newFavorites = prev.includes(detectionId)
        ? prev.filter(id => id !== detectionId)
        : [...prev, detectionId];
      
      // Save to localStorage
      localStorage.setItem('agrismart_favorites', JSON.stringify(newFavorites));
      
      // Show toast
      toast.success(
        prev.includes(detectionId)
          ? 'Removed from favorites'
          : 'Added to favorites',
        { autoClose: 1500 }
      );
      
      return newFavorites;
    });
  };

  const isFavorite = (detectionId) => {
    return favorites.includes(detectionId);
  };

  return { favorites, toggleFavorite, isFavorite };
};

// Favorite Button Component
const FavoriteButton = ({ detectionId, size = 20, className = '' }) => {
  const { isFavorite, toggleFavorite } = useFavorites();
  const favorited = isFavorite(detectionId);

  return (
    <button
      onClick={(e) => {
        e.stopPropagation(); // Prevent parent click events
        toggleFavorite(detectionId);
      }}
      className={`p-2 rounded-full transition-all duration-300 hover:scale-110 ${
        favorited
          ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-600 dark:text-yellow-400'
          : 'bg-gray-100 dark:bg-gray-700 text-gray-400 hover:text-yellow-600'
      } ${className}`}
      title={favorited ? 'Remove from favorites' : 'Add to favorites'}
    >
      <FiStar
        size={size}
        className={favorited ? 'fill-current' : ''}
      />
    </button>
  );
};

export default FavoriteButton;
