# Finance Assistant

A comprehensive financial analysis platform featuring **real AI-powered backend API** using Hugging Face models and a modern React frontend. The system provides real-time stock data, technical analysis, and intelligent financial insights through both a web interface and REST API.

## Key Features

- **Real AI Models**: Using actual machine learning models instead of rule-based systems
- **FinBERT Integration**: Financial sentiment analysis powered by ProsusAI/finbert
- **Advanced NLP**: Intent classification using Sentence Transformers
- **Smart Q&A**: Question answering with RoBERTa-based models
- **GPU Acceleration**: Automatic CUDA detection for faster AI processing

## Overview

Finance Assistant combines professional-grade financial analysis with cutting-edge AI capabilities. Users can analyze stocks using company names or ticker symbols, get detailed technical analysis reports, and interact with an AI assistant that truly understands natural language financial queries using real machine learning models.

<img width="1466" height="839" alt="Screenshot 2025-08-15 at 19 02 41" src="https://github.com/user-attachments/assets/2f110db2-5bfe-46ff-8ce2-7eba955b5bf5" />

## Key Features

### Frontend Application
- **Clean Interface**: Black and white design focused on data clarity
- **Company Search**: Browse and search Fortune 500 companies with detailed filtering
- **Technical Analysis**: Interactive charts and indicators with company name support
- **AI Assistant**: **Real AI-powered** natural language processing for financial questions
- **Real-time Data**: Live integration with financial data sources
- **Responsive Design**: Works seamlessly across desktop and mobile devices

### Backend API
- **Stock Data**: Real-time stock prices and comprehensive company information
- **Technical Analysis**: RSI, Bollinger Bands, Moving Averages, and trend analysis
- **Fortune 500 Database**: Complete company database with sector and industry data
- **AI Query Processing**: **Real machine learning models** for natural language understanding
- **High Performance**: In-memory caching and optimized data processing
- **Production Ready**: Scalable architecture with comprehensive error handling

<img width="1470" height="837" alt="Screenshot 2025-08-15 at 19 03 00" src="https://github.com/user-attachments/assets/24e433d8-2fb6-4d57-919c-1fb491f777f6" />

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

<img width="1470" height="837" alt="Screenshot 2025-08-15 at 19 03 19" src="https://github.com/user-attachments/assets/c7d5eade-600d-4b79-a705-334463b441c8" />

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn package manager
- **8GB+ RAM recommended** for AI model loading

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>     (ssh or https)
   cd Finance-Assistant
   ```

2. **Set up the backend**
   ```bash
   # Install Python dependencies (including AI models)
   uv sync
   
   # Start the backend server
   python start_backend.py
   ```

3. **Set up the frontend**
   ```bash
   # Navigate to frontend directory
   cd frontend
   
   # Install dependencies
   npm install
   
   # Start the development server
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Usage Examples

### Web Interface
The frontend provides three main sections accessible through clean tab navigation:

**Companies Tab**: Search and browse Fortune 500 companies with filters by sector, industry, and financial metrics.

**Technical Analysis Tab**: Enter company names or ticker symbols to get comprehensive technical analysis including price trends, RSI signals, moving averages, and Bollinger Bands.

**AI Assistant Tab**: Ask questions in natural language - now powered by **real AI models**:
- "Analyze Apple's performance"
- "Technical analysis of Tesla" 
- "How is Microsoft doing?"
- "What's Amazon's revenue?"
- "Explain diversification"
- "What is compound interest?"

### API Usage
```bash
# Get comprehensive company analysis
curl "http://localhost:8000/api/v1/technical-analysis/AAPL"

# Search companies by name or sector
curl "http://localhost:8000/api/v1/companies/search?q=technology"

# Process natural language queries with AI
curl -X POST "http://localhost:8000/api/v1/ai/query?query=Analyze Tesla performance"

# Get Fortune 500 top companies
curl "http://localhost:8000/api/v1/companies/top"
```

## API Endpoints

### Core Endpoints
- `GET /` - Application welcome message
- `GET /health` - System health check and status

### Company Data
- `GET /api/v1/companies/top` - Fortune 500 top companies
- `GET /api/v1/companies/search?q={query}` - Search companies by name, sector, or industry
- `GET /api/v1/companies/{name}` - Detailed company information
- `GET /api/v1/companies/sector/{sector}` - Companies by sector

### Technical Analysis
- `GET /api/v1/technical-analysis/{ticker}` - Complete technical analysis
- `GET /api/v1/technical-analysis/{ticker}/rsi` - RSI indicator analysis
- `GET /api/v1/technical-analysis/{ticker}/bollinger-bands` - Bollinger Bands data
- `GET /api/v1/technical-analysis/{ticker}/moving-averages` - Moving averages analysis

### AI Processing
- `POST /api/v1/ai/query` - Process natural language financial queries using **real AI models**
- `GET /api/v1/ai/examples` - Get example queries and usage patterns

## Project Structure

