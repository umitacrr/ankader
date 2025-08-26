import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Axios interceptor for token
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling 401 errors
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

const authService = {
  // Giriş yap
  login: async (credentials) => {
    try {
      const response = await axios.post(`${API_URL}/auth/login`, credentials);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Sunucu hatası' };
    }
  },

  // Mevcut kullanıcı bilgilerini al
  getCurrentUser: async () => {
    try {
      const response = await axios.get(`${API_URL}/auth/me`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Sunucu hatası' };
    }
  },

  // Şifre değiştir
  changePassword: async (passwordData) => {
    try {
      const response = await axios.put(`${API_URL}/auth/change-password`, passwordData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Sunucu hatası' };
    }
  },

  // Aktivite logla
  logActivity: async (activityData) => {
    try {
      const response = await axios.post(`${API_URL}/auth/log-activity`, activityData);
      return response.data;
    } catch (error) {
      console.error('Activity log error:', error);
      // Don't throw error for activity logging
      return { success: false };
    }
  },

  // Token doğrula
  verifyToken: async () => {
    try {
      const response = await axios.post(`${API_URL}/auth/verify-token`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Sunucu hatası' };
    }
  },

  // Çıkış yap
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  }
};

export default authService;
