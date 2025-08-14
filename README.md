# Finance Assistant - Backend API

A clean, simple, and production-ready financial analysis API built with FastAPI.

## 🎯 Current Status: Backend Complete ✅

The backend API is complete and ready for production use. Frontend coming next!

## 🚀 Features

✅ **Stock Data**: Real-time stock prices and company information  
✅ **Technical Analysis**: RSI, Bollinger Bands, Moving Averages  
✅ **Fortune 500 Data**: Comprehensive company database  
✅ **AI Queries**: Natural language processing for financial questions  
✅ **Fast Caching**: In-memory caching for optimal performance  
✅ **Clean Architecture**: Modular, maintainable code structure  

## 🏁 Quick Start

1. **Install Dependencies**
   ```bash
   uv sync
   ```

2. **Start Backend API**
   ```bash
   python start_backend.py
   ```

3. **Access API Documentation**
   - Interactive Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

## 📋 API Endpoints

### Core
- `GET /` - Welcome message  
- `GET /health` - Health check

### Companies (Fortune 500)
- `GET /api/v1/companies/top` - Top companies
- `GET /api/v1/companies/search?q=apple` - Search companies  
- `GET /api/v1/companies/{name}` - Company details

### Technical Analysis
- `GET /api/v1/technical-analysis/{ticker}` - Complete analysis
- `GET /api/v1/technical-analysis/{ticker}/rsi` - RSI indicator
- `GET /api/v1/technical-analysis/{ticker}/bollinger-bands` - Bollinger Bands
- `GET /api/v1/technical-analysis/{ticker}/moving-averages` - Moving averages

### AI Queries
- `POST /api/v1/ai/query` - Process natural language queries
- `GET /api/v1/ai/examples` - Example queries

## 📁 Project Structure

```
Finance-Assistant/
├── start_backend.py              # Backend startup script  
├── backend/                      # Backend API
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── dependencies.py     # Service dependencies  
│   │   ├── models/
│   │   │   └── models.py        # Pydantic data models
│   │   ├── routers/             # API endpoints
│   │   │   ├── companies.py     # Fortune 500 endpoints
│   │   │   ├── technical_analysis.py  # Technical analysis
│   │   │   └── ai_queries.py    # AI query processing
│   │   └── services/            # Business logic
│   │       ├── yahoo_finance_service.py  # Stock data
│   │       ├── fortune500_service.py     # Company data  
│   │       ├── ai_query_processor.py     # AI processing
│   │       └── cache_service.py          # Caching layer
│   └── Dockerfile               # Docker configuration
├── data/                        # Reference data files
├── pyproject.toml              # Python dependencies
└── README.md                   # This file
```

## 🔧 Example API Calls

```bash
# Get Apple stock technical analysis
curl "http://localhost:8000/api/v1/technical-analysis/AAPL"

# Search for companies
curl "http://localhost:8000/api/v1/companies/search?q=Apple"

# Process AI query
curl -X POST "http://localhost:8000/api/v1/ai/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the price of Tesla?"}'

# Get Fortune 500 top companies
curl "http://localhost:8000/api/v1/companies/top"
```

## 🛠️ Technology Stack

- **FastAPI**: Modern Python web framework
- **yfinance**: Yahoo Finance data source
- **pandas**: Data manipulation and analysis  
- **pydantic**: Data validation and serialization
- **uvicorn**: ASGI server for production

## ✨ Code Quality

- ✅ **Clean Architecture**: Separated concerns with routers, services, and models
- ✅ **Type Hints**: Full type annotation throughout codebase
- ✅ **Error Handling**: Comprehensive error handling and validation
- ✅ **Documentation**: Clear docstrings and API documentation
- ✅ **Testing Ready**: Structure prepared for comprehensive testing

## 📈 Performance

- ✅ **Fast Response Times**: Optimized data processing
- ✅ **In-Memory Caching**: Quick data retrieval  
- ✅ **Async Support**: Non-blocking request handling
- ✅ **Production Ready**: Structured for scalability

## 🔜 Coming Next

- **React Frontend**: Modern UI with Vite build system
- **Docker Deployment**: Containerized frontend and backend
- **Docker Compose**: Full-stack development environment

## 📝 License

MIT License - Feel free to use for any purpose!
