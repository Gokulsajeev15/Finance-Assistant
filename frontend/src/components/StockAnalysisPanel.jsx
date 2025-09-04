import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { financeAPI } from '../api_services/financial_api_client';
import { BarChart3 } from 'lucide-react';

const StockAnalysisPanel = () => {
  const [ticker, setTicker] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalysis = async (e) => {
    e.preventDefault();
    if (!ticker.trim()) return;

    setLoading(true);
    setError('');
    
    try {
      // First try to get technical analysis directly
      let analysisData = null;
      let searchTicker = ticker.trim().toUpperCase();
      
      try {
        // Try direct technical analysis API first
        const directResponse = await financeAPI.getTechnicalAnalysis(searchTicker);
        analysisData = directResponse.data;
      } catch (directError) {
        // If direct API fails, try to search for the company and get its ticker
        if (ticker.length > 5 || !ticker.match(/^[A-Z]+$/i)) {
          try {
            const searchResponse = await financeAPI.searchCompanies(ticker);
            if (searchResponse.data && searchResponse.data.length > 0) {
              searchTicker = searchResponse.data[0].ticker;
              const directResponse = await financeAPI.getTechnicalAnalysis(searchTicker);
              analysisData = directResponse.data;
            }
          } catch (searchError) {
            // Fall back to AI query
            const aiResponse = await financeAPI.processAIQuery(`Technical analysis of ${ticker}`);
            
            if (aiResponse.data.type === 'error') {
              throw new Error(aiResponse.data.message);
            }
            
            // Extract data from AI response
            analysisData = aiResponse.data.data;
          }
        } else {
          // If it looks like a ticker but failed, try AI as fallback
          const aiResponse = await financeAPI.processAIQuery(`Technical analysis of ${ticker}`);
          
          if (aiResponse.data.type === 'error') {
            throw new Error(aiResponse.data.message);
          }
          
          // Extract data from AI response
          analysisData = aiResponse.data.data;
        }
      }
      
      if (analysisData) {
        setAnalysis(analysisData);
      } else {
        throw new Error('No analysis data available');
      }
      
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch technical analysis');
      setAnalysis(null);
    } finally {
      setLoading(false);
    }
  };

  const getRSIColor = (rsi) => {
    if (rsi > 70) return 'text-red-600';
    if (rsi < 30) return 'text-green-600';
    return 'text-yellow-600';
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center space-x-2 mb-6">
        <BarChart3 className="h-6 w-6 text-black" />
        <h2 className="text-2xl font-bold text-gray-900">Technical Analysis</h2>
      </div>

      <form onSubmit={handleAnalysis} className="mb-6">
        <div className="flex space-x-4">
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            placeholder="Enter company name or ticker (e.g., Apple, AAPL, Tesla, Microsoft)"
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-gray-500 focus:border-transparent outline-none"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-black text-white px-6 py-2 rounded-md hover:bg-gray-800 disabled:opacity-50 transition-colors"
          >
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>
      </form>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-6">
          {error}
        </div>
      )}

      {analysis && (
        <div className="space-y-6">
          {/* Company Information */}
          {(analysis.stock_data?.company_name || analysis.stock_data?.sector) && (
            <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-black">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Company Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {analysis.stock_data?.company_name && (
                  <div>
                    <span className="text-gray-600">Company:</span>
                    <span className="ml-2 font-semibold">{analysis.stock_data.company_name}</span>
                  </div>
                )}
                {analysis.stock_data?.sector && (
                  <div>
                    <span className="text-gray-600">Sector:</span>
                    <span className="ml-2 font-semibold">{analysis.stock_data.sector}</span>
                  </div>
                )}
              </div>
            </div>
          )}
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Price Data */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Price Information</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Current Price:</span>
                  <span className="font-semibold">${analysis.stock_data?.current_price?.toFixed(2) || 'N/A'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">52-Week High:</span>
                  <span className="font-semibold">${analysis.stock_data?.['52_week_high']?.toFixed(2) || 'N/A'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">52-Week Low:</span>
                  <span className="font-semibold">${analysis.stock_data?.['52_week_low']?.toFixed(2) || 'N/A'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Volume:</span>
                  <span className="font-semibold">{(analysis.stock_data?.volume)?.toLocaleString() || 'N/A'}</span>
                </div>
              </div>
            </div>

            {/* RSI */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Technical Indicators</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">RSI:</span>
                  <span className={`font-semibold ${getRSIColor(analysis.technical_data?.rsi?.value)}`}>
                    {analysis.technical_data?.rsi?.value ? analysis.technical_data.rsi.value.toFixed(2) : 'N/A'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Signal:</span>
                  <span className="text-sm text-gray-700">{analysis.technical_data?.rsi?.interpretation || 'N/A'}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Moving Averages */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Moving Averages</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <p className="text-gray-600 text-sm">SMA 20:</p>
                <p className="font-semibold">${analysis.technical_data?.sma_20?.toFixed(2) || 'N/A'}</p>
              </div>
              <div className="text-center">
                <p className="text-gray-600 text-sm">SMA 50:</p>
                <p className="font-semibold">${analysis.technical_data?.sma_50?.toFixed(2) || 'N/A'}</p>
              </div>
              <div className="text-center">
                <p className="text-gray-600 text-sm">EMA 12:</p>
                <p className="font-semibold">${analysis.technical_data?.ema_12?.toFixed(2) || 'N/A'}</p>
              </div>
              <div className="text-center">
                <p className="text-gray-600 text-sm">EMA 26:</p>
                <p className="font-semibold">${analysis.technical_data?.ema_26?.toFixed(2) || 'N/A'}</p>
              </div>
            </div>
            {analysis.technical_data?.trend && (
              <div className="mt-4 text-center">
                <p className="text-gray-600 text-sm">Trend:</p>
                <p className={`font-semibold ${analysis.technical_data.trend === 'Up' ? 'text-green-600' : 'text-red-600'}`}>
                  {analysis.technical_data.trend}
                </p>
              </div>
            )}
          </div>

          {/* Bollinger Bands */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Bollinger Bands</h3>
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center">
                <p className="text-gray-600 text-sm">Upper:</p>
                <p className="font-semibold">${analysis.technical_data?.bollinger_bands?.upper?.toFixed(2) || 'N/A'}</p>
              </div>
              <div className="text-center">
                <p className="text-gray-600 text-sm">Middle:</p>
                <p className="font-semibold">${analysis.technical_data?.bollinger_bands?.middle?.toFixed(2) || 'N/A'}</p>
              </div>
              <div className="text-center">
                <p className="text-gray-600 text-sm">Lower:</p>
                <p className="font-semibold">${analysis.technical_data?.bollinger_bands?.lower?.toFixed(2) || 'N/A'}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StockAnalysisPanel;

