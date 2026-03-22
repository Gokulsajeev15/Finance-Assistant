# Architecture

## Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Frontend | React 18 + Vite + TailwindCSS     |
| Backend  | FastAPI (Python 3.11+)            |
| Data     | yfinance (Yahoo Finance)          |
| AI       | OpenAI GPT-4o-mini                |

---

## Directory Structure

```
Finance-Assistant/
├── backend/app/
│   ├── main.py              # FastAPI app, CORS, router mounting
│   ├── dependencies.py      # Singleton service instances + Depends() providers
│   ├── models/
│   │   └── models.py        # Pydantic request/response models
│   ├── routers/
│   │   ├── companies.py     # GET /api/v1/companies/...
│   │   ├── technical.py     # GET /api/v1/technical-analysis/...
│   │   └── ai.py            # POST /api/v1/ai/query
│   └── services/
│       ├── companies.py     # In-memory company cache, yfinance fetching
│       ├── stock_data.py    # Live price + technical indicator calculations
│       └── ai.py            # OpenAI integration, ticker extraction, prompt building
├── frontend/src/
│   ├── App.jsx                          # Root component, 3-tab layout
│   ├── api_services/
│   │   └── financial_api_client.js      # Axios client, all API calls
│   └── components/
│       ├── AppHeader.jsx
│       ├── CompanySearchBar.jsx
│       ├── CompanyInfoCard.jsx
│       ├── StockAnalysisPanel.jsx       # Technical analysis tab
│       └── FinancialChatbot.jsx         # AI chat tab
└── docs/
    ├── ARCHITECTURE.md      # This file
    └── API.md               # Endpoint reference
```

---

## Backend

### `main.py`
Creates the FastAPI app, enables CORS for `localhost:3000` and `localhost:5173`, then mounts the three routers. Has a `/health` endpoint that checks whether `OPENAI_API_KEY` is set.

### `dependencies.py`
Creates three **singleton** service instances at startup and exposes them via FastAPI's `Depends()` system:

```python
company_service  = SimpleCompanyService()
stock_service    = SimpleStockService()
ai_service       = OpenAIFinancialAI(stock_service, company_service)
```

Because these are module-level singletons, all requests share the same instances — which is how the 6-hour company cache works.

---

### Services

#### `services/stock_data.py` → `SimpleStockService`
Wraps `yfinance` to pull live stock data. All methods are **synchronous** — they block the event loop when called from async routes (this gets fixed in Phase 1 with Alpaca).

| Method | What it does |
|--------|-------------|
| `get_stock_data(ticker)` | Pulls last 5 days of price history. Returns current price, daily change, volume, P/E, market cap. |
| `get_technical_indicators(ticker)` | Pulls 3 months of history. Computes RSI (14-period), SMA 20/50, EMA 12/26, Bollinger Bands (20-period, 2σ). |
| `_calculate_rsi(prices)` | Standard RSI formula: diff → separate gains/losses → rolling avg → `100 - (100 / (1 + RS))`. Returns 50 on failure as a neutral fallback. |

#### `services/companies.py` → `SimpleCompanyService`
Maintains an **in-memory cache** of 100 companies, refreshed every 6 hours.

- `__init__` defines a hardcoded list of 100 tickers (the universe to fetch from).
- On first request, `_ensure_fresh()` triggers `update_companies()`, which calls `_fetch_all()`.
- `_fetch_all()` uses `asyncio.gather` + `ThreadPoolExecutor` to fetch all 100 tickers from yfinance in parallel.
- Results are sorted by market cap and the top 100 are cached in `self.companies`.
- `search_companies(term)` does fuzzy matching against the cache with an alias map (e.g. `"google"` → `"alphabet"`). Prioritizes exact ticker matches, then exact name matches, then partial matches.
- `get_company_by_ticker(ticker)` checks the cache first, then falls back to a direct yfinance fetch for tickers outside the top 100.

#### `services/ai.py` → `OpenAIFinancialAI`
The current AI layer is a **"fetch-everything-then-prompt"** pattern — it pre-fetches data before the LLM sees anything. This gets replaced with true tool-calling in Phase 1.

