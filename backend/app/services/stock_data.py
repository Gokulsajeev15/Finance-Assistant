import os
import requests
import pandas as pd
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://www.alphavantage.co/query"


class SimpleStockService:

    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_KEY')
        if not self.api_key:
            logger.error("ALPHA_VANTAGE_KEY not set")

    def get_stock_data(self, ticker):
        """
        Fetch current price, daily change, volume, and day range for a ticker.
        Uses the GLOBAL_QUOTE endpoint — one call, real-time data.
        """
        if not self.api_key:
            return {"error": "Stock service not configured. Set ALPHA_VANTAGE_KEY in .env"}

        try:
            response = requests.get(BASE_URL, params={
                "function": "GLOBAL_QUOTE",
                "symbol": ticker.upper(),
                "apikey": self.api_key
            })
            response.raise_for_status()
            data = response.json()

            quote = data.get("Global Quote", {})

            # Alpha Vantage sends rate limit messages as special keys instead of HTTP errors.
            # Only treat it as a hard failure if there's no actual quote data alongside the message.
            if not quote and ("Note" in data or "Information" in data):
                msg = data.get("Note") or data.get("Information", "")
                logger.warning(f"Alpha Vantage rate limit: {msg}")
                return {"error": "API rate limit reached. Alpha Vantage free tier allows 25 requests/day."}

            if not quote or not quote.get("05. price"):
                return {"error": f"No data found for '{ticker}'. Check the ticker symbol is valid (e.g. AAPL, TSLA)."}

            return {
                "ticker": ticker.upper(),
                "current_price": float(quote["05. price"]),
                "change": float(quote["09. change"]),
                # Alpha Vantage returns change percent as "4.35%" — strip the % sign before casting
                "change_percent": float(quote["10. change percent"].replace("%", "")),
                "volume": int(quote["06. volume"]),
                "day_high": float(quote["03. high"]),
                "day_low": float(quote["04. low"]),
                "previous_close": float(quote["08. previous close"]),
            }

        except requests.RequestException as e:
            logger.error(f"Network error fetching quote for {ticker}: {e}")
            return {"error": "Could not reach the data provider. Check your internet connection and try again."}
        except Exception as e:
            logger.error(f"Error getting stock data for {ticker}: {e}")
            return {"error": f"Could not get data for {ticker}"}

    def get_technical_indicators(self, ticker):
        """
        Fetch 100 days of daily OHLCV bars and compute RSI, moving averages, and Bollinger Bands.
        Uses TIME_SERIES_DAILY — the pandas math is the same as before, just better source data.
        """
        if not self.api_key:
            return {"error": "Stock service not configured. Set ALPHA_VANTAGE_KEY in .env"}

        try:
            response = requests.get(BASE_URL, params={
                "function": "TIME_SERIES_DAILY",
                "symbol": ticker.upper(),
                "outputsize": "compact",  # last 100 trading days — enough for SMA50 + RSI14
                "apikey": self.api_key
            })
            response.raise_for_status()
            data = response.json()

            time_series = data.get("Time Series (Daily)", {})

            if not time_series and ("Note" in data or "Information" in data):
                msg = data.get("Note") or data.get("Information", "")
                logger.warning(f"Alpha Vantage rate limit: {msg}")
                return {"error": "API rate limit reached. Alpha Vantage free tier allows 25 requests/day."}

            if not time_series:
                error_msg = data.get("Error Message", "")
                if error_msg:
                    return {"error": f"Invalid ticker: {ticker}"}
                return {"error": f"No historical data available for {ticker}"}

            # Alpha Vantage returns a dict of {date_string: {OHLCV fields}}
            # We build a DataFrame from it, sort oldest-first, then run our indicator math
            df = pd.DataFrame.from_dict(time_series, orient="index")
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            df.columns = ["open", "high", "low", "close", "volume"]
            df = df.astype(float)

            close = df["close"]

            # Price data derived from bars — used by the technical route so it doesn't
            # need a separate get_stock_data call (avoids back-to-back API calls)
            current_price = float(close.iloc[-1])
            prev_price = float(close.iloc[-2])
            price_change = current_price - prev_price

            rsi = self._calculate_rsi(close)
            sma_20 = close.rolling(window=20).mean().iloc[-1]
            sma_50 = close.rolling(window=50).mean().iloc[-1]
            ema_12 = close.ewm(span=12).mean().iloc[-1]
            ema_26 = close.ewm(span=26).mean().iloc[-1]

            sma_20_series = close.rolling(window=20).mean()
            std_20 = close.rolling(window=20).std()
            upper_band = sma_20_series + (std_20 * 2)
            lower_band = sma_20_series - (std_20 * 2)

            return {
                # Price fields — lets the technical route skip a separate get_stock_data call
                "current_price": current_price,
                "change": price_change,
                "change_percent": (price_change / prev_price) * 100 if prev_price else 0,
                "volume": int(df["volume"].iloc[-1]),
                "day_high": float(df["high"].iloc[-1]),
                "day_low": float(df["low"].iloc[-1]),
                # 100-day high/low — compact outputsize gives ~100 trading days (~5 months).
                # True 52-week range requires outputsize=full which is a paid Alpha Vantage feature.
                "high_100d": float(df["high"].max()),
                "low_100d": float(df["low"].min()),
                # Technical indicators
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

        except requests.RequestException as e:
            logger.error(f"Network error fetching bars for {ticker}: {e}")
            return {"error": "Could not reach the data provider. Check your internet connection and try again."}
        except Exception as e:
            logger.error(f"Error calculating indicators for {ticker}: {e}")
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
