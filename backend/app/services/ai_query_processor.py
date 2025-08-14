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
        """Process a natural language query and return results"""
        query = query.lower().strip()
        
        try:
            # Stock price queries
            if self._is_price_query(query):
                return self._handle_price_query(query)
            
            # Company search queries
            elif self._is_company_query(query):
                return self._handle_company_query(query)
            
            # Technical analysis queries
            elif self._is_technical_query(query):
                return self._handle_technical_query(query)
            
            else:
                return {
                    "type": "unknown",
                    "message": "Sorry, I didn't understand your query. Try asking about stock prices, company information, or technical analysis.",
                    "suggestions": [
                        "What is the price of AAPL?",
                        "Tell me about Apple",
                        "Show RSI for TSLA"
                    ]
                }
                
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
    
    def _is_technical_query(self, query: str) -> bool:
        """Check if query is asking for technical analysis"""
        technical_keywords = ["rsi", "bollinger", "moving average", "technical", "analysis", "indicator"]
        return any(keyword in query for keyword in technical_keywords)
    
    def _extract_ticker(self, query: str) -> str:
        """Extract stock ticker from query"""
        # Look for common ticker patterns
        ticker_patterns = [
            r'\b([A-Z]{1,5})\b',  # 1-5 uppercase letters
            r'\$([A-Z]{1,5})\b',  # $ followed by letters
        ]
        
        for pattern in ticker_patterns:
            match = re.search(pattern, query.upper())
            if match:
                return match.group(1)
        
        # If no ticker found, try common company names
        company_map = {
            "apple": "AAPL",
            "tesla": "TSLA", 
            "amazon": "AMZN",
            "google": "GOOGL",
            "microsoft": "MSFT",
            "meta": "META",
            "netflix": "NFLX"
        }
        
        for company, ticker in company_map.items():
            if company in query:
                return ticker
        
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
        
        return {
            "type": "technical",
            "ticker": ticker,
            "data": data,
            "message": f"Here's the technical analysis for {ticker}"
        }
