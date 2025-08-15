"""
AI Query Processor - Simple and Clean
Processes natural language queries about stocks and companies
"""
from typing import Dict, Any
import re
import logging

logger = logging.getLogger(__name__)

class AIQueryProcessor:
    """Simple AI query processor for financial questions"""
    
    def __init__(self, yahoo_service, fortune500_service):
        self.yahoo_service = yahoo_service
        self.fortune500_service = fortune500_service
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a natural language query and return intelligent results"""
        query = query.lower().strip()
        
        try:
            # Analysis and comparison queries
            if self._is_analysis_query(query):
                return self._handle_analysis_query(query)
            
            # Performance and valuation queries
            elif self._is_performance_query(query):
                return self._handle_performance_query(query)
            
            # Technical analysis queries
            elif self._is_technical_query(query):
                return self._handle_technical_query(query)
            
            # Stock price queries
            elif self._is_price_query(query):
                return self._handle_price_query(query)
            
            # Company information queries
            elif self._is_company_query(query):
                return self._handle_company_query(query)
            
            else:
                return self._handle_general_query(query)
                
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {"type": "error", "message": f"Error processing query: {str(e)}"}
    
    def _is_price_query(self, query: str) -> bool:
        """Check if query is asking for stock price"""
        price_keywords = ["price", "cost", "value", "worth", "current", "quote"]
        return any(keyword in query for keyword in price_keywords)
    
    def _is_company_query(self, query: str) -> bool:
        """Check if query is asking for company information"""
        company_keywords = ["company", "about", "information", "details", "tell me"]
        return any(keyword in query for keyword in company_keywords)
    
    def _is_analysis_query(self, query: str) -> bool:
        """Check if query is asking for comprehensive analysis"""
        analysis_keywords = ["analyze", "analysis", "how is", "performance", "overview", "summary", "report"]
        return any(keyword in query for keyword in analysis_keywords)
    
    def _is_performance_query(self, query: str) -> bool:
        """Check if query is asking about financial performance"""
        performance_keywords = ["revenue", "profit", "earnings", "income", "margin", "growth", "financials"]
        return any(keyword in query for keyword in performance_keywords)
    
    def _is_technical_query(self, query: str) -> bool:
        """Check if query is asking for technical analysis"""
        technical_keywords = ["rsi", "bollinger", "moving average", "technical", "analysis", "indicator", "chart"]
        return any(keyword in query for keyword in technical_keywords)
    
    def _extract_ticker(self, query: str) -> str:
        """Extract stock ticker from query with comprehensive company name mapping"""
        # Comprehensive company name to ticker mapping
        company_map = {
            # Technology
            "apple": "AAPL", "apple inc": "AAPL", "iphone": "AAPL",
            "microsoft": "MSFT", "windows": "MSFT", "xbox": "MSFT",
            "google": "GOOGL", "alphabet": "GOOGL", "youtube": "GOOGL",
            "amazon": "AMZN", "aws": "AMZN", "prime": "AMZN",
            "meta": "META", "facebook": "META", "instagram": "META", "whatsapp": "META",
            "tesla": "TSLA", "spacex": "TSLA", "elon musk": "TSLA",
            "netflix": "NFLX", "streaming": "NFLX",
            "nvidia": "NVDA", "ai chips": "NVDA",
            "intel": "INTC", "processor": "INTC",
            "oracle": "ORCL", "database": "ORCL",
            "salesforce": "CRM", "crm": "CRM",
            "adobe": "ADBE", "photoshop": "ADBE",
            "zoom": "ZM", "video call": "ZM",
            
            # Retail & Consumer
            "walmart": "WMT", "supermarket": "WMT",
            "target": "TGT", "retail": "TGT",
            "costco": "COST", "wholesale": "COST",
            "home depot": "HD", "hardware store": "HD",
            "mcdonalds": "MCD", "mcdonald's": "MCD", "fast food": "MCD",
            "starbucks": "SBUX", "coffee": "SBUX",
            "nike": "NKE", "sports shoes": "NKE", "sneakers": "NKE",
            "coca cola": "KO", "coke": "KO", "coca-cola": "KO",
            "pepsi": "PEP", "pepsico": "PEP",
            
            # Healthcare
            "unitedhealth": "UNH", "united health": "UNH", "health insurance": "UNH",
            "johnson": "JNJ", "johnson & johnson": "JNJ", "j&j": "JNJ",
            "pfizer": "PFE", "vaccine": "PFE",
            "moderna": "MRNA", "covid": "MRNA",
            "cvs": "CVS", "pharmacy": "CVS",
            
            # Financial
            "berkshire": "BRK-B", "berkshire hathaway": "BRK-B", "warren buffett": "BRK-B",
            "jpmorgan": "JPM", "jp morgan": "JPM", "chase": "JPM",
            "bank of america": "BAC", "bofa": "BAC",
            "goldman sachs": "GS", "goldman": "GS",
            "american express": "AXP", "amex": "AXP",
            "visa": "V", "credit card": "V",
            "mastercard": "MA", "payment": "MA",
            
            # Energy & Industrial
            "exxon": "XOM", "exxonmobil": "XOM", "oil": "XOM",
            "chevron": "CVX", "gas": "CVX",
            "boeing": "BA", "airplane": "BA", "aircraft": "BA",
            "caterpillar": "CAT", "construction": "CAT",
            "general electric": "GE", "ge": "GE",
            
            # Entertainment & Media
            "disney": "DIS", "walt disney": "DIS", "marvel": "DIS",
            "comcast": "CMCSA", "cable": "CMCSA",
            "verizon": "VZ", "telecom": "VZ",
            "at&t": "T", "att": "T", "phone": "T"
        }
        
        query_lower = query.lower()
        
        # Try exact matches first (longer phrases first)
        sorted_companies = sorted(company_map.items(), key=lambda x: len(x[0]), reverse=True)
        for company, ticker in sorted_companies:
            if company in query_lower:
                return ticker
        
        # Look for known tickers in the query
        known_tickers = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NFLX", "NVDA", 
            "INTC", "ORCL", "CRM", "ADBE", "ZM", "WMT", "TGT", "COST", "HD", 
            "MCD", "SBUX", "NKE", "KO", "PEP", "UNH", "JNJ", "PFE", "MRNA", 
            "CVS", "BRK-B", "BRK.A", "JPM", "BAC", "GS", "AXP", "V", "MA", 
            "XOM", "CVX", "BA", "CAT", "GE", "DIS", "CMCSA", "VZ", "T"
        ]
        
        words = query.upper().split()
        for word in words:
            clean_word = re.sub(r'[^\w.-]', '', word)
            if clean_word in known_tickers:
                return clean_word
        
        # Look for $ symbol followed by ticker
        dollar_match = re.search(r'\$([A-Z.-]{1,6})\b', query.upper())
        if dollar_match:
            return dollar_match.group(1)
        
        return None
    
    def _handle_price_query(self, query: str) -> Dict[str, Any]:
        """Handle stock price queries"""
        ticker = self._extract_ticker(query)
        if not ticker:
            return {"type": "error", "message": "Please specify a stock ticker (e.g., AAPL, TSLA)"}
        
        data = self.yahoo_service.get_stock_data(ticker)
        if "error" in data:
            return {"type": "error", "message": f"Could not get price for {ticker}: {data['error']}"}
        
        return {
            "type": "price",
            "ticker": ticker,
            "data": data,
            "message": f"{ticker} is currently trading at ${data['current_price']:.2f}"
        }
    
    def _handle_company_query(self, query: str) -> Dict[str, Any]:
        """Handle company information queries"""
        ticker = self._extract_ticker(query)
        if not ticker:
            return {"type": "error", "message": "Please specify a company or ticker"}
        
        data = self.yahoo_service.get_stock_data(ticker)
        if "error" in data:
            return {"type": "error", "message": f"Could not find information for {ticker}"}
        
        return {
            "type": "company",
            "ticker": ticker,
            "data": data,
            "message": f"Here's information about {data.get('company_name', ticker)}"
        }
    
    def _handle_technical_query(self, query: str) -> Dict[str, Any]:
        """Handle technical analysis queries"""
        ticker = self._extract_ticker(query)
        if not ticker:
            return {"type": "error", "message": "Please specify a stock ticker for technical analysis"}
        
        data = self.yahoo_service.get_technical_indicators(ticker)
        if "error" in data:
            return {"type": "error", "message": f"Could not get technical analysis for {ticker}"}
        
        # Get company information first
        company_data = self.yahoo_service.get_stock_data(ticker)
        company_name = company_data.get('company_name', ticker) if "error" not in company_data else ticker
        sector = company_data.get('sector', 'Unknown') if "error" not in company_data else 'Unknown'
        market_cap = company_data.get('market_cap') if "error" not in company_data else None
        
        # Generate comprehensive technical analysis
        message = f"TECHNICAL ANALYSIS REPORT\n"
        message += f"Company: {company_name} ({ticker})\n"
        message += f"Sector: {sector}\n"
        if market_cap:
            message += f"Market Cap: ${market_cap:,.0f}\n"
        message += f"{'-' * 50}\n\n"
        
        # Price Analysis
        price_data = data.get("price_data", {})
        if price_data:
            current = price_data.get("current_price")
            high_6m = price_data.get("high_6m")
            low_6m = price_data.get("low_6m")
            volume_avg = price_data.get("volume_avg")
            
            message += f"PRICE ANALYSIS:\n"
            if current:
                message += f"Current Price: ${current:.2f}\n"
            if high_6m and low_6m:
                range_position = ((current - low_6m) / (high_6m - low_6m)) * 100
                message += f"6-Month High: ${high_6m:.2f}\n"
                message += f"6-Month Low: ${low_6m:.2f}\n"
                message += f"Position in Range: {range_position:.1f}%\n"
            if volume_avg:
                message += f"Average Volume: {volume_avg:,.0f}\n"
            message += f"\n"
        
        # Technical Indicators
        indicators = data.get("indicators", {})
        message += f"TECHNICAL INDICATORS:\n"
        
        # RSI Analysis
        rsi_data = indicators.get("rsi", {})
        rsi = rsi_data.get("current")
        if rsi:
            message += f"RSI (14-day): {rsi:.2f}\n"
            if rsi > 70:
                message += f"Signal: OVERBOUGHT - Potential sell signal\n"
            elif rsi < 30:
                message += f"Signal: OVERSOLD - Potential buy signal\n"
            else:
                message += f"Signal: NEUTRAL - No strong directional bias\n"
        
        # Moving Averages
        ma_data = indicators.get("moving_averages", {})
        if ma_data:
            message += f"\nMOVING AVERAGES:\n"
            if ma_data.get("sma_20"):
                message += f"SMA 20: ${ma_data['sma_20']:.2f}\n"
            if ma_data.get("sma_50"):
                message += f"SMA 50: ${ma_data['sma_50']:.2f}\n"
            if ma_data.get("ema_12"):
                message += f"EMA 12: ${ma_data['ema_12']:.2f}\n"
            if ma_data.get("ema_26"):
                message += f"EMA 26: ${ma_data['ema_26']:.2f}\n"
        
        # Bollinger Bands
        bb_data = indicators.get("bollinger_bands", {})
        if bb_data and bb_data.get("upper"):
            message += f"\nBOLLINGER BANDS:\n"
            message += f"Upper Band: ${bb_data['upper']:.2f}\n"
            message += f"Middle Band: ${bb_data['middle']:.2f}\n"
            message += f"Lower Band: ${bb_data['lower']:.2f}\n"
            
            if current:
                if current > bb_data['upper']:
                    message += f"Position: Above upper band (overbought)\n"
                elif current < bb_data['lower']:
                    message += f"Position: Below lower band (oversold)\n"
                else:
                    message += f"Position: Within bands (normal range)\n"
        
        return {
            "type": "technical",
            "ticker": ticker,
            "data": data,
            "message": message
        }
    
    def _handle_analysis_query(self, query: str) -> Dict[str, Any]:
        """Handle comprehensive analysis queries"""
        ticker = self._extract_ticker(query)
        if not ticker:
            return {"type": "error", "message": "Please specify a company for analysis"}
        
        # Get both stock data and technical indicators
        stock_data = self.yahoo_service.get_stock_data(ticker)
        if "error" in stock_data:
            return {"type": "error", "message": f"Could not analyze {ticker}: {stock_data['error']}"}
        
        tech_data = self.yahoo_service.get_technical_indicators(ticker)
        
        # Create comprehensive analysis
        company_name = stock_data.get('company_name', ticker)
        current_price = stock_data.get('current_price', 0)
        change = stock_data.get('change', 0)
        change_percent = stock_data.get('change_percent', 0)
        market_cap = stock_data.get('market_cap')
        sector = stock_data.get('sector', 'Unknown')
        industry = stock_data.get('industry', 'Unknown')
        volume = stock_data.get('volume', 0)
        
        message = f"COMPREHENSIVE COMPANY ANALYSIS\n"
        message += f"{'=' * 50}\n\n"
        
        message += f"COMPANY OVERVIEW:\n"
        message += f"Name: {company_name}\n"
        message += f"Ticker: {ticker}\n"
        message += f"Sector: {sector}\n"
        message += f"Industry: {industry}\n"
        if market_cap:
            cap_category = ""
            if market_cap > 200e9:
                cap_category = " (Large Cap)"
            elif market_cap > 10e9:
                cap_category = " (Mid Cap)"
            elif market_cap > 2e9:
                cap_category = " (Small Cap)"
            else:
                cap_category = " (Micro Cap)"
            message += f"Market Capitalization: ${market_cap:,.0f}{cap_category}\n"
        message += f"\n"
        
        message += f"CURRENT TRADING DATA:\n"
        message += f"Current Price: ${current_price:.2f}\n"
        message += f"Daily Change: ${change:.2f} ({change_percent:+.2f}%)\n"
        if volume:
            message += f"Today's Volume: {volume:,} shares\n"
        
        # Add detailed technical analysis if available
        if "error" not in tech_data:
            message += f"\nTECHNICAL INDICATORS:\n"
            
            rsi = tech_data.get("indicators", {}).get("rsi", {}).get("current")
            if rsi:
                message += f"RSI (14-day): {rsi:.2f}\n"
                if rsi > 70:
                    message += f"RSI Signal: OVERBOUGHT (Potential selling opportunity)\n"
                elif rsi < 30:
                    message += f"RSI Signal: OVERSOLD (Potential buying opportunity)\n"
                else:
                    message += f"RSI Signal: NEUTRAL (No strong directional bias)\n"
            
            # Moving averages analysis
            ma_data = tech_data.get("indicators", {}).get("moving_averages", {})
            if ma_data:
                sma_20 = ma_data.get("sma_20")
                sma_50 = ma_data.get("sma_50")
                
                if sma_20 and sma_50:
                    message += f"Moving Averages: SMA20(${sma_20:.2f}) vs SMA50(${sma_50:.2f})\n"
                    if sma_20 > sma_50:
                        message += f"Trend: BULLISH (SMA20 above SMA50)\n"
                    else:
                        message += f"Trend: BEARISH (SMA20 below SMA50)\n"
            
            # Price position analysis
            price_data = tech_data.get("price_data", {})
            if price_data:
                high_6m = price_data.get("high_6m")
                low_6m = price_data.get("low_6m")
                
                if high_6m and low_6m and current_price:
                    range_position = ((current_price - low_6m) / (high_6m - low_6m)) * 100
                    message += f"6-Month Range: ${low_6m:.2f} - ${high_6m:.2f}\n"
                    message += f"Current Position: {range_position:.1f}% of range\n"
                    
                    if range_position > 80:
                        message += f"Price Level: Near 6-month highs\n"
                    elif range_position < 20:
                        message += f"Price Level: Near 6-month lows\n"
                    else:
                        message += f"Price Level: Mid-range\n"
        
        return {
            "type": "analysis",
            "ticker": ticker,
            "data": {
                "stock_data": stock_data,
                "technical_data": tech_data
            },
            "message": message
        }
    
    def _handle_performance_query(self, query: str) -> Dict[str, Any]:
        """Handle financial performance queries"""
        ticker = self._extract_ticker(query)
        if not ticker:
            return {"type": "error", "message": "Please specify a company for performance data"}
        
        data = self.yahoo_service.get_stock_data(ticker)
        if "error" in data:
            return {"type": "error", "message": f"Could not get performance data for {ticker}"}
        
        # Create performance-focused response
        company_name = data.get('company_name', ticker)
        current_price = data.get('current_price', 0)
        change = data.get('change', 0)
        change_percent = data.get('change_percent', 0)
        market_cap = data.get('market_cap')
        sector = data.get('sector', 'Unknown')
        industry = data.get('industry', 'Unknown')
        volume = data.get('volume', 0)
        
        message = f"FINANCIAL PERFORMANCE ANALYSIS\n"
        message += f"Company: {company_name} ({ticker})\n"
        message += f"{'=' * 50}\n\n"
        
        message += f"STOCK PERFORMANCE:\n"
        message += f"Current Price: ${current_price:.2f}\n"
        message += f"Daily Change: ${change:.2f} ({change_percent:+.2f}%)\n"
        
        if market_cap:
            message += f"\nVALUATION:\n"
            if market_cap > 1e12:
                message += f"Market Cap: ${market_cap/1e12:.2f}T (Mega-cap stock)\n"
            elif market_cap > 200e9:
                message += f"Market Cap: ${market_cap/1e9:.1f}B (Large-cap stock)\n"
            elif market_cap > 10e9:
                message += f"Market Cap: ${market_cap/1e9:.1f}B (Mid-cap stock)\n"
            elif market_cap > 2e9:
                message += f"Market Cap: ${market_cap/1e9:.1f}B (Small-cap stock)\n"
            else:
                message += f"Market Cap: ${market_cap/1e6:.0f}M (Micro-cap stock)\n"
        
        message += f"\nCOMPANY DETAILS:\n"
        message += f"Sector: {sector}\n"
        message += f"Industry: {industry}\n"
        
        if volume:
            message += f"\nTRADING ACTIVITY:\n"
            message += f"Volume Today: {volume:,} shares\n"
            
            # Volume analysis
            if volume > 50000000:
                message += f"Activity Level: Very High Volume\n"
            elif volume > 10000000:
                message += f"Activity Level: High Volume\n"
            elif volume > 1000000:
                message += f"Activity Level: Moderate Volume\n"
            else:
                message += f"Activity Level: Low Volume\n"
        
        return {
            "type": "performance",
            "ticker": ticker,
            "data": data,
            "message": message
        }
    
    def _handle_general_query(self, query: str) -> Dict[str, Any]:
        """Handle general queries with helpful suggestions"""
        # Try to extract a ticker even for general queries
        ticker = self._extract_ticker(query)
        
        if ticker:
            # If we found a ticker, provide basic info
            data = self.yahoo_service.get_stock_data(ticker)
            if "error" not in data:
                company_name = data.get('company_name', ticker)
                current_price = data.get('current_price', 0)
                
                return {
                    "type": "general",
                    "ticker": ticker,
                    "data": data,
                    "message": f"I found information about {company_name} ({ticker}). Current price: ${current_price:.2f}. Try asking more specific questions like 'analyze {company_name}' or 'technical analysis of {ticker}'"
                }
        
        # General help response
        return {
            "type": "help",
            "message": "I can help you with stock analysis! Try asking questions like:",
            "suggestions": [
                "Analyze Apple",
                "What's Tesla's performance?",
                "Technical analysis of Microsoft",
                "How is Amazon doing?",
                "Show me Apple's RSI",
                "What's the price of Google?"
            ]
        }
