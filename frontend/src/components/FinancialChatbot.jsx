// Import React tools and icons
import { useState } from 'react';
import { financeAPI } from '../api_services/financial_api_client';
import { MessageCircle, Send } from 'lucide-react';

const FinancialChatbot = () => {
  // Store what the user is typing
  const [query, setQuery] = useState('');
  
  // Store all the messages (user questions and AI answers)
  const [messages, setMessages] = useState([]);
  
  // Track if AI is thinking
  const [loading, setLoading] = useState(false);

  // Function that runs when user sends a message
  const handleSubmit = async (e) => {
    e.preventDefault();  // Don't refresh the page
    if (!query.trim()) return;  // Don't send empty messages

    // Add the user's message to the chat
    const userMessage = { type: 'user', content: query };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);  // Show "thinking..." message

    try {
      // Ask our AI to answer the question
      const response = await financeAPI.processAIQuery(query);
      const aiMessage = {
        type: 'ai',
        content: response.data.message || 'No response available',
        data: response.data
      };
      // Add AI's answer to the chat
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      // If something went wrong, show an error message
      const errorMessage = {
        type: 'ai',
        content: error.response?.data?.detail || 'Sorry, I had trouble with that question.',
        error: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);  // Hide "thinking..." message
      setQuery('');  // Clear the input box
    }
  };

  // Example questions to help users get started
  const exampleQueries = [
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
            {exampleQueries.map((example, index) => (
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
          <div
            key={index}
            className={`mb-4 ${
              message.type === 'user' ? 'text-right' : 'text-left'
            }`}
          >
            <div
              className={`inline-block max-w-xs lg:max-w-2xl px-4 py-3 rounded-lg ${
                message.type === 'user'
                  ? 'bg-black text-white'
                  : message.error
                  ? 'bg-red-100 text-red-700'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              <div className="whitespace-pre-line">{message.content}</div>
              
              {/* Show suggestions if available */}
              {message.data && message.data.suggestions && (
                <div className="mt-3 space-y-1">
                  <p className="text-xs font-medium text-gray-600">Try asking:</p>
                  {message.data.suggestions.map((suggestion, idx) => (
                    <button
                      key={idx}
                      onClick={() => setQuery(suggestion)}
                      className="block w-full text-left text-xs bg-white hover:bg-gray-50 text-gray-700 px-2 py-1 rounded border border-gray-200 transition-colors"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              )}
              
              {/* Show ticker info if available */}
              {message.data && message.data.ticker && (
                <div className="mt-2 pt-2 border-t border-gray-200 text-xs">
                  <span className="font-medium">Ticker: {message.data.ticker}</span>
                  {message.data.data && message.data.data.current_price && (
                    <span className="ml-3">Price: ${message.data.data.current_price.toFixed(2)}</span>
                  )}
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
