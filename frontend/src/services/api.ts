import axios from 'axios';
import { SearchFormData, SearchResult } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

export const searchExperian = async (formData: SearchFormData): Promise<SearchResult> => {
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