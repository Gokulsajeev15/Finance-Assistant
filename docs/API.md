# API Documentation

## Overview

The Finance Assistant API provides real-time financial data, technical analysis, and AI-powered insights for stock market analysis.

**Base URL:** `http://localhost:8000`
**Documentation:** `http://localhost:8000/docs` (Swagger UI)

## Authentication

Currently, no authentication is required for API endpoints. The OpenAI integration requires an API key configured in the backend environment.

## Endpoints

### Health Check

#### GET `/`
Returns basic API information and health status.

**Response:**
```json
{
  "message": "Finance Assistant API",
  "status": "healthy",
  "version": "3.0.0"
}
```

### Companies

#### GET `/api/v1/companies/search`
Search for companies by name or ticker symbol.

**Parameters:**
- `q` (query string, required): Search term (company name or ticker)

**Example:**
```bash
curl "http://localhost:8000/api/v1/companies/search?q=apple"
```

**Response:**
```json
[
  {
    "rank": 0,
    "company": "Apple Inc.",
    "ticker": "AAPL",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "market_cap": 3550000000000,
    "employees": 150000,
    "revenue": "$408.6B",
    "profit": "$99.3B",
    "name": "Apple Inc."
  }
]
```

#### GET `/api/v1/companies/top`
Get top companies by market capitalization.

**Response:**
```json
[
  {
    "rank": 1,
    "company": "Apple Inc.",
    "ticker": "AAPL",
    "sector": "Technology",
    "market_cap": 3550000000000,
    "employees": 150000
  }
]
```

### Technical Analysis

#### GET `/api/v1/technical-analysis/{ticker}`
Get comprehensive technical analysis for a stock.

**Parameters:**
- `ticker` (path, required): Stock ticker symbol or company name

**Example:**
```bash
curl "http://localhost:8000/api/v1/technical-analysis/AAPL"
curl "http://localhost:8000/api/v1/technical-analysis/apple"
```

**Response:**
```json
{
  "ticker": "AAPL",
  "original_query": "apple",
  "last_updated": "2025-09-04T20:30:00.000000",
  "stock_data": {
    "ticker": "AAPL",
    "current_price": 230.45,
    "change": 2.15,
    "change_percent": 0.94,
    "volume": 45000000,
    "52_week_high": 235.00,
    "52_week_low": 180.00,
    "company_name": "Apple Inc.",
    "sector": "Technology",
    "market_cap": 3550000000000,
    "pe_ratio": 28.5,
    "dividend_yield": 0.51
  },
  "technical_data": {
    "rsi": {
      "value": 65.4,
      "interpretation": "Neutral - stock is neither expensive nor cheap"
    },
    "sma_20": 225.30,
    "sma_50": 220.15,
    "ema_12": 228.45,
    "ema_26": 224.30,
    "bollinger_bands": {
      "upper": 235.50,
      "middle": 225.30,
      "lower": 215.10
    },
    "trend": "Up"
  }
}
```

#### GET `/api/v1/technical-analysis/{ticker}/rsi`
Get only RSI (Relative Strength Index) for a stock.

**Response:**
```json
{
  "ticker": "AAPL",
  "rsi": {
    "value": 65.4,
    "interpretation": "Neutral - stock is neither expensive nor cheap"
  },
  "last_updated": "2025-09-04T20:30:00.000000"
}
```

#### GET `/api/v1/technical-analysis/{ticker}/basic`
Get basic stock information without technical indicators.

**Response:**
```json
{
  "ticker": "AAPL",
  "data": {
    "current_price": 230.45,
    "change": 2.15,
    "change_percent": 0.94,
    "volume": 45000000,
    "company_name": "Apple Inc."
  },
  "last_updated": "2025-09-04T20:30:00.000000"
}
```

### AI Assistant

#### POST `/api/v1/ai/chat`
Chat with the AI financial assistant.

**Request Body:**
```json
{
  "message": "What is the current trend for Apple stock?"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/ai/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the current trend for Apple stock?"}'
```

**Response:**
```json
{
  "response": "Based on the current technical analysis, Apple (AAPL) is showing an upward trend...",
  "timestamp": "2025-09-04T20:30:00.000000"
}
```

## Error Responses

All endpoints return structured error responses:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Codes

- **400 Bad Request**: Invalid parameters or data not available
- **404 Not Found**: Endpoint or resource not found  
- **422 Unprocessable Entity**: Invalid request format
- **500 Internal Server Error**: Server-side error

### Example Error Responses

**Company not found:**
```json
{
  "detail": "No data available for INVALIDTICKER. Company not found in our database of top 100 companies."
}
```

**AI service unavailable:**
```json
{
  "detail": "AI service temporarily unavailable. Please check your OpenAI API key configuration."
}
```

## Rate Limits

Currently, no rate limits are enforced, but the API depends on external services (Yahoo Finance, OpenAI) that may have their own rate limits.

## Data Sources

- **Stock Data**: Yahoo Finance via `yfinance` library
- **Company Information**: Real-time data from Yahoo Finance
- **AI Responses**: OpenAI GPT-4o mini
- **Company Database**: Top 100 companies by market capitalization

## Supported Company Search

The API supports flexible company search:

- **Direct ticker symbols**: AAPL, GOOGL, MSFT, etc.
- **Company names**: Apple, Google, Microsoft, etc.
- **Partial names**: "app" finds Apple, "micro" finds Microsoft
- **Common aliases**: 
  - "google" → "Alphabet Inc."
  - "facebook" → "Meta Platforms"
  - "tesla" → "Tesla Inc."

## Technical Indicators Explained

- **RSI (Relative Strength Index)**: 
  - Range: 0-100
  - >70: Overbought (potentially overvalued)
  - <30: Oversold (potentially undervalued)
  - 30-70: Neutral

- **Moving Averages**:
  - SMA 20: 20-day simple moving average
  - SMA 50: 50-day simple moving average
  - EMA 12/26: Exponential moving averages

- **Bollinger Bands**: 
  - Upper/Lower bands show volatility
  - Price touching upper band may indicate overbought condition
  - Price touching lower band may indicate oversold condition

- **Trend**: Overall price direction (Up/Down/Sideways)

## Notes

- All prices are in USD
- Market data is updated in real-time during market hours
- Technical indicators are calculated from the last 3 months of data
- Company database includes top 100 companies by market capitalization
