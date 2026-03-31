import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Generate a unique session ID once per browser tab.
// crypto.randomUUID() is built into modern browsers — no library needed.
// This ID groups all messages from this tab into one conversation in the DB.
const SESSION_ID = crypto.randomUUID();

export const financeAPI = {
  getHealth: () => api.get('/health'),

  getTopCompanies: () => api.get('/api/v1/companies/top'),
  searchCompanies: (query) => api.get(`/api/v1/companies/search?q=${query}`),
  getCompanyInfo: (companyName) => api.get(`/api/v1/companies/${companyName}`),

  getTechnicalAnalysis: (ticker) => api.get(`/api/v1/technical-analysis/${ticker}`),
  getRSI: (ticker) => api.get(`/api/v1/technical-analysis/${ticker}/rsi`),
  getBollingerBands: (ticker) => api.get(`/api/v1/technical-analysis/${ticker}/bollinger-bands`),
  getMovingAverages: (ticker) => api.get(`/api/v1/technical-analysis/${ticker}/moving-averages`),

  processAIQuery: (query) => api.post('/api/v1/ai/query', null, { params: { query, session_id: SESSION_ID } }),
  getAIExamples: () => api.get('/api/v1/ai/examples'),
};
