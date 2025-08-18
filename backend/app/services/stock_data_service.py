"""
Stock Data Service - Gets real-time stock prices and information

This service connects to Yahoo Finance to get:
- Current stock prices (how much a stock costs right now)
- Price changes (how much it went up or down today)
- Company information (name, sector, market cap)
- Technical indicators (RSI, moving averages)

It's like having a direct line to the stock market!
"""
import yfinance as yf
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class SimpleStockService:
    """A service that fetches live stock market data from Yahoo Finance"""
    
    def __init__(self):
        """Set up the service"""
        pass
    
    def get_stock_data(self, ticker):
        """Get basic information about a stock"""
        try:
            # Create a Yahoo Finance ticker object
            stock = yf.Ticker(ticker)
            
            # Get recent price history (last 5 days)
            history = stock.history(period="5d")
            
            # Get company information
            info = stock.info
            
            # Make sure we have data
            if history.empty:
                return {"error": "No data available for this stock"}
            
            # Get the most recent prices
            current_price = float(history['Close'].iloc[-1])  # Today's price
            previous_price = float(history['Close'].iloc[-2])  # Yesterday's price
            
            # Calculate the change
            price_change = current_price - previous_price
            percent_change = (price_change / previous_price) * 100
            
            # Get today's volume
            volume = int(history['Volume'].iloc[-1])
            
            # Calculate 52-week high and low from history
            max_52_week = float(history['High'].max()) if len(history) >= 252 else float(history['High'].max())
            min_52_week = float(history['Low'].min()) if len(history) >= 252 else float(history['Low'].min())
            
            # Return all the information in a simple format
            return {
                "ticker": ticker.upper(),
                "current_price": current_price,
                "change": price_change,
                "change_percent": percent_change,
                "volume": volume,
                "52_week_high": max_52_week,
                "52_week_low": min_52_week,
                "company_name": info.get('longName', ticker),
                "sector": info.get('sector', 'Unknown'),
                "industry": info.get('industry', 'Unknown'),
                "market_cap": info.get('marketCap'),
                "pe_ratio": info.get('trailingPE'),
                "dividend_yield": info.get('dividendYield')
            }
            
        except Exception as e:
            logger.error(f"Error getting data for {ticker}: {e}")
            return {"error": f"Could not get data for {ticker}"}
    
    def get_technical_indicators(self, ticker):
        """Get some basic technical indicators (simple stuff)"""
        try:
            # Get the stock
            stock = yf.Ticker(ticker)
            
            # Get more history for calculations
            history = stock.history(period="3mo")  # 3 months of data
            
            if history.empty:
                return {"error": "No data available for technical analysis"}
            
            # Calculate RSI (Relative Strength Index)
            # This shows if a stock is overbought or oversold
            rsi = self._calculate_simple_rsi(history['Close'])
            
            # Calculate simple moving averages
            sma_20 = history['Close'].rolling(window=20).mean().iloc[-1]  # 20-day average
            sma_50 = history['Close'].rolling(window=50).mean().iloc[-1]  # 50-day average
            
            return {
                "rsi": {
                    "value": float(rsi),
                    "interpretation": self._interpret_rsi(rsi)
                },
                "sma_20": float(sma_20) if not pd.isna(sma_20) else None,
                "sma_50": float(sma_50) if not pd.isna(sma_50) else None,
                "trend": "Up" if sma_20 > sma_50 else "Down"
            }
            
        except Exception as e:
            logger.error(f"Error getting technical indicators for {ticker}: {e}")
            return {"error": f"Could not calculate indicators for {ticker}"}
    
    def _calculate_simple_rsi(self, prices, window=14):
        """Calculate RSI in a simple way"""
        try:
            # Calculate price changes
            delta = prices.diff()
            
            # Separate gains and losses
            gains = delta.where(delta > 0, 0)  # Only positive changes
            losses = -delta.where(delta < 0, 0)  # Only negative changes (made positive)
            
            # Calculate average gains and losses
            avg_gains = gains.rolling(window=window).mean()
            avg_losses = losses.rolling(window=window).mean()
            
            # Calculate relative strength
            rs = avg_gains / avg_losses
            
            # Calculate RSI
            rsi = 100 - (100 / (1 + rs))
            
            return rsi.iloc[-1]  # Return the most recent RSI
            
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return 50  # Return neutral RSI if calculation fails
    
    def _interpret_rsi(self, rsi):
        """Explain what the RSI means in simple terms"""
        if rsi >= 70:
            return "Overbought - stock might be expensive right now"
        elif rsi <= 30:
            return "Oversold - stock might be cheap right now"
        else:
            return "Neutral - stock is neither expensive nor cheap"
    
    def search_stock(self, query):
        """Search for stocks by company name or ticker"""
        try:
            # This is a simple implementation
            # In a real app, you might use a stock search API
            query = query.upper()
            
            # Try to get stock data to see if it's a valid ticker
            result = self.get_stock_data(query)
            
            if "error" not in result:
                return [result]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error searching for {query}: {e}")
            return []
    
    def get_market_status(self):
        """Check if the market is open or closed"""
        try:
            from datetime import datetime, time
            import pytz
            
            # Get current time in Eastern Time (where NYSE is)
            et = pytz.timezone('US/Eastern')
            current_time = datetime.now(et).time()
            
            # Market is open Monday-Friday, 9:30 AM to 4:00 PM ET
            market_open = time(9, 30)
            market_close = time(16, 0)
            
            is_weekend = datetime.now(et).weekday() >= 5  # Saturday = 5, Sunday = 6
            
            if is_weekend:
                return {"status": "closed", "reason": "Weekend"}
            elif market_open <= current_time <= market_close:
                return {"status": "open", "reason": "Market hours"}
            else:
                return {"status": "closed", "reason": "After hours"}
                
        except Exception as e:
            logger.error(f"Error checking market status: {e}")
            return {"status": "unknown", "reason": "Could not determine"}

# Import pandas for the RSI calculation
import pandas as pd
