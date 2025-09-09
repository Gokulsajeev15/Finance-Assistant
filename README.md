# Finance Assistant

A modern, AI-powered financial analysis application that provides real-time stock data, technical analysis, and intelligent financial insights.

## Features

- **Real-time Stock Data**: Live prices, market data, and company information for 100 major companies by market cap
- **Technical Analysis**: RSI, moving averages, Bollinger bands, and trend analysis with smart interpretations
- **AI Financial Assistant**: Powered by OpenAI GPT-4o mini with real-time data integration
- **Dynamic Company Search**: Searches curated database of 100 major stocks with intelligent name matching
- **Smart Technical Indicators**: Oversold/overbought signals, trend analysis, and trading insights
- **Modern UI**: Clean, responsive React frontend with real-time updates
- **Fast API**: High-performance FastAPI backend with comprehensive documentation

<img width="1470" height="840" alt="Screenshot 2025-09-04 at 20 54 43" src="https://github.com/user-attachments/assets/f134149b-e6d3-4b87-937a-203d75dbcbf6" />

<img width="1470" height="756" alt="Screenshot 2025-09-04 at 22 14 59" src="https://github.com/user-attachments/assets/c8f83505-2d0d-4ebe-9d02-2deead566fe7" />


<img width="1462" height="829" alt="Screenshot 2025-09-04 at 21 54 43" src="https://github.com/user-attachments/assets/c23e9b4a-8110-4cfc-837b-226585f6fa30" />


## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.11+**: Latest Python features and performance
- **yfinance**: Real-time financial data from Yahoo Finance
- **OpenAI API**: GPT-4o mini for intelligent responses
- **Pydantic**: Data validation and serialization

### Frontend
- **React 18**: Modern React with hooks
- **Vite**: Lightning-fast development and build tool
- **TailwindCSS**: Utility-first CSS framework
- **Modern JavaScript**: ES6+ features

## Quick Start

