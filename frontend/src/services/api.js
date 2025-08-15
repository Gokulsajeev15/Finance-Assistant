import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const financeAPI = {
  // Health check
  getHealth: () => api.get('/health'),
  
  // Companies endpoints
  getTopCompanies: () => api.get('/api/v1/companies/top'),
  searchCompanies: (query) => api.get(`/api/v1/companies/search?q=${query}`),
  getCompanyInfo: (companyName) => api.get(`/api/v1/companies/${companyName}`),
  getCompaniesBySector: (sector) => api.get(`/api/v1/companies/sector/${sector}`),
  
  // Technical analysis endpoints
  getTechnicalAnalysis: (ticker) => api.get(`/api/v1/technical-analysis/${ticker}`),
  getRSI: (ticker) => api.get(`/api/v1/technical-analysis/${ticker}/rsi`),
  getBollingerBands: (ticker) => api.get(`/api/v1/technical-analysis/${ticker}/bollinger-bands`),
  getMovingAverages: (ticker) => api.get(`/api/v1/technical-analysis/${ticker}/moving-averages`),
  
  // AI query endpoint
  processAIQuery: (query) => api.post('/api/v1/ai/query', null, { params: { query } }),
  getAIExamples: () => api.get('/api/v1/ai/examples'),
};
