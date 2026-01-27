import axios from 'axios';
import { SearchFormData, SearchResult, LoginRequest, SignupRequest, AuthResponse, User } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Request interceptor to add auth token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor completely disabled for debugging
// apiClient.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     console.log('API Error:', error.response?.status, error.config?.url, error.response?.data);
//     return Promise.reject(error);
//   }
// );

// Authentication API
export const authAPI = {
  login: async (credentials: LoginRequest): Promise<AuthResponse> => {
    try {
      const response = await apiClient.post('/auth/login', credentials);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const message = error.response?.data?.detail || error.message || 'Login failed';
        throw new Error(message);
      }
      throw new Error('An unexpected error occurred during login');
    }
  },

  signup: async (userData: SignupRequest): Promise<AuthResponse> => {
    try {
      const response = await apiClient.post('/auth/signup', userData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const message = error.response?.data?.detail || error.message || 'Signup failed';
        throw new Error(message);
      }
      throw new Error('An unexpected error occurred during signup');
    }
  },

  getCurrentUser: async (): Promise<User> => {
    try {
      const response = await apiClient.get('/auth/me');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const message = error.response?.data?.detail || error.message || 'Failed to get user info';
        throw new Error(message);
      }
      throw new Error('An unexpected error occurred');
    }
  },

  resetPassword: async (token: string, newPassword: string, email?: string): Promise<{ message: string }> => {
    try {
      if (email) {
        // Email-based reset (new approach)
        const response = await apiClient.post('/auth/forgot-password', {
          email,
          new_password: newPassword
        });
        return response.data;
      } else {
        // Token-based reset (legacy approach) - not implemented in backend yet
        throw new Error('Token-based password reset is not currently supported');
      }
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const message = error.response?.data?.detail || error.message || 'Failed to reset password';
        throw new Error(message);
      }
      throw new Error('An unexpected error occurred');
    }
  },
};

// Search API (now protected)
export const searchKnowledgeCore = async (formData: SearchFormData): Promise<SearchResult> => {
  try {
    const response = await apiClient.post('/search', formData);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.detail || error.message || 'API request failed';
      throw new Error(message);
    }
    throw new Error('An unexpected error occurred');
  }
};

// Phone Validation API
export const validatePhoneNumbers = async (formData: SearchFormData): Promise<any> => {
  try {
    const response = await apiClient.post('/validate-phone', formData);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.detail || error.message || 'Phone validation failed';
      throw new Error(message);
    }
    throw new Error('An unexpected error occurred during phone validation');
  }
};

// Email Validation API
export const validateEmailAddress = async (formData: SearchFormData): Promise<any> => {
  try {
    const response = await apiClient.post('/validate-email', formData);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.detail || error.message || 'Email validation failed';
      throw new Error(message);
    }
    throw new Error('An unexpected error occurred during email validation');
  }
};

// AI Insights API
export const generateAIInsights = async (category: string, profileData: any): Promise<any> => {
  try {
    const response = await apiClient.post('/ai-insights', {
      category: category,
      profile_data: profileData
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.detail || error.message || 'AI insights generation failed';
      throw new Error(message);
    }
    throw new Error('An unexpected error occurred during AI insights generation');
  }
};

// Recent Searches API
export const getRecentSearches = async (): Promise<any> => {
  try {
    const response = await apiClient.get('/recent/searches');
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.detail || error.message || 'Failed to fetch recent searches';
      throw new Error(message);
    }
    throw new Error('An unexpected error occurred while fetching recent searches');
  }
};

export const clearRecentSearches = async (): Promise<any> => {
  try {
    const response = await apiClient.delete('/recent/searches/clear');
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.detail || error.message || 'Failed to clear recent searches';
      throw new Error(message);
    }
    throw new Error('An unexpected error occurred while clearing recent searches');
  }
};

export const deleteSelectedSearches = async (searchIds: number[]): Promise<any> => {
  try {
    const response = await apiClient.delete('/recent/searches/delete', {
      data: { search_ids: searchIds }
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.detail || error.message || 'Failed to delete selected searches';
      throw new Error(message);
    }
    throw new Error('An unexpected error occurred while deleting selected searches');
  }
};

// Transaction History API
export const getTransactions = async (constituentId: string): Promise<any> => {
  try {
    const response = await apiClient.get(`/transactions/${constituentId}`);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.detail || error.message || 'Failed to fetch transactions';
      throw new Error(message);
    }
    throw new Error('An unexpected error occurred while fetching transactions');
  }
};

// DataIris Search API
export const searchDataIris = async (formData: SearchFormData): Promise<any> => {
  try {
    const response = await apiClient.post('/datairis/search', formData);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.detail || error.message || 'DataIris search failed';
      throw new Error(message);
    }
    throw new Error('An unexpected error occurred during DataIris search');
  }
};

// DataIris Health Check API
export const checkDataIrisHealth = async (): Promise<any> => {
  try {
    const response = await apiClient.get('/datairis/health');
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.detail || error.message || 'DataIris health check failed';
      throw new Error(message);
    }
    throw new Error('An unexpected error occurred during DataIris health check');
  }
};

// Philanthropy API - BrightData donations search
export const getPhilanthropy = async (donorName: string, city: string, state: string): Promise<any> => {
  try {
    const params = new URLSearchParams();
    params.append('donor_name', donorName);
    params.append('city', city);
    params.append('state', state);
    
    const response = await apiClient.post(`/philanthropy/contributions?${params.toString()}`);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.detail || error.message || 'Failed to fetch philanthropy data';
      throw new Error(message);
    }
    throw new Error('An unexpected error occurred while fetching philanthropy data');
  }
};