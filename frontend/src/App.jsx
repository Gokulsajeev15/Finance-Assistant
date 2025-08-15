import { useState, useEffect } from 'react';
import Header from './components/Header';
import SearchBar from './components/SearchBar';
import CompanyCard from './components/CompanyCard';
import TechnicalAnalysis from './components/TechnicalAnalysis';
import AIChat from './components/AIChat';
import { financeAPI } from './services/api';

function App() {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('companies');

  useEffect(() => {
    loadTopCompanies();
  }, []);

  const loadTopCompanies = async () => {
    setLoading(true);
    try {
      const response = await financeAPI.getTopCompanies();
      setCompanies(response.data);
      setError('');
    } catch (err) {
      setError('Failed to load companies');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (query) => {
    setLoading(true);
    setError('');
    
    try {
      const response = await financeAPI.searchCompanies(query);
      setCompanies(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Search failed');
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'companies', label: 'Companies' },
    { id: 'technical', label: 'Technical Analysis' },
    { id: 'ai', label: 'AI Assistant' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
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
              <SearchBar onSearch={handleSearch} />
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
                  <CompanyCard key={`${company.rank}-${company.company}`} company={company} />
                ))}
              </div>
            )}
          </>
        )}

        {activeTab === 'technical' && <TechnicalAnalysis />}
        {activeTab === 'ai' && <AIChat />}
      </main>
    </div>
  );
}

export default App;
