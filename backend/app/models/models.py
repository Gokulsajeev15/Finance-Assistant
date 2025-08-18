from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum

# Enums
class QueryType(str, Enum):
    COMPARISON = "comparison"
    RANKING = "ranking"
    PORTFOLIO = "portfolio"
    SECTOR = "sector"
    TECHNICAL = "technical"
    FUNDAMENTAL = "fundamental"
    SENTIMENT = "sentiment"
    SCREENING = "screening"
    GENERAL = "general"

class RiskLevel(str, Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"

class Timeframe(str, Enum):
    DAILY = "1d"
    WEEKLY = "1wk"
    MONTHLY = "1mo"
    QUARTERLY = "3mo"
    YEARLY = "1y"
    FIVE_YEAR = "5y"

# Base Models
class BaseResponse(BaseModel):
    success: bool = True
    timestamp: datetime = Field(default_factory=datetime.now)
    message: Optional[str] = None

class ErrorResponse(BaseResponse):
    success: bool = False
    error: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

# Company Models
class CompanyInfo(BaseModel):
    rank: int
    company: str
    ticker: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    revenue: Optional[float] = None
    profit: Optional[float] = None
    market_cap: Optional[float] = None

class CompanyComparison(BaseModel):
    company: str
    ticker: str
    data: Dict[str, Any]
    error: Optional[str] = None

class ComparisonResponse(BaseResponse):
    query_type: QueryType = QueryType.COMPARISON
    query: str
    companies: List[CompanyComparison]
    metric: Optional[str] = None
    comparison_summary: str

# Ranking Models
class RankingEntry(BaseModel):
    rank: int
    company: str
    ticker: str
    value: float
    sector: Optional[str] = None
    industry: Optional[str] = None

class RankingResponse(BaseResponse):
    query_type: QueryType = QueryType.RANKING
    query: str
    rankings: List[RankingEntry]
    metric: str
    count: int
    summary: str

# Technical Analysis Models
class TechnicalIndicator(BaseModel):
    current: Optional[float] = None
    interpretation: str
    values: Optional[List[float]] = None

class MACDData(BaseModel):
    macd_line: Optional[float] = None
    signal_line: Optional[float] = None
    histogram: Optional[float] = None
    interpretation: str

class BollingerBands(BaseModel):
    upper: Optional[float] = None
    middle: Optional[float] = None
    lower: Optional[float] = None
    bandwidth: Optional[float] = None
    interpretation: str

class MovingAverages(BaseModel):
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    ema_12: Optional[float] = None
    ema_26: Optional[float] = None
    interpretation: str

class StochasticData(BaseModel):
    k_percent: Optional[float] = None
    d_percent: Optional[float] = None
    interpretation: str

class TechnicalIndicators(BaseModel):
    rsi: TechnicalIndicator
    macd: MACDData
    bollinger_bands: BollingerBands
    moving_averages: MovingAverages
    stochastic: StochasticData
    atr: Optional[float] = None
    williams_r: Optional[float] = None
    cci: Optional[float] = None
    mfi: Optional[float] = None

class PriceData(BaseModel):
    current_price: float
    high_6m: float
    low_6m: float
    volume_avg: float

class TechnicalAnalysisResponse(BaseResponse):
    ticker: str
    last_updated: datetime
    indicators: TechnicalIndicators
    price_data: PriceData

# Financial Ratios Models
class ValuationRatios(BaseModel):
    pe_ratio: Optional[float] = None
    forward_pe: Optional[float] = None
    peg_ratio: Optional[float] = None
    price_to_book: Optional[float] = None
    price_to_sales: Optional[float] = None
    ev_to_revenue: Optional[float] = None
    ev_to_ebitda: Optional[float] = None
    price_to_cash_flow: Optional[float] = None

class ProfitabilityRatios(BaseModel):
    profit_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    gross_margin: Optional[float] = None
    return_on_assets: Optional[float] = None
    return_on_equity: Optional[float] = None
    return_on_capital: Optional[float] = None

class LiquidityRatios(BaseModel):
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    cash_ratio: Optional[float] = None

class LeverageRatios(BaseModel):
    debt_to_equity: Optional[float] = None
    debt_to_assets: Optional[float] = None
    total_debt: Optional[float] = None
    interest_coverage: Optional[float] = None

class EfficiencyRatios(BaseModel):
    asset_turnover: Optional[float] = None
    inventory_turnover: Optional[float] = None
    receivables_turnover: Optional[float] = None

class GrowthMetrics(BaseModel):
    revenue_growth: Optional[float] = None
    earnings_growth: Optional[float] = None
    revenue_per_share: Optional[float] = None
    book_value_per_share: Optional[float] = None

class FinancialRatiosResponse(BaseResponse):
    ticker: str
    last_updated: datetime
    valuation_ratios: ValuationRatios
    profitability_ratios: ProfitabilityRatios
    liquidity_ratios: LiquidityRatios
    leverage_ratios: LeverageRatios
    efficiency_ratios: EfficiencyRatios
    growth_metrics: GrowthMetrics

# Market Sentiment Models
class OwnershipInfo(BaseModel):
    name: str
    shares: Optional[int] = None
    value: Optional[float] = None
    percent: Optional[float] = None

class AnalystRecommendations(BaseModel):
    buy_count: int
    hold_count: int
    sell_count: int
    total_recommendations: int
    sentiment_score: float

class MarketData(BaseModel):
    market_cap: Optional[float] = None
    enterprise_value: Optional[float] = None
    float_shares: Optional[int] = None
    shares_outstanding: Optional[int] = None
    shares_short: Optional[int] = None
    shares_short_prior_month: Optional[int] = None
    short_ratio: Optional[float] = None
    short_percent_of_float: Optional[float] = None

class MarketSentimentResponse(BaseResponse):
    ticker: str
    last_updated: datetime
    ownership: Dict[str, List[OwnershipInfo]]
    analyst_recommendations: AnalystRecommendations
    market_data: MarketData

# Portfolio Models
class PortfolioHolding(BaseModel):
    market_cap: float
    weight: float
    pe_ratio: Optional[float] = None
    beta: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None

class PortfolioMetrics(BaseModel):
    total_market_cap: float
    weighted_pe_ratio: float
    weighted_beta: float
    diversification_score: float
    sector_allocation: Dict[str, float]

class PortfolioAnalysisResponse(BaseResponse):
    portfolio_metrics: PortfolioMetrics
    individual_holdings: Dict[str, PortfolioHolding]
    total_holdings: int

# Sector Analysis Models
class SectorSummary(BaseModel):
    count: int
    total_revenue: float
    total_profit: float
    companies: List[str]

class SectorAnalysisResponse(BaseResponse):
    query_type: QueryType = QueryType.SECTOR
    query: str
    sector: Optional[str] = None
    companies: List[CompanyInfo]
    count: int
    sector_summary: Optional[Dict[str, SectorSummary]] = None

# AI Query Models
class AIQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    include_technical: bool = False
    include_fundamental: bool = False
    include_sentiment: bool = False

class AIQueryResponse(BaseResponse):
    query_type: QueryType
    query: str
    data: Dict[str, Any]
    suggestions: Optional[List[str]] = None

# Portfolio Optimization Models
class PortfolioOptimizationRequest(BaseModel):
    tickers: List[str] = Field(..., min_items=1, max_items=50)
    risk_level: RiskLevel = RiskLevel.MODERATE
    investment_amount: float = Field(..., gt=0)
    target_return: Optional[float] = None
    constraints: Optional[Dict[str, Any]] = None

class PortfolioOptimizationResponse(BaseResponse):
    optimal_weights: Dict[str, float]
    expected_return: float
    expected_risk: float
    sharpe_ratio: float
    sector_allocation: Dict[str, float]
    risk_metrics: Dict[str, float]

# Screening Models
class ScreeningCriteria(BaseModel):
    pe_ratio_min: Optional[float] = None
    pe_ratio_max: Optional[float] = None
    market_cap_min: Optional[float] = None
    market_cap_max: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    revenue_growth_min: Optional[float] = None
    profit_margin_min: Optional[float] = None

class StockScreeningRequest(BaseModel):
    criteria: ScreeningCriteria
    max_results: int = Field(default=100, le=500)
    sort_by: str = "market_cap"
    sort_order: str = "desc"

class StockScreeningResponse(BaseResponse):
    results: List[CompanyInfo]
    total_found: int
    criteria_used: ScreeningCriteria
    execution_time: float

# Cache Models
class CacheStats(BaseModel):
    status: str
    total_keys: Optional[int] = None
    memory_usage: Optional[str] = None
    redis_version: Optional[str] = None
    connected_clients: Optional[int] = None
    keyspace_hits: Optional[int] = None
    keyspace_misses: Optional[int] = None

# Health and Status Models
class HealthResponse(BaseModel):
    status: str
    version: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    services: Dict[str, str]
    cache_status: Optional[CacheStats] = None
    uptime: Optional[float] = None

class ServiceStatus(BaseModel):
    name: str
    status: str
    response_time: Optional[float] = None
    last_check: datetime = Field(default_factory=datetime.now)
    error: Optional[str] = None

# Utility Models
class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort_by: Optional[str] = None
    sort_order: str = "asc"

class PaginatedResponse(BaseModel):
    data: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool

# Validators
@validator('tickers')
def validate_tickers(cls, v):
    """Validate ticker symbols"""
    for ticker in v:
        if not ticker.isalpha() or len(ticker) > 5:
            raise ValueError(f"Invalid ticker symbol: {ticker}")
    return v

@validator('investment_amount')
def validate_investment_amount(cls, v):
    """Validate investment amount"""
    if v <= 0:
        raise ValueError("Investment amount must be positive")
    return v

@validator('query')
def validate_query(cls, v):
    """Validate AI query"""
    if not v.strip():
        raise ValueError("Query cannot be empty")
    if len(v) > 1000:
        raise ValueError("Query too long (max 1000 characters)")
    return v.strip()
