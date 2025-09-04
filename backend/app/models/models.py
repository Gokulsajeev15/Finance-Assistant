"""
Simple data models for the Finance Assistant API

These models define the structure of data that flows through our API.
Think of them as templates that describe what information we expect!
"""
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

# Simple types for categorizing responses
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

# Basic response models
class BaseResponse(BaseModel):
    """Basic response that all API responses use"""
    success: bool = True
    timestamp: datetime = Field(default_factory=datetime.now)
    message: str = None

class ErrorResponse(BaseResponse):
    """Response for when something goes wrong"""
    success: bool = False
    error: str
    error_code: str = None
    details: dict = None

class HealthResponse(BaseResponse):
    """Health check response"""
    status: str = "ok"
    version: str = "3.0.0"
    services: dict = {}

# Company information models
class CompanyInfo(BaseModel):
    """Information about a company"""
    rank: int
    company: str
    ticker: str
    sector: str = None
    industry: str = None
    revenue: float = None
    profit: float = None
    market_cap: float = None

class CompanyComparison(BaseModel):
    """Data for comparing companies"""
    company: str
    ticker: str
    data: dict
    error: str = None

class ComparisonResponse(BaseResponse):
    """Response for company comparisons"""
    query_type: QueryType = QueryType.COMPARISON
    query: str
    companies: list
    metric: str = None
    comparison_summary: str

# Ranking models
class RankingEntry(BaseModel):
    """Entry in a ranking list"""
    rank: int
    company: str
    ticker: str
    value: float
    sector: str = None
    industry: str = None

class RankingResponse(BaseResponse):
    """Response for rankings"""
    query_type: QueryType = QueryType.RANKING
    query: str
    rankings: list
    metric: str
    count: int
    summary: str

# Technical analysis models
class TechnicalIndicator(BaseModel):
    """A technical analysis indicator"""
    current: float = None
    interpretation: str
    values: list = None

class MACDData(BaseModel):
    """MACD indicator data"""
    macd_line: float = None
    signal_line: float = None
    histogram: float = None
    interpretation: str

class BollingerBands(BaseModel):
    """Bollinger Bands data"""
    upper: float = None
    middle: float = None
    lower: float = None
    bandwidth: float = None
    interpretation: str

class MovingAverages(BaseModel):
    """Moving averages data"""
    sma_20: float = None
    sma_50: float = None
    ema_12: float = None
    ema_26: float = None
    interpretation: str

class StochasticData(BaseModel):
    """Stochastic oscillator data"""
    k_percent: float = None
    d_percent: float = None
    interpretation: str

class TechnicalIndicators(BaseModel):
    """Collection of technical indicators"""
    rsi: TechnicalIndicator
    macd: MACDData
    bollinger_bands: BollingerBands
    moving_averages: MovingAverages
    stochastic: StochasticData
    atr: float = None
    williams_r: float = None
    cci: float = None
    mfi: float = None

class PriceData(BaseModel):
    """Stock price data"""
    current_price: float
    high_6m: float
    low_6m: float
    volume_avg: float

class TechnicalAnalysisResponse(BaseResponse):
    """Technical analysis response"""
    ticker: str
    last_updated: datetime
    indicators: TechnicalIndicators
    price_data: PriceData

# Financial ratios models
class ValuationRatios(BaseModel):
    """Valuation ratio metrics"""
    pe_ratio: float = None
    forward_pe: float = None
    peg_ratio: float = None
    price_to_book: float = None
    price_to_sales: float = None
    ev_to_revenue: float = None
    ev_to_ebitda: float = None
    price_to_cash_flow: float = None

class ProfitabilityRatios(BaseModel):
    """Profitability ratio metrics"""
    profit_margin: float = None
    operating_margin: float = None
    gross_margin: float = None
    return_on_assets: float = None
    return_on_equity: float = None
    return_on_capital: float = None

class LiquidityRatios(BaseModel):
    """Liquidity ratio metrics"""
    current_ratio: float = None
    quick_ratio: float = None
    cash_ratio: float = None

class LeverageRatios(BaseModel):
    """Leverage ratio metrics"""
    debt_to_equity: float = None
    debt_to_assets: float = None
    total_debt: float = None
    interest_coverage: float = None

class EfficiencyRatios(BaseModel):
    """Efficiency ratio metrics"""
    asset_turnover: float = None
    inventory_turnover: float = None
    receivables_turnover: float = None

class GrowthMetrics(BaseModel):
    """Growth metric data"""
    revenue_growth: float = None
    earnings_growth: float = None
    revenue_per_share: float = None
    book_value_per_share: float = None

class FinancialRatiosResponse(BaseResponse):
    """Financial ratios analysis response"""
    ticker: str
    last_updated: datetime
    valuation_ratios: ValuationRatios
    profitability_ratios: ProfitabilityRatios
    liquidity_ratios: LiquidityRatios
    leverage_ratios: LeverageRatios
    efficiency_ratios: EfficiencyRatios
    growth_metrics: GrowthMetrics

# AI Query Models
class AIQueryRequest(BaseModel):
    """Request for AI analysis"""
    query: str
    include_suggestions: bool = True

class AIQueryResponse(BaseResponse):
    """AI analysis response"""
    query: str
    message: str
    type: str = "general"
    companies_analyzed: list = []
    has_real_time_data: bool = False
    suggestions: list = None
    confidence_score: float = None

# Stock data models
class StockDataRequest(BaseModel):
    """Request for stock data"""
    ticker: str
    timeframe: Timeframe = Timeframe.DAILY

class BasicStockData(BaseModel):
    """Basic stock information"""
    ticker: str
    company_name: str = None
    current_price: float = None
    price_change: float = None
    change_percent: str = None
    volume: str = None
    market_cap: str = None
    pe_ratio: float = None
    day_high: float = None
    day_low: float = None
    year_high: float = None
    year_low: float = None
    sector: str = None

class StockDataResponse(BaseResponse):
    """Stock data response"""
    ticker: str
    data: BasicStockData
    last_updated: datetime

# Simple search models
class SearchRequest(BaseModel):
    """Search request"""
    query: str
    limit: int = 10

class SearchResponse(BaseResponse):
    """Search results response"""
    query: str
    results: list
    total_results: int
