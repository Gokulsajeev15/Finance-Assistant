# Project Architecture

## Overview

Finance Assistant is a modern full-stack financial analysis application built with FastAPI and React. The application provides real-time stock data, technical analysis, and AI-powered financial insights.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Finance Assistant                        │
├─────────────────────┬───────────────────────────────────────┤
│      Frontend       │             Backend                   │
│      (React)        │            (FastAPI)                  │
├─────────────────────┼───────────────────────────────────────┤
│                     │                                       │
│  ┌─────────────┐    │  ┌─────────────┐ ┌─────────────────┐  │
│  │ Components  │    │  │   Routers   │ │    Services     │  │
│  │  - Chat     │◄───┼──┤  - AI       │ │  - AI           │  │
│  │  - Search   │    │  │  - Companies│ │  - Companies    │  │
│  │  - Analysis │    │  │  - Technical│ │  - Stock Data   │  │
│  └─────────────┘    │  └─────────────┘ └─────────────────┘  │
│                     │         │                │            │
│  ┌─────────────┐    │         ▼                ▼            │
│  │ API Client  │◄───┼──── FastAPI App ──── Dependencies ────┤
│  └─────────────┘    │                                       │
└─────────────────────┼───────────────────────────────────────┘
                      │
           ┌──────────┴──────────┐
           ▼                     ▼
    ┌─────────────┐      ┌─────────────┐
    │ Yahoo       │      │ OpenAI      │
    │ Finance     │      │ GPT-4o-mini │
    │ (yfinance)  │      │ API         │
    └─────────────┘      └─────────────┘
```

## Backend Architecture

### FastAPI Application (`backend/app/`)

```
backend/app/
├── main.py              # FastAPI application setup
├── dependencies.py      # Dependency injection
├── models/
│   └── models.py       # Pydantic data models
├── routers/            # API endpoint handlers
│   ├── ai.py          # AI chat endpoints
│   ├── companies.py   # Company search endpoints
│   └── technical.py   # Technical analysis endpoints
└── services/          # Business logic layer
    ├── ai.py         # OpenAI integration
    ├── companies.py  # Company data management
    └── stock_data.py # Stock market data
```

### Key Components

#### 1. **Routers** (API Endpoints)
- **companies.py**: Company search and listing
- **technical.py**: Stock analysis and technical indicators
- **ai.py**: AI-powered financial chat

#### 2. **Services** (Business Logic)
- **companies.py**: Manages top 100 companies database
- **stock_data.py**: Real-time stock data from Yahoo Finance
- **ai.py**: OpenAI GPT-4o-mini integration

#### 3. **Models** (Data Structures)
- **models.py**: Pydantic models for API request/response validation

#### 4. **Dependencies** (Dependency Injection)
- **dependencies.py**: Service instantiation and dependency management

## Frontend Architecture

### React Application (`frontend/src/`)

```
frontend/src/
├── App.jsx             # Main application component
├── main.jsx           # React application entry point
├── index.css          # Global styles (Tailwind)
├── components/        # React components
│   ├── AppHeader.jsx         # Application header
│   ├── CompanyInfoCard.jsx   # Company information display
│   ├── CompanySearchBar.jsx  # Company search interface
│   ├── FinancialChatbot.jsx  # AI chat interface
│   └── StockAnalysisPanel.jsx # Technical analysis display
└── api_services/      # API communication
    └── financial_api_client.js # Backend API client
```

### Key Components

#### 1. **Components**
- **AppHeader**: Navigation and branding
- **CompanySearchBar**: Smart company search with autocomplete
- **CompanyInfoCard**: Company information display
- **StockAnalysisPanel**: Technical analysis visualization
- **FinancialChatbot**: AI-powered chat interface

#### 2. **API Services**
- **financial_api_client.js**: Centralized API communication

## Data Flow

### 1. Company Search Flow
```
User Input → SearchBar → API Client → Companies Router → 
Companies Service → Yahoo Finance → Database Cache → Response
```

### 2. Technical Analysis Flow
```
Ticker/Name → Technical Router → Stock Data Service → 
Yahoo Finance API → Technical Calculations → Formatted Response
```

### 3. AI Chat Flow
```
User Message → Chatbot → AI Router → AI Service → 
OpenAI API → Context + Real-time Data → AI Response
```

## Key Features Implementation

### 1. **Smart Company Search**
- **Alias Mapping**: Common names (google → Alphabet)
- **Partial Matching**: Flexible search algorithm
- **Priority Ranking**: Exact matches first
- **Caching**: In-memory company database

### 2. **Technical Analysis**
- **RSI Calculation**: 14-period relative strength index
- **Moving Averages**: SMA 20/50, EMA 12/26
- **Bollinger Bands**: Price volatility indicators
- **Trend Detection**: Price direction analysis

### 3. **AI Integration**
- **Context Awareness**: Real-time market data context
- **Financial Expertise**: GPT-4o-mini with financial prompting
- **Response Formatting**: Structured financial advice

## External Dependencies

### Data Sources
- **Yahoo Finance**: Real-time stock data via `yfinance`
- **OpenAI**: AI responses via GPT-4o-mini API

### Core Libraries
- **FastAPI**: Web framework and API documentation
- **React**: Frontend user interface
- **Pydantic**: Data validation and serialization
- **TailwindCSS**: Utility-first styling

## Deployment Architecture

### Development
```
./manage.sh dev
├── Backend: localhost:8000
└── Frontend: localhost:5173
```

### Production
```
Backend: FastAPI + Uvicorn
Frontend: Static files (npm run build)
```

## Security Considerations

1. **API Keys**: Environment variable management
2. **CORS**: Configured for development origins
3. **Input Validation**: Pydantic model validation
4. **Rate Limiting**: Dependent on external APIs

## Performance Optimizations

1. **Caching**: In-memory company database
2. **Async Operations**: FastAPI async endpoints
3. **Batch Processing**: Concurrent API calls
4. **Response Compression**: FastAPI automatic compression

## Monitoring and Logging

1. **Application Logs**: Python logging module
2. **API Documentation**: Auto-generated Swagger UI
3. **Health Checks**: Basic health endpoint
4. **Error Handling**: Structured error responses

This architecture provides a scalable, maintainable foundation for financial analysis applications with clear separation of concerns and modern development practices.
