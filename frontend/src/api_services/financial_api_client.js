/**
 * Financial API Client - Connects our frontend to the backend
 * 
 * This file is like a messenger that carries information between:
 * - Our React frontend (what users see)
 * - Our Python backend (where the AI and data live)
 * 
 * It handles all the API calls so other components don't have to worry about it!
 */

import axios from 'axios';

// Where our backend server is running
const API_BASE_URL = 'http://localhost:8000';

// Create an axios instance with default settings
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// All the API functions our app can use
export const financeAPI = {
  // Check if the backend server is working
  getHealth: () => api.get('/health'),
  
  // Company-related functions
  getTopCompanies: () => api.get('/api/v1/companies/top'),  // Get biggest companies
  searchCompanies: (query) => api.get(`/api/v1/companies/search?q=${query}`),  // Search companies
  getCompanyInfo: (companyName) => api.get(`/api/v1/companies/${companyName}`),  // Get company details
  getCompaniesBySector: (sector) => api.get(`/api/v1/companies/sector/${sector}`),  // Companies by industry
  
  // Stock analysis functions
  getTechnicalAnalysis: (ticker) => api.get(`/api/v1/technical-analysis/${ticker}`),  // Full stock analysis
  getRSI: (ticker) => api.get(`/api/v1/technical-analysis/${ticker}/rsi`),  // RSI indicator
  getBollingerBands: (ticker) => api.get(`/api/v1/technical-analysis/${ticker}/bollinger-bands`),  // Bollinger Bands
  getMovingAverages: (ticker) => api.get(`/api/v1/technical-analysis/${ticker}/moving-averages`),  // Moving averages
  
  // AI chatbot functions
  processAIQuery: (query) => api.post('/api/v1/ai/query', null, { params: { query } }),  // Ask AI a question
  getAIExamples: () => api.get('/api/v1/ai/examples'),  // Get example AI questions
};
