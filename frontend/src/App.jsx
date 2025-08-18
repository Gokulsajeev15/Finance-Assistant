/**
 * Main App Component - The heart of our Finance Assistant
 * 
 * This is the main page that users see. It has three tabs:
 * 1. Companies - Browse and search big companies
 * 2. Technical Analysis - Analyze stock performance  
 * 3. AI Assistant - Chat with our financial AI
 * 
 * Think of this as the control center for the whole app!
 */

// Import React tools and our components with clear names
import { useState, useEffect } from 'react';
import AppHeader from './components/AppHeader';
import CompanySearchBar from './components/CompanySearchBar';
import CompanyInfoCard from './components/CompanyInfoCard';
import StockAnalysisPanel from './components/StockAnalysisPanel';
import FinancialChatbot from './components/FinancialChatbot';
import { financeAPI } from './api_services/financial_api_client';

function App() {
  // Store information about companies we're showing
  const [companies, setCompanies] = useState([]);
  
  // Track if we're loading data
  const [loading, setLoading] = useState(false);
  
  // Store any error messages
  const [error, setError] = useState('');
  
  // Track which tab is currently selected
  const [activeTab, setActiveTab] = useState('companies');

  // Load top companies when the app starts
  useEffect(() => {
    loadTopCompanies();
  }, []);

  // Function to load the top companies from our API
  const loadTopCompanies = async () => {
    setLoading(true);  // Show loading spinner
    try {
      const response = await financeAPI.getTopCompanies();
      setCompanies(response.data);  // Store the companies
      setError('');  // Clear any old errors
    } catch (err) {
      setError('Failed to load companies');
      console.error(err);
    } finally {
      setLoading(false);  // Hide loading spinner
    }
  };

  // Function to search for companies
  const handleSearch = async (query) => {
    setLoading(true);  // Show loading spinner
    setError('');  // Clear any old errors
    
    try {
      const response = await financeAPI.searchCompanies(query);
      setCompanies(response.data);  // Show search results
    } catch (err) {
      setError(err.response?.data?.detail || 'Search failed');
    } finally {
      setLoading(false);  // Hide loading spinner
    }
  };

  const tabs = [
    { id: 'companies', label: 'Companies' },
    { id: 'technical', label: 'Technical Analysis' },
    { id: 'ai', label: 'AI Assistant' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <AppHeader />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tab Navigation */}
        <div className="flex justify-center mb-8">
          <div className="flex space-x-1 bg-gray-200 rounded-lg p-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 rounded-md transition-colors font-medium ${
                  activeTab === tab.id
                    ? 'bg-black text-white'
                    : 'text-gray-600 hover:text-black hover:bg-gray-100'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {activeTab === 'companies' && (
          <>
            <div className="mb-8">
              <CompanySearchBar onSearch={handleSearch} />
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-6">
                {error}
              </div>
            )}

            {loading ? (
              <div className="flex justify-center items-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {companies.map((company) => (
                  <CompanyInfoCard key={`${company.rank}-${company.company}`} company={company} />
                ))}
              </div>
            )}
          </>
        )}

        {activeTab === 'technical' && <StockAnalysisPanel />}
        {activeTab === 'ai' && <FinancialChatbot />}
      </main>
    </div>
  );
}

export default App;