Request flow:
```
question
  → _extract_tickers()   # scan for uppercase words + company indicators, search each
  → _fetch_financial_data()  # call stock_service + company_service for each ticker
  → _build_prompt()      # concatenate question + all fetched data into one string
  → OpenAI API (gpt-4o-mini, temp=0.3)
  → _classify()          # keyword-based response type labeling
  → return dict
```

`_extract_tickers` is a heuristic — it looks for uppercase 2–5 char words (likely tickers) and words adjacent to company indicators like "Inc" or "Corp". This is imprecise and gets replaced by LLM tool-calling in Phase 1.

---

### Routers

#### `routers/companies.py`
| Endpoint | Handler |
|----------|---------|
| `GET /api/v1/companies/top?limit=20` | Returns top N from cache |
| `GET /api/v1/companies/search?q=...` | Fuzzy search |
| `GET /api/v1/companies/cache/info` | Cache metadata |
| `GET /api/v1/companies/{name}` | Ticker lookup, falls back to search |

#### `routers/technical.py`
| Endpoint | Handler |
|----------|---------|
| `GET /api/v1/technical-analysis/{ticker}` | Full analysis: price + all indicators |
| `GET /api/v1/technical-analysis/{ticker}/rsi` | RSI only |
| `GET /api/v1/technical-analysis/{ticker}/basic` | Price data only |

The main `/{ticker}` route tries the ticker directly first. If that fails, it searches the company cache to resolve a company name to its ticker symbol.

#### `routers/ai.py`
| Endpoint | Handler |
|----------|---------|
| `POST /api/v1/ai/query?query=...` | Calls `ai_service.process_query()` — note: query is a URL param, not request body |
| `GET /api/v1/ai/examples` | Returns hardcoded example questions |
| `GET /api/v1/ai/health` | Fires a test query to verify the service is alive |

---

## Frontend

### `App.jsx`
Shell component. Holds the 3-tab layout (Companies / Technical Analysis / AI Assistant). Owns the `companies` state and the search/load handlers — passes them down to `CompanySearchBar` and `CompanyInfoCard`.

### `api_services/financial_api_client.js`
Single axios instance pointing to `http://localhost:8000`. All API calls are named functions exported as `financeAPI`. Components import this and call it directly.

### `FinancialChatbot.jsx`
Stateless chat UI — messages are stored in local `useState` and are lost on page refresh. Each message is an independent API call with no session context (no memory). This gets replaced with PostgreSQL-backed sessions in Phase 1.

### `StockAnalysisPanel.jsx`
Ticker input that calls `getTechnicalAnalysis()`. Displays RSI, SMA 20/50, EMA 12/26, Bollinger Bands. If the ticker fails, it tries `searchCompanies()` to resolve a name to a ticker, then retries.

---

## Data Flow

### Company Browse
```
App mounts → loadTopCompanies() → GET /api/v1/companies/top
           → SimpleCompanyService.get_top_companies()
           → _ensure_fresh() → yfinance (parallel, 100 tickers)
           → sorted by market_cap → cached → returned
```

### Technical Analysis
```
User types ticker → StockAnalysisPanel → GET /api/v1/technical-analysis/{ticker}
                  → SimpleStockService.get_stock_data() + get_technical_indicators()
                  → yfinance (5d for price, 3mo for indicators)
                  → RSI, SMA, EMA, Bollinger Bands calculated in pandas
```

### AI Chat
```
User sends message → FinancialChatbot → POST /api/v1/ai/query?query=...
                   → OpenAIFinancialAI._answer()
                   → _extract_tickers() → search_companies() per candidate word
                   → _fetch_financial_data() → yfinance per resolved ticker
                   → _build_prompt() → one big string
                   → OpenAI gpt-4o-mini (single, non-streaming call)
                   → response rendered as Markdown
```

---

## Known Limitations (addressed in Phase 1+)

| Issue | Fix |
|-------|-----|
| `yfinance` is unreliable and rate-limited | Replace with Alpaca API |
| AI has no agency — data fetched before LLM sees anything | OpenAI tool-calling |
| No conversation memory — every message is stateless | PostgreSQL `conversations` table |
| User waits for full response (no streaming) | FastAPI SSE + React EventSource |
| 52-week high/low calculated from 5-day window (wrong) | Proper range data from Alpaca |
