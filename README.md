# Finance Assistant

A comprehensive financial analysis platform featuring **real AI-powered backend API** using Hugging Face models and a modern React frontend. The system provides real-time stock data for the **top 100 companies by market cap**, technical analysis, and intelligent financial insights through both a web interface and REST API.

## Key Features

- **Real-Time Data**: Dynamic top 100 companies by market cap from Yahoo Finance API
- **Real AI Models**: Actual machine learning models (FinBERT, RoBERTa, Sentence Transformers)
- **Technical Analysis**: RSI, Bollinger Bands, Moving Averages, and trend analysis
- **Smart Search**: Search companies by name, sector, or ticker symbol
- **AI Assistant**: Natural language processing for financial questions
- **High Performance**: In-memory caching with 6-hour auto-refresh
- **Modern UI**: Clean React interface with Tailwind CSS

## System Architecture

Finance Assistant combines professional-grade financial analysis with cutting-edge AI capabilities. Users can analyze any of the top 100 companies using company names or ticker symbols, get detailed technical analysis reports, and interact with an AI assistant powered by real machine learning models.

![Finance Assistant Screenshot](https://github.com/user-attachments/assets/2f110db2-5bfe-46ff-8ce2-7eba955b5bf5)

## Application Features

### Frontend Application
- **Clean Interface**: Professional black and white design focused on data clarity
- **Company Browser**: Browse and search top 100 companies by market cap with sector filtering
- **Technical Analysis**: Interactive charts and indicators with real company name support
- **AI Assistant**: Real AI-powered natural language processing for financial questions
- **Real-time Data**: Live integration with Yahoo Finance API
- **Responsive Design**: Works seamlessly across desktop and mobile devices

### Backend API
- **Dynamic Company Database**: Real-time top 100 companies by market cap (auto-updated every 6 hours)
- **Stock Data**: Real-time stock prices and comprehensive company information
- **Technical Analysis**: RSI, Bollinger Bands, Moving Averages, and trend analysis
- **AI Query Processing**: Real machine learning models for natural language understanding
- **High Performance**: In-memory caching and optimized data processing
- **Production Ready**: Scalable architecture with comprehensive error handling

![Technical Analysis Screenshot](https://github.com/user-attachments/assets/24e433d8-2fb6-4d57-919c-1fb491f777f6)

## AI Technology Stack

### Real AI Models (Hugging Face)
- **FinBERT** (`ProsusAI/finbert`): Financial sentiment analysis and market mood detection
- **Sentence Transformers** (`all-MiniLM-L6-v2`): Intent classification and semantic understanding
- **RoBERTa** (`deepset/roberta-base-squad2`): Question answering for complex financial queries

### AI Capabilities
- **Intent Classification**: Automatically categorizes questions (price, analysis, company, education, strategy)
- **Sentiment Analysis**: Analyzes financial text and stock movements for market sentiment
- **Smart Routing**: Routes queries to appropriate AI handlers based on understanding
- **Fallback Handling**: Graceful degradation if AI models are unavailable
- **GPU Acceleration**: Automatic CUDA detection for faster AI processing

## Technology Stack

### Frontend
- **React 18**: Modern component-based UI framework
- **Vite**: Fast development server and build tool
- **Tailwind CSS**: Utility-first styling framework
- **Axios**: HTTP client for API communication
- **Lucide React**: Clean and minimal icons

### Backend
- **FastAPI**: High-performance Python web framework
- **Yahoo Finance**: Real-time financial data source
- **Pandas**: Advanced data manipulation and analysis
- **Pydantic**: Data validation and serialization
- **Uvicorn**: Production-grade ASGI server
- **PyTorch**: Deep learning framework for AI models
- **Transformers**: Hugging Face model loading and inference
- **Sentence Transformers**: Advanced NLP capabilities

![AI Assistant Screenshot](https://github.com/user-attachments/assets/c7d5eade-600d-4b79-a705-334463b441c8)

## Quick Start

### Prerequisites
- **Python 3.11+** 
- **Node.js 18+** 
- **8GB+ RAM** (recommended for AI models)
- **5GB+ Storage** (for model downloads)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Gokulsajeev15/Finance-Assistant.git
   cd Finance-Assistant
   ```

2. **Start the Backend**
   ```bash
   # Install Python dependencies (including AI models)
   uv sync
   
   # Start the backend server
   python start_backend.py
   ```
   
3. **Start the Frontend**
   ```bash
   # Navigate to frontend directory
   cd frontend
   
   # Install dependencies
   npm install
   
   # Start the development server
   npm run dev
   ```

4. **Access the Application**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

## Usage Examples

### Web Interface Usage
The frontend provides three main sections:

- **Companies Tab**: Browse top 100 companies by market cap with sector and industry filters
- **Technical Analysis Tab**: Enter company names or ticker symbols for comprehensive analysis
- **AI Assistant Tab**: Ask questions in natural language powered by real AI models

### Example AI Queries
```
"Analyze Apple's performance"
"Technical analysis of Tesla" 
"How is Microsoft doing?"
"What's Amazon's revenue?"
"Explain diversification"
"What is the 98th ranked company?"
```

### API Usage Examples
```bash
# Get comprehensive technical analysis
curl "http://localhost:8000/api/v1/technical-analysis/AAPL"

# Search companies by name or sector
curl "http://localhost:8000/api/v1/companies/search?q=technology"

# Process natural language queries with AI
curl -X POST "http://localhost:8000/api/v1/ai/query?query=Analyze Tesla performance"

# Get top 100 companies by market cap
curl "http://localhost:8000/api/v1/companies/top"

# Get cache information (updates every 6 hours)
curl "http://localhost:8000/api/v1/companies/cache/info"
```

## API Endpoints

### System Health
- `GET /` - Application welcome message
- `GET /health` - System health check and status

### Company Data
- `GET /api/v1/companies/top` - Top 100 companies by market cap
- `GET /api/v1/companies/search?q={query}` - Search companies by name, sector, or industry
- `GET /api/v1/companies/{name}` - Detailed company information
- `GET /api/v1/companies/cache/info` - Cache status and update information
- `GET /api/v1/companies/cache/refresh` - Force refresh company data

### Technical Analysis
- `GET /api/v1/technical-analysis/{ticker}` - Complete technical analysis
- `GET /api/v1/technical-analysis/{ticker}/rsi` - RSI indicator analysis
- `GET /api/v1/technical-analysis/{ticker}/bollinger-bands` - Bollinger Bands data
- `GET /api/v1/technical-analysis/{ticker}/moving-averages` - Moving averages analysis

### AI Processing
- `POST /api/v1/ai/query` - Process natural language financial queries using real AI models
- `GET /api/v1/ai/examples` - Get example queries and usage patterns

## Project Structure

```
Finance-Assistant/
├── start_backend.py              # Backend startup script
├── backend/                      # FastAPI backend application
│   ├── app/
│   │   ├── main.py                  # Main FastAPI application
│   │   ├── dependencies.py          # Service dependency injection
│   │   ├── models/
│   │   │   └── models.py            # Pydantic data models
│   │   ├── routers/                 # API route handlers
│   │   │   ├── companies.py         # Company endpoints
│   │   │   ├── technical_analysis.py # Technical analysis endpoints
│   │   │   └── ai_queries.py        # AI query processing endpoints
│   │   └── services/                # Business logic services
│   │       ├── dynamic_companies.py # Dynamic top 100 companies service
│   │       ├── stock_data_service.py # Enhanced stock data service
│   │       ├── huggingface_ai.py    # Real AI models (FinBERT, RoBERTa, etc.)
│   │       └── data_cache.py        # Caching layer
│   └── Dockerfile                   # Docker containerization
├── frontend/                     # React frontend application
│   ├── src/
│   │   ├── components/              # React components
│   │   │   ├── AppHeader.jsx        # Application header
│   │   │   ├── CompanySearchBar.jsx # Search functionality
│   │   │   ├── CompanyInfoCard.jsx  # Company display cards
│   │   │   ├── StockAnalysisPanel.jsx # Technical analysis interface
│   │   │   └── FinancialChatbot.jsx # AI assistant interface
│   │   ├── api_services/
│   │   │   └── financial_api_client.js # API service layer
│   │   ├── App.jsx                  # Main application component
│   │   ├── main.jsx                 # Application entry point
│   │   └── index.css                # Global styles
│   ├── package.json                 # Frontend dependencies
│   ├── vite.config.js               # Vite build configuration
│   └── tailwind.config.js           # Tailwind CSS configuration
├── pyproject.toml                # Python dependencies (including AI libraries)
└── README.md                     # Project documentation
```

## Key Features in Detail

### Intelligent Company Recognition
The system recognizes company names and variations, allowing natural language input:
- **"Apple"** → automatically maps to AAPL
- **"Tesla"** → automatically maps to TSLA  
- **"Microsoft"** → automatically maps to MSFT
- **"Berkshire Hathaway"** → automatically maps to BRK-A

### Advanced Technical Analysis
Comprehensive technical analysis includes:
- **RSI Analysis**: 14-day Relative Strength Index with overbought/oversold signals
- **Moving Averages**: SMA 20/50 and EMA 12/26 with trend analysis  
- **Bollinger Bands**: Upper, middle, and lower bands with position analysis
- **Price Analysis**: 6-month range positioning and volume analysis
- **Market Context**: Market cap categorization and sector information

### AI-Powered Insights
The AI assistant uses real machine learning models for detailed, context-aware responses:
- **Intent Classification**: Automatically understands question types using Sentence Transformers
- **Sentiment Analysis**: Analyzes financial sentiment using FinBERT
- **Smart Question Answering**: Handles complex queries using RoBERTa
- **Analysis Reports**: Comprehensive company analysis with technical insights
- **Performance Metrics**: Financial performance with market context
- **Technical Summaries**: Detailed technical analysis with actionable signals
- **Natural Language**: Truly understands questions in plain English

### Dynamic Data Management
- **Real-time Updates**: Top 100 companies refreshed every 6 hours
- **Smart Caching**: In-memory caching for optimal performance
- **Parallel Processing**: Concurrent API calls for faster data retrieval
- **Automatic Fallback**: Graceful handling of API failures

## Development & Deployment

### Development Mode
```bash
# Backend development (with AI models)
python start_backend.py

# Frontend development  
cd frontend
npm run dev
```

### Production Build
```bash
# Frontend production build
cd frontend
npm run build

# Backend production deployment
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

### AI Model Management
- **Auto-Download**: Models downloaded automatically on first run
- **GPU Support**: Automatic CUDA detection for 10x+ speed improvement  
- **Fallback**: Graceful degradation to rule-based responses if models fail
- **Memory Optimization**: Efficient model loading and memory management

## API Response Examples

### Technical Analysis Response
```json
{
  "ticker": "AAPL",
  "last_updated": "2025-09-04T14:38:02.154353",
  "stock_data": {
    "ticker": "AAPL", 
    "current_price": 230.89,
    "change": -1.75,
    "change_percent": -0.76,
    "volume": 58415211,
    "52_week_high": 249.39,
    "52_week_low": 168.80,
    "company_name": "Apple Inc.",
    "sector": "Technology",
    "market_cap": 3500000000000,
    "pe_ratio": 28.5,
    "dividend_yield": 0.44
  },
  "technical_data": {
    "rsi": {
      "value": 67.08,
      "interpretation": "Neutral"
    },
    "sma_20": 216.59,
    "sma_50": 209.36,
    "ema_12": 223.27, 
    "ema_26": 217.13,
    "bollinger_bands": {
      "upper": 237.22,
      "middle": 216.59,
      "lower": 195.97
    },
    "trend": "Up"
  }
}
```

### AI Query Response
```json
{
  "type": "analysis",
  "ticker": "AAPL",
  "message": "**AI Analysis: Apple Inc.**\n\n**$230.89** (-0.76%)\n\n**Technical Indicators:**\n• RSI: 67.1 (Neutral)\n• 20-day SMA: $216.59\n• 50-day SMA: $209.36\n\n**AI Sentiment:** Positive (85% confidence)",
  "data": {
    "stock_data": {...},
    "technical_data": {...},
    "ai_sentiment": {
      "label": "positive", 
      "score": 0.85
    }
  }
}
```

## Performance & Requirements

### System Requirements
- **Minimum**: 8GB RAM, Python 3.11+, Node.js 18+
- **Recommended**: 16GB RAM, CUDA-capable GPU for AI acceleration
- **Storage**: 5GB+ free space for AI models and data cache

### AI Model Performance
- **First Run**: AI models downloaded automatically (~2-3GB total)
- **Memory Usage**: ~4-6GB RAM for all AI models loaded
- **GPU Support**: Automatic CUDA detection for 10x+ speed improvement
- **CPU Fallback**: Graceful degradation to CPU if GPU unavailable

### Data Update Cycle
- **Company Data**: Refreshed every 6 hours automatically
- **Stock Prices**: Real-time via Yahoo Finance API
- **Cache Strategy**: In-memory with intelligent invalidation
- **Performance**: Sub-second response times for cached data

## Contributing

This project follows clean architecture principles and maintains high code quality standards:

1. **Code Structure**: Follow existing patterns and naming conventions
2. **Type Safety**: Add appropriate type hints and documentation  
3. **Error Handling**: Include comprehensive error handling for new features
4. **Testing**: Test both frontend and backend integration thoroughly
5. **AI Integration**: Test AI model integration and fallback scenarios
6. **Design**: Maintain clean, professional design aesthetic

### Code Quality Standards
- **Type Safety**: Full type hints in Python with Pydantic models
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Clean Architecture**: Separation of concerns with clear module boundaries
- **Documentation**: Extensive inline documentation and API specs
- **Performance**: Optimized queries and efficient data processing
- **AI Integration**: Robust fallback handling for AI model failures

## What Makes This Special

- **Real Data**: Top 100 companies by actual market cap, not static lists
- **Real AI**: Actual ML models, not rule-based chatbots
- **Performance**: Sub-second responses with intelligent caching
- **Always Fresh**: Auto-updating data every 6 hours
- **User Focused**: Natural language queries, company name recognition
- **Production Ready**: Scalable architecture, comprehensive error handling

## License

This project is available for educational and personal use. Please review the license file for detailed terms and conditions.

## Support & Questions

For questions, issues, or feature requests:
- Check the comprehensive API documentation at `/docs`
- Submit issues through the project repository
- Review existing documentation and examples
- Test with the provided API endpoints

---

**Ready to explore the financial markets with AI-powered insights!**