### Prerequisites
- **Python 3.11+**
- **Node.js 18+**
- **uv** (Python package manager) - Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **OpenAI API Key** (for AI features) - Get from [OpenAI Platform](https://platform.openai.com/api-keys)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Finance-Assistant
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Start development environment**
   ```bash
   ./manage.sh dev
   ```

This will start both backend (port 8000) and frontend (port 3001) servers.

## Management Commands

Use the `./manage.sh` script for all project management:

```bash
./manage.sh dev     # Start development environment (recommended)
./manage.sh start   # Start backend only
./manage.sh stop    # Stop all services
./manage.sh test    # Test all API endpoints
./manage.sh clean   # Clean cache and temporary files
./manage.sh build   # Build frontend for production
./manage.sh help    # Show all commands
```

## API Endpoints

### Companies
- `GET /api/v1/companies/search?q={query}` - Search companies by name or ticker

### Technical Analysis
- `GET /api/v1/technical-analysis/{ticker}` - Full technical analysis (supports company names and tickers)

### AI Assistant
- `POST /api/v1/ai/query?query={message}` - Query AI with financial questions

### Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## Project Structure

```
Finance-Assistant/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── models/         # Pydantic data models
│   │   ├── routers/        # API route handlers
│   │   │   ├── companies.py    # Company search endpoints
│   │   │   ├── technical.py    # Technical analysis endpoints
│   │   │   └── ai.py           # AI chat endpoints
│   │   ├── services/       # Business logic
│   │   │   ├── companies.py    # Company data service
│   │   │   ├── stock_data.py   # Stock data service
│   │   │   └── ai.py           # OpenAI integration
│   │   ├── dependencies.py # Dependency injection
│   │   └── main.py         # FastAPI application
│   └── tests/              # Backend tests
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── api_services/   # API client
│   │   └── App.jsx         # Main application
│   └── dist/               # Production build (generated)
├── .env.example           # Environment template
├── manage.sh              # Project management script (main entry point)
├── start_backend.py       # Backend startup script
└── README.md              # This file
```

## Development

### Using the Management Script (Recommended)
```bash
./manage.sh dev    # Start both frontend and backend
```

### Manual Development
**Backend:**
```bash
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Adding New Features
1. **API Endpoints**: Add routes in `backend/app/routers/`
2. **Business Logic**: Add services in `backend/app/services/`
3. **UI Components**: Add components in `frontend/src/components/`
4. **Data Models**: Add models in `backend/app/models/`

## Example Usage

**Search for any company:**
```bash
curl "http://localhost:8000/api/v1/companies/search?q=CSX"
# Returns: CSX Corporation, ticker: CSX, railroads industry
```

**Get real-time technical analysis:**
```bash
curl "http://localhost:8000/api/v1/technical-analysis/CSX"
# Returns: Current price $32.66, RSI 20.65 (oversold), uptrend
```

**Ask AI about any stock:**
```bash
curl -X POST "http://localhost:8000/api/v1/ai/query?query=Analyze%20CSX%20performance"
# Returns: Real-time analysis with current price, technical indicators, and insights
```

**The AI automatically recognizes companies and provides real-time data:**
- "What about Johnson & Johnson?" → Gets live JNJ data ($178.76, $430B market cap)
- "How is CSX doing?" → Gets live CSX data ($32.66, RSI 20.65 oversold)
- "Compare Apple and Microsoft" → Gets both AAPL and MSFT real-time data

## Testing

**Test all APIs:**
```bash
./manage.sh test
```

**Manual API testing:**
```bash
# Company search
curl "http://localhost:8000/api/v1/companies/search?q=apple"

# Technical analysis
curl "http://localhost:8000/api/v1/technical-analysis/AAPL"

# AI chat
curl -X POST "http://localhost:8000/api/v1/ai/query?query=What%20is%20the%20current%20trend%20for%20Apple%20stock?"
```

## Production Deployment

1. **Build frontend**
   ```bash
   ./manage.sh build
   ```

2. **Configure production environment**
   ```env
   OPENAI_API_KEY=your_production_api_key
   OPENAI_MODEL=gpt-4o-mini
   ```

3. **Run production backend**
   ```bash
   uv run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
   ```

## Environment Variables

Create `.env` file with:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (defaults provided)
OPENAI_MODEL=gpt-4o-mini
```

## Key Features Explained

### Smart Company Search
- Search from 100 major companies: "CSX", "Johnson & Johnson", "Berkshire Hathaway"
- Search by ticker: "AAPL", "GOOGL", "MSFT", "CSX"
- Intelligent name matching with 15+ company aliases (Google→GOOGL, Facebook→META)
- Exact ticker matching and fuzzy company name search

### Technical Analysis
- **RSI**: Relative Strength Index with smart interpretations (oversold/overbought signals)
- **Moving Averages**: 20-day and 50-day SMA with trend analysis
- **Bollinger Bands**: Price volatility and mean reversion indicators
- **Trend Analysis**: Current market trend direction with actionable insights
- **Real-time Data**: All indicators calculated from live market data

### AI Assistant
- Real-time financial insights powered by OpenAI GPT-4o mini
- Dynamic company recognition - analyzes any mentioned stock
- Integrates live market data into AI responses
- No generic responses - always uses current market conditions
- Contextual understanding of technical indicators
- Personalized investment guidance based on real data

## Recent Improvements

- **Dynamic Company Recognition**: AI now automatically finds any company you mention
- **Real-time Data Integration**: All AI responses use current market data
- **Smart Technical Analysis**: RSI interpretations, trend analysis with actionable insights  
- **Unified Management**: Single `manage.sh` script for all operations
- **Clean Architecture**: Organized codebase with clear separation of concerns
- **Comprehensive Documentation**: Updated API docs and user guides

## Maintenance

**Clean project:**
```bash
./manage.sh clean
```

**Stop all services:**
```bash
./manage.sh stop
```

**View logs:**
- Backend logs appear in terminal where `./manage.sh dev` is running
- Frontend logs appear in browser console
