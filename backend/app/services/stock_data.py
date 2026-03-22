import yfinance as yf
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class SimpleStockService:

    def get_stock_data(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="5d")
            info = stock.info

            if history.empty:
                return {"error": "No data available for this stock"}

            current_price = float(history['Close'].iloc[-1])
            previous_price = float(history['Close'].iloc[-2])
            price_change = current_price - previous_price
            percent_change = (price_change / previous_price) * 100

            return {
                "ticker": ticker.upper(),
                "current_price": current_price,
                "change": price_change,
                "change_percent": percent_change,
                "volume": int(history['Volume'].iloc[-1]),
                # 52-week range from 5-day history is approximate; will be replaced with Alpaca in Phase 1
                "52_week_high": float(history['High'].max()),
                "52_week_low": float(history['Low'].min()),
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
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="3mo")

            if history.empty:
                return {"error": "No data available for technical analysis"}

            rsi = self._calculate_rsi(history['Close'])
            sma_20 = history['Close'].rolling(window=20).mean().iloc[-1]
            sma_50 = history['Close'].rolling(window=50).mean().iloc[-1]
            ema_12 = history['Close'].ewm(span=12).mean().iloc[-1]
            ema_26 = history['Close'].ewm(span=26).mean().iloc[-1]

            sma_20_series = history['Close'].rolling(window=20).mean()
            std_20 = history['Close'].rolling(window=20).std()
            upper_band = sma_20_series + (std_20 * 2)
            lower_band = sma_20_series - (std_20 * 2)

            return {
                "rsi": {
                    "value": float(rsi),
                    "interpretation": self._interpret_rsi(rsi)
                },
                "sma_20": float(sma_20) if not pd.isna(sma_20) else None,
                "sma_50": float(sma_50) if not pd.isna(sma_50) else None,
                "ema_12": float(ema_12) if not pd.isna(ema_12) else None,
                "ema_26": float(ema_26) if not pd.isna(ema_26) else None,
                "bollinger_bands": {
                    "upper": float(upper_band.iloc[-1]) if not pd.isna(upper_band.iloc[-1]) else None,
                    "middle": float(sma_20) if not pd.isna(sma_20) else None,
                    "lower": float(lower_band.iloc[-1]) if not pd.isna(lower_band.iloc[-1]) else None
                },
                "trend": "Up" if sma_20 > sma_50 else "Down"
            }

        except Exception as e:
            logger.error(f"Error getting technical indicators for {ticker}: {e}")
            return {"error": f"Could not calculate indicators for {ticker}"}

    def _calculate_rsi(self, prices, window=14):
        try:
            delta = prices.diff()
            gains = delta.where(delta > 0, 0)
            losses = -delta.where(delta < 0, 0)
            avg_gains = gains.rolling(window=window).mean()
            avg_losses = losses.rolling(window=window).mean()
            rs = avg_gains / avg_losses
            return (100 - (100 / (1 + rs))).iloc[-1]
        except Exception as e:
            logger.error(f"RSI calculation failed: {e}")
            return 50  # neutral fallback

    def _interpret_rsi(self, rsi):
        if rsi >= 70:
            return "Overbought"
        elif rsi <= 30:
            return "Oversold"
        return "Neutral"

    def search_stock(self, query):
        result = self.get_stock_data(query.upper())
        return [result] if "error" not in result else []
