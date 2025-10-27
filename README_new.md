# Finance Assistant

A modern, AI-powered financial analysis application that provides real-time stock data, technical analysis, and intelligent financial insights.

## Features

- **Real-time Stock Data**: Live prices, market data, and company information for top 100 companies
- **Technical Analysis**: RSI, moving averages, Bollinger bands, and trend analysis
- **AI Financial Assistant**: Powered by OpenAI GPT-4o mini for intelligent insights
- **Smart Company Search**: Search by company name or ticker symbol with intelligent aliases
- **Modern UI**: Clean, responsive React frontend
- **Fast API**: High-performance FastAPI backend

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

This will start both backend (port 8000) and frontend (port 5173) servers.

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
- `GET /api/v1/companies/top` - Get top companies by market cap

### Technical Analysis
- `GET /api/v1/technical-analysis/{ticker}` - Full technical analysis
- `GET /api/v1/technical-analysis/{ticker}/rsi` - RSI indicator only
- `GET /api/v1/technical-analysis/{ticker}/basic` - Basic stock info only

### AI Assistant
- `POST /api/v1/ai/chat` - Chat with AI financial assistant

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
├── docs/                   # Documentation
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
curl -X POST "http://localhost:8000/api/v1/ai/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the current trend for Apple stock?"}'
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
- Search by company name: "apple", "google", "microsoft"
- Search by ticker: "AAPL", "GOOGL", "MSFT"  
- Smart aliases: "facebook" → "Meta", "google" → "Alphabet"
- Covers top 100 companies by market cap

### Technical Analysis
- **RSI**: Relative Strength Index for overbought/oversold signals
- **Moving Averages**: 20-day and 50-day simple moving averages
- **Bollinger Bands**: Price volatility and trend indicators
- **Trend Analysis**: Current market trend direction

### AI Assistant
- Real-time financial insights powered by OpenAI GPT-4o mini
- Contextual understanding of market data
- Personalized investment guidance
- Market trend explanations

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

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test: `./manage.sh test`
5. Commit: `git commit -m "Add feature"`
6. Push: `git push origin feature-name`
7. Submit a pull request

## License

This project is licensed under the MIT License.

## Troubleshooting

**Backend won't start:**
- Check if port 8000 is free: `lsof -i :8000`
- Verify Python dependencies: `uv sync`
- Check environment variables in `.env`

**Frontend won't start:**
- Check if port 5173 is free: `lsof -i :5173`
- Install dependencies: `cd frontend && npm install`
- Check Node.js version: `node --version` (should be 18+)

**API tests fail:**
- Ensure backend is running: `curl http://localhost:8000/docs`
- Check OpenAI API key is valid
- Verify internet connection for stock data

**Need help?**
- Check the [API documentation](http://localhost:8000/docs) when running locally
- Review logs in the terminal
- Run `./manage.sh test` to verify system health

---

**Happy investing!**
