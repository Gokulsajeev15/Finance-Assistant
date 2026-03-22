import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { financeAPI } from '../api_services/financial_api_client';
import { MessageCircle, Send } from 'lucide-react';

const FinancialChatbot = () => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setMessages(prev => [...prev, { type: 'user', content: query }]);
    setLoading(true);

    try {
      const response = await financeAPI.processAIQuery(query);
      setMessages(prev => [...prev, {
        type: 'ai',
        content: response.data.message || 'No response available',
        data: response.data
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        type: 'ai',
        content: error.response?.data?.detail || 'Something went wrong, please try again.',
        error: true
      }]);
    } finally {
      setLoading(false);
      setQuery('');
    }
  };

  const examples = [
    "What is Apple's stock price?",
    "Tell me about Tesla",
    "How is Microsoft doing?",
    "What is compound interest?",
    "Explain P/E ratios",
    "How should I invest?",
    "What is diversification?",
    "Analyze Google performance"
  ];

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center space-x-2 mb-6">
        <MessageCircle className="h-6 w-6 text-black" />
        <h2 className="text-2xl font-bold text-gray-900">AI Financial Assistant</h2>
      </div>

      {messages.length === 0 && (
        <div className="bg-gray-50 rounded-lg p-6 mb-6">
          <p className="text-gray-600 mb-4">Try asking me about:</p>
          <div className="flex flex-wrap gap-2">
            {examples.map((example, index) => (
              <button
                key={index}
                onClick={() => setQuery(example)}
                className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded-full text-sm transition-colors"
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="bg-white rounded-lg shadow-md mb-6 h-96 overflow-y-auto p-4">
        {messages.map((message, index) => (
          <div key={index} className={`mb-4 ${message.type === 'user' ? 'text-right' : 'text-left'}`}>
            <div className={`inline-block max-w-xs lg:max-w-2xl px-4 py-3 rounded-lg ${
              message.type === 'user'
                ? 'bg-black text-white'
                : message.error
                ? 'bg-red-100 text-red-700'
                : 'bg-gray-100 text-gray-900'
            }`}>
              <ReactMarkdown>{message.content}</ReactMarkdown>

              {message.data?.suggestions && (
                <div className="mt-3 space-y-1">
                  <p className="text-xs font-medium text-gray-600">Try asking:</p>
                  {message.data.suggestions.map((s, idx) => (
                    <button
                      key={idx}
                      onClick={() => setQuery(s)}
                      className="block w-full text-left text-xs bg-white hover:bg-gray-50 text-gray-700 px-2 py-1 rounded border border-gray-200 transition-colors"
                    >
                      {s}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="text-left">
            <div className="inline-block bg-gray-100 text-gray-900 px-4 py-2 rounded-lg">
              Thinking...
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="flex space-x-4">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask me about stocks, companies, or financial data..."
          className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="bg-black text-white p-2 rounded-md hover:bg-gray-800 disabled:opacity-50 transition-colors"
        >
          <Send className="h-5 w-5" />
        </button>
      </form>
    </div>
  );
};

export default FinancialChatbot;
