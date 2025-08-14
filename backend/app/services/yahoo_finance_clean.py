"""
Yahoo Finance Service - Clean and Simple
Provides stock data and technical analysis using Yahoo Finance API
"""
import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Any, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EnhancedYahooFinanceService:
    """Clean and simple Yahoo Finance service"""
    
    def __init__(self):
        """Initialize the service"""
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
    
    def get_stock_data(self, ticker: str, period: str = "1y") -> Dict[str, Any]:
        """Get basic stock data"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            info = stock.info
            
            if hist.empty:
                return {"error": "No data available"}
            
            return {
                "ticker": ticker,
                "current_price": float(hist['Close'].iloc[-1]),
                "change": float(hist['Close'].iloc[-1] - hist['Close'].iloc[-2]),
                "change_percent": float((hist['Close'].iloc[-1] / hist['Close'].iloc[-2] - 1) * 100),
                "volume": int(hist['Volume'].iloc[-1]),
                "market_cap": info.get('marketCap'),
                "company_name": info.get('longName', ticker),
                "sector": info.get('sector'),
                "industry": info.get('industry')
            }
        except Exception as e:
            logger.error(f"Error getting stock data for {ticker}: {e}")
            return {"error": str(e)}
    
    def get_technical_indicators(self, ticker: str) -> Dict[str, Any]:
        """Get technical analysis indicators"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="6mo")
            
            if hist.empty:
                return {"error": "No historical data available"}
            
            # Get price data
            close_prices = hist['Close']
            high_prices = hist['High']
            low_prices = hist['Low']
            volume = hist['Volume']
            
            # Calculate RSI (simple version)
            delta = close_prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # Calculate moving averages
            sma_20 = close_prices.rolling(window=20).mean()
            sma_50 = close_prices.rolling(window=50).mean()
            ema_12 = close_prices.ewm(span=12).mean()
            ema_26 = close_prices.ewm(span=26).mean()
            
            # Calculate Bollinger Bands
            bb_middle = sma_20
            bb_std = close_prices.rolling(window=20).std()
            bb_upper = bb_middle + (bb_std * 2)
            bb_lower = bb_middle - (bb_std * 2)
            
            # Calculate volatility
            volatility = close_prices.pct_change().rolling(window=20).std() * np.sqrt(252)
            
            return {
                "ticker": ticker,
                "last_updated": datetime.now().isoformat(),
                "indicators": {
                    "rsi": {
                        "current": float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else None,
                        "interpretation": self._get_rsi_signal(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else "No data"
                    },
                    "bollinger_bands": {
                        "upper": float(bb_upper.iloc[-1]) if not pd.isna(bb_upper.iloc[-1]) else None,
                        "middle": float(bb_middle.iloc[-1]) if not pd.isna(bb_middle.iloc[-1]) else None,
                        "lower": float(bb_lower.iloc[-1]) if not pd.isna(bb_lower.iloc[-1]) else None,
                        "interpretation": "Bollinger Bands analysis"
                    },
                    "moving_averages": {
                        "sma_20": float(sma_20.iloc[-1]) if not pd.isna(sma_20.iloc[-1]) else None,
                        "sma_50": float(sma_50.iloc[-1]) if not pd.isna(sma_50.iloc[-1]) else None,
                        "ema_12": float(ema_12.iloc[-1]) if not pd.isna(ema_12.iloc[-1]) else None,
                        "ema_26": float(ema_26.iloc[-1]) if not pd.isna(ema_26.iloc[-1]) else None,
                        "interpretation": "Moving averages"
                    },
                    "volatility": {
                        "current": float(volatility.iloc[-1]) if not pd.isna(volatility.iloc[-1]) else None,
                        "interpretation": "20-day volatility"
                    }
                },
                "price_data": {
                    "current_price": float(close_prices.iloc[-1]),
                    "high_6m": float(high_prices.max()),
                    "low_6m": float(low_prices.min()),
                    "volume_avg": float(volume.mean())
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting technical indicators for {ticker}: {e}")
            return {"error": str(e)}
    
    def get_financial_ratios(self, ticker: str) -> Dict[str, Any]:
        """Get financial ratios"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                "ticker": ticker,
                "last_updated": datetime.now().isoformat(),
                "valuation": {
                    "pe_ratio": info.get('trailingPE'),
                    "forward_pe": info.get('forwardPE'),
                    "price_to_book": info.get('priceToBook'),
                    "price_to_sales": info.get('priceToSalesTrailing12Months')
                },
                "profitability": {
                    "profit_margin": info.get('profitMargins'),
                    "operating_margin": info.get('operatingMargins'),
                    "return_on_equity": info.get('returnOnEquity'),
                    "return_on_assets": info.get('returnOnAssets')
                },
                "financial_health": {
                    "current_ratio": info.get('currentRatio'),
                    "debt_to_equity": info.get('debtToEquity'),
                    "total_cash": info.get('totalCash'),
                    "total_debt": info.get('totalDebt')
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting financial ratios for {ticker}: {e}")
            return {"error": str(e)}
    
    def _get_rsi_signal(self, rsi_value: float) -> str:
        """Simple RSI interpretation"""
        if rsi_value > 70:
            return "Overbought"
        elif rsi_value < 30:
            return "Oversold"
        else:
            return "Neutral"
