import api from './api';

// Auth Services
export const authService = {
  async register(userData) {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  async login(credentials) {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    const response = await api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }
    
    return response.data;
  },

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },

  isAuthenticated() {
    return !!localStorage.getItem('token');
  },
};

// Disease Detection Services
export const diseaseService = {
  async getModelStatus() {
    const response = await api.get('/disease/model-status');
    return response.data;
  },

  async detectDisease(imageFile, cropType, location) {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('crop_type', cropType);
    if (location) formData.append('location', location);

    const response = await api.post('/disease/detect', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    
    return response.data;
  },

  async getHistory(limit = 20) {
    const response = await api.get(`/disease/history?limit=${limit}`);
    return response.data;
  },

  async getStats() {
    const response = await api.get('/disease/stats');
    return response.data;
  },
};

// Weather Services
export const weatherService = {
  async getForecast(lat, lon) {
    const response = await api.get(`/weather/forecast?lat=${lat}&lon=${lon}`);
    return response.data;
  },

  async getAlerts(lat, lon) {
    const response = await api.get(`/weather/alerts?lat=${lat}&lon=${lon}`);
    return response.data;
  },
};

// Market Price Services
export const marketService = {
  async getPrices(crop, region = null) {
    const params = new URLSearchParams({ crop });
    if (region) params.append('region', region);
    
    const response = await api.get(`/market/prices?${params}`);
    return response.data;
  },

  async getPredictions(crop, region = null, days = 7) {
    const params = new URLSearchParams({ crop, days });
    if (region) params.append('region', region);
    
    const response = await api.get(`/market/predict?${params}`);
    return response.data;
  },
};

// Chat Services
export const chatService = {
  async sendMessage(message, language = 'en') {
    const response = await api.post('/chat/message', { message, language });
    return response.data;
  },

  async getHistory(limit = 20) {
    const response = await api.get(`/chat/history?limit=${limit}`);
    return response.data;
  },
};

// User Profile Services
export const userService = {
  async getProfile() {
    const response = await api.get('/user/profile');
    return response.data;
  },

  async updateProfile(userData) {
    const response = await api.put('/user/profile', userData);
    localStorage.setItem('user', JSON.stringify(response.data));
    return response.data;
  },

  async getCrops() {
    const response = await api.get('/user/crops');
    return response.data;
  },

  async addCrop(cropData) {
    const response = await api.post('/user/crops', cropData);
    return response.data;
  },

  async updateCrop(cropId, cropData) {
    const response = await api.put(`/user/crops/${cropId}`, cropData);
    return response.data;
  },

  async deleteCrop(cropId) {
    const response = await api.delete(`/user/crops/${cropId}`);
    return response.data;
  },
};
