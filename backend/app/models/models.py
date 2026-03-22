from pydantic import BaseModel, Field
from datetime import datetime


class BaseResponse(BaseModel):
    success: bool = True
    timestamp: datetime = Field(default_factory=datetime.now)
    message: str = None


class CompanyInfo(BaseModel):
    rank: int
    company: str
    ticker: str
    sector: str = None
    industry: str = None
    revenue: float = None
    profit: float = None
    market_cap: float = None


class AIQueryRequest(BaseModel):
    query: str
    include_suggestions: bool = True


class AIQueryResponse(BaseResponse):
    query: str
    message: str
    type: str = "general"
    companies_analyzed: list = []
    has_real_time_data: bool = False
    suggestions: list = None
