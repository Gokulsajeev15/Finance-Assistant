# Finance Assistant

A comprehensive financial analysis platform featuring an AI-powered backend API and modern React frontend. The system provides real-time stock data, technical analysis, and intelligent financial insights through both a web interface and REST API.

## Overview

Finance Assistant combines professional-grade financial analysis with an intuitive user interface. Users can analyze stocks using company names or ticker symbols, get detailed technical analysis reports, and interact with an AI assistant that understands natural language financial queries.

<img width="1466" height="839" alt="Screenshot 2025-08-15 at 19 02 41" src="https://github.com/user-attachments/assets/2f110db2-5bfe-46ff-8ce2-7eba955b5bf5" />



## Key Features

### Frontend Application
- **Clean Interface**: Black and white design focused on data clarity
- **Company Search**: Browse and search Fortune 500 companies with detailed filtering
- **Technical Analysis**: Interactive charts and indicators with company name support
- **AI Assistant**: Natural language processing for financial questions
- **Real-time Data**: Live integration with financial data sources
- **Responsive Design**: Works seamlessly across desktop and mobile devices

### Backend API
- **Stock Data**: Real-time stock prices and comprehensive company information
- **Technical Analysis**: RSI, Bollinger Bands, Moving Averages, and trend analysis
- **Fortune 500 Database**: Complete company database with sector and industry data
- **AI Query Processing**: Advanced natural language understanding for financial queries
- **High Performance**: In-memory caching and optimized data processing
- **Production Ready**: Scalable architecture with comprehensive error handling

<img width="1470" height="837" alt="Screenshot 2025-08-15 at 19 03 00" src="https://github.com/user-attachments/assets/24e433d8-2fb6-4d57-919c-1fb491f777f6" />


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

<img width="1470" height="837" alt="Screenshot 2025-08-15 at 19 03 19" src="https://github.com/user-attachments/assets/c7d5eade-600d-4b79-a705-334463b441c8" />


## Getting Started

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>     (ssh or https)
   cd Finance-Assistant
   ```

2. **Set up the backend**
   ```bash
   # Install Python dependencies
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

**AI Assistant Tab**: Ask questions in natural language such as:
- "Analyze Apple's performance"
- "Technical analysis of Tesla" 
- "How is Microsoft doing?"
- "What's Amazon's revenue?"

### API Usage
```bash
# Get comprehensive company analysis
curl "http://localhost:8000/api/v1/technical-analysis/AAPL"

# Search companies by name or sector
curl "http://localhost:8000/api/v1/companies/search?q=technology"

# Process natural language queries
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
- `POST /api/v1/ai/query` - Process natural language financial queries
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
│   │       ├── yahoo_finance_clean.py     # Enhanced stock data service
│   │       ├── fortune500_service.py      # Company database service
│   │       ├── ai_query_processor.py      # AI query processing
│   │       └── cache_service.py           # Caching layer
│   └── Dockerfile               # Docker containerization
├── frontend/                     # React frontend application
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── Header.jsx       # Application header
│   │   │   ├── SearchBar.jsx    # Search functionality
│   │   │   ├── CompanyCard.jsx  # Company display cards
│   │   │   ├── TechnicalAnalysis.jsx  # Technical analysis interface
│   │   │   └── AIChat.jsx       # AI assistant interface
│   │   ├── services/
│   │   │   └── api.js           # API service layer
│   │   ├── App.jsx              # Main application component
│   │   ├── main.jsx             # Application entry point
│   │   └── index.css            # Global styles
│   ├── package.json             # Frontend dependencies
│   ├── vite.config.js           # Vite build configuration
│   └── tailwind.config.js       # Tailwind CSS configuration
├── data/                         # Reference data files
│   └── fortune_500_2024.pdf     # Fortune 500 dataset
├── pyproject.toml               # Python dependencies
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

### AI-Powered Insights
The AI assistant provides detailed, context-aware responses:
- **Analysis Reports**: Comprehensive company analysis with technical insights
- **Performance Metrics**: Financial performance with market context
- **Technical Summaries**: Detailed technical analysis with actionable signals
- **Natural Language**: Understands questions in plain English

## Development

### Running in Development Mode
```bash
# Backend development
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

### Code Quality Standards
- **Type Safety**: Full TypeScript-style type hints in Python
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Clean Architecture**: Separation of concerns with clear module boundaries
- **Documentation**: Extensive inline documentation and API specs
- **Performance**: Optimized queries and efficient data processing

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

### AI Query Response
```json
{
  "type": "analysis",
  "ticker": "AAPL",
  "message": "COMPREHENSIVE COMPANY ANALYSIS\n\nCOMPANY OVERVIEW:\nName: Apple Inc.\nTicker: AAPL\nSector: Technology\n\nCURRENT TRADING DATA:\nCurrent Price: $230.89\nDaily Change: $-1.77 (-0.76%)\n\nTECHNICAL INDICATORS:\nRSI (14-day): 67.08\nRSI Signal: NEUTRAL (No strong directional bias)\nTrend: BULLISH (SMA20 above SMA50)"
}
```

## Contributing

This project follows clean architecture principles and maintains high code quality standards. When contributing:

1. Follow the existing code structure and naming conventions
2. Add appropriate type hints and documentation
3. Include error handling for new features
4. Test both frontend and backend integration
5. Maintain the clean, professional design aesthetic

## License

This project is available for educational and personal use. Please review the license file for detailed terms and conditions.

## Support

For questions, issues, or feature requests, please refer to the project documentation or submit an issue through the appropriate channels.
