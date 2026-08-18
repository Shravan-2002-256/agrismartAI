export const DISEASE_SEVERITY_COLORS = {
  none: 'bg-green-100 text-green-800',
  low: 'bg-yellow-100 text-yellow-800',
  medium: 'bg-orange-100 text-orange-800',
  high: 'bg-red-100 text-red-800',
};

export const CROP_TYPES = [
  'tomato',
  'potato',
  'corn',
  'wheat',
  'rice',
  'apple',
  'grape',
  'pepper',
  'strawberry',
  'peach',
  'orange',
  'soybean',
  'cherry',
];

export const LANGUAGES = [
  { code: 'en', name: 'English', nativeName: 'English', flag: '🇬🇧' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिंदी', flag: '🇮🇳' },
  { code: 'te', name: 'Telugu', nativeName: 'తెలుగు', flag: '🇮🇳' },
  { code: 'ta', name: 'Tamil', nativeName: 'தமிழ்', flag: '🇮🇳' },
];

export const PRICE_TREND_COLORS = {
  rising: 'text-green-600',
  falling: 'text-red-600',
  stable: 'text-gray-600',
};

export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
export const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png'];

export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