```
Finance-Assistant/
├── start_backend.py              # Backend startup script
├── backend/                      # FastAPI backend application
│   ├── app/
│   │   ├── main.py              # Main FastAPI application
│   │   ├── dependencies.py     # Service dependency injection
│   │   ├── models/
│   │   │   └── models.py        # Pydantic data models
│   │   ├── routers/             # API route handlers
│   │   │   ├── companies.py     # Fortune 500 company endpoints
│   │   │   ├── technical_analysis.py  # Technical analysis endpoints
│   │   │   └── ai_queries.py    # AI query processing endpoints
│   │   └── services/            # Business logic services
│   │       ├── stock_data_service.py     # Enhanced stock data service
│   │       ├── company_database.py      # Company database service
│   │       ├── huggingface_ai.py        # **Real AI models** (FinBERT, RoBERTa, Sentence Transformers)
│   │       └── data_cache.py           # Caching layer
│   └── Dockerfile               # Docker containerization
├── frontend/                     # React frontend application
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── AppHeader.jsx    # Application header
│   │   │   ├── CompanySearchBar.jsx    # Search functionality
│   │   │   ├── CompanyInfoCard.jsx  # Company display cards
│   │   │   ├── StockAnalysisPanel.jsx  # Technical analysis interface
│   │   │   └── FinancialChatbot.jsx   # **AI assistant interface**
│   │   ├── services/
│   │   │   └── financial_api_client.js # API service layer
│   │   ├── App.jsx              # Main application component
│   │   ├── main.jsx             # Application entry point
│   │   └── index.css            # Global styles
│   ├── package.json             # Frontend dependencies
│   ├── vite.config.js           # Vite build configuration
│   └── tailwind.config.js       # Tailwind CSS configuration
├── data/                         # Reference data files
│   └── fortune_500_2024.pdf     # Fortune 500 dataset
├── pyproject.toml               # Python dependencies (including AI libraries)
└── README.md                    # Project documentation
```

## Features in Detail

### Intelligent Company Recognition
The system recognizes over 70 company names and variations, allowing users to type natural names instead of remembering ticker symbols:
- "Apple" automatically maps to AAPL
- "Tesla" automatically maps to TSLA
- "Microsoft" automatically maps to MSFT
- "Warren Buffett" automatically maps to Berkshire Hathaway

### Advanced Technical Analysis
Comprehensive technical analysis includes:
- **RSI Analysis**: 14-day Relative Strength Index with overbought/oversold signals
- **Moving Averages**: SMA 20/50 and EMA 12/26 with trend analysis
- **Bollinger Bands**: Upper, middle, and lower bands with position analysis
- **Price Analysis**: 6-month range positioning and volume analysis
- **Market Context**: Market cap categorization and sector information

### **AI-Powered Insights**
The AI assistant uses **real machine learning models** for detailed, context-aware responses:
- **Intent Classification**: Automatically understands question types using Sentence Transformers
- **Sentiment Analysis**: Analyzes financial sentiment using FinBERT
- **Smart Question Answering**: Handles complex queries using RoBERTa
- **Analysis Reports**: Comprehensive company analysis with technical insights
- **Performance Metrics**: Financial performance with market context
- **Technical Summaries**: Detailed technical analysis with actionable signals
- **Natural Language**: Truly understands questions in plain English

## Development

### Running in Development Mode
```bash
# Backend development (with AI models)
python start_backend.py

# Frontend development
cd frontend
npm run dev
```

### Building for Production
```bash
# Frontend production build
cd frontend
npm run build

# Backend production deployment
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

### **AI Model Management**
```bash
# Models are automatically downloaded on first run
# GPU acceleration is automatically detected
# Fallback to CPU if CUDA is unavailable
```

### Code Quality Standards
- **Type Safety**: Full TypeScript-style type hints in Python
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Clean Architecture**: Separation of concerns with clear module boundaries
- **Documentation**: Extensive inline documentation and API specs
- **Performance**: Optimized queries and efficient data processing
- **AI Integration**: Robust fallback handling for AI model failures

## API Response Examples

### Technical Analysis Response
```json
{
  "success": true,
  "ticker": "AAPL",
  "company_name": "Apple Inc.",
  "sector": "Technology",
  "indicators": {
    "rsi": {
      "current": 67.08,
      "interpretation": "Neutral"
    },
    "moving_averages": {
      "sma_20": 216.59,
      "sma_50": 209.36,
      "ema_12": 223.27,
      "ema_26": 217.13
    },
    "bollinger_bands": {
      "upper": 237.22,
      "middle": 216.59,
      "lower": 195.97
    }
  },
  "price_data": {
    "current_price": 230.89,
    "high_6m": 249.39,
    "low_6m": 168.80,
    "volume_avg": 58415211
  }
}
```

### **AI Query Response**
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

## **Performance & Requirements**

### **AI Model Loading**
- **First Run**: Models are downloaded (~2-3GB total)
- **Memory Usage**: ~4-6GB RAM for all AI models
- **GPU Support**: Automatic CUDA detection for 10x+ speed improvement
- **Fallback**: Graceful degradation to rule-based responses if models fail

### **System Requirements**
- **Minimum**: 8GB RAM, Python 3.11+
- **Recommended**: 16GB RAM, CUDA-capable GPU
- **Storage**: 5GB+ free space for models and data

## Contributing

This project follows clean architecture principles and maintains high code quality standards. When contributing:

1. Follow the existing code structure and naming conventions
2. Add appropriate type hints and documentation
3. Include error handling for new features
4. Test both frontend and backend integration
5. Maintain the clean, professional design aesthetic
6. **Test AI model integration** and fallback scenarios

## License

This project is available for educational and personal use. Please review the license file for detailed terms and conditions.

## Support

For questions, issues, or feature requests, please refer to the project documentation or submit an issue through the appropriate channels.


