"""
Simple OpenAI Financial AI Service

This service uses OpenAI to answer financial questions with real-time stock data.
Easy to understand and modify!
"""

import logging
import os
from openai import AsyncOpenAI
from datetime import datetime

# Create a logger to track what happens
logger = logging.getLogger(__name__)

class OpenAIFinancialAI:
    """Simple AI helper that answers financial questions"""
    
    def __init__(self, stock_service, company_service):
        # Store the services we need
        self.stock_service = stock_service
        self.company_service = company_service
        self.client = None
        self.setup_openai_client()
    
    
    def setup_openai_client(self):
        """Set up OpenAI client"""
        try:
            # Get API key from environment variable
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                logger.error("OPENAI_API_KEY environment variable not set")
                return
            
            self.client = AsyncOpenAI(api_key=api_key)
            logger.info("OpenAI client ready!")
        except Exception as e:
            logger.error(f"Failed to setup OpenAI client: {e}")
    
    async def answer_question(self, question):
        """Main method that answers financial questions using AI"""
        try:
            if not self.client:
                return {
                    "type": "error", 
                    "message": "AI service not available. Please check OpenAI API key."
                }
            
            # Find companies mentioned in the question
            companies = await self.find_companies_in_question(question)
            
            # Get real-time stock data for the companies
            financial_data = await self.get_financial_data(companies)
            
            # Create prompts for OpenAI
            system_prompt = self.create_system_prompt()
            user_prompt = self.create_user_prompt(question, financial_data)
            
            # Ask OpenAI to answer the question
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.3  # Lower = more factual, Higher = more creative
            )
            
            ai_answer = response.choices[0].message.content
            
            # Figure out what type of response this is
            response_type = self.figure_out_response_type(question, ai_answer)
            
            return {
                "type": response_type,
                "message": ai_answer,
                "companies_analyzed": companies,
                "has_real_time_data": len(financial_data) > 0,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return {
                "type": "error", 
                "message": "I'm having trouble processing your request. Please try again in a moment."
            }
    
    async def process_query(self, query):
        """Process a query - this is an alias for answer_question to match the router expectations"""
        return await self.answer_question(query)
    
    async def find_companies_in_question(self, question):
        """Find company names or stock symbols in the question using dynamic search"""
        companies = []
        question_lower = question.lower()
        
        # Extract potential company names/tickers from the question
        words = question.split()
        potential_searches = []
        
        # Look for potential stock tickers (2-5 uppercase letters)
        for word in words:
            clean_word = word.strip('.,!?()[]{}":;')
            if len(clean_word) >= 2 and len(clean_word) <= 5 and clean_word.isupper():
                potential_searches.append(clean_word)
        
        # Look for common company words and extract surrounding context
        company_indicators = ['corporation', 'corp', 'company', 'inc', 'ltd', 'llc', 'group', 'holdings']
        for i, word in enumerate(words):
            word_lower = word.lower().strip('.,!?()[]{}":;')
            if word_lower in company_indicators:
                # Get 1-2 words before the indicator
                start = max(0, i-2)
                company_phrase = ' '.join(words[start:i+1])
                potential_searches.append(company_phrase.strip('.,!?()[]{}":;'))
        
        # Also add individual words that might be company names
        for word in words:
            clean_word = word.strip('.,!?()[]{}":;')
            if len(clean_word) > 2 and clean_word.isalpha():
                potential_searches.append(clean_word)
        
        # Search for each potential company using the company service
        for search_term in potential_searches[:10]:  # Limit searches
            try:
                search_results = await self.company_service.search_companies(search_term)
                if search_results:
                    # Take the best match (first result)
                    best_match = search_results[0]
                    ticker = best_match.get('ticker')
                    if ticker and ticker not in companies:
                        companies.append(ticker)
                        if len(companies) >= 5:  # Limit to 5 companies max
                            break
            except Exception as e:
                logger.warning(f"Error searching for company '{search_term}': {e}")
                continue
        
        return companies
    
    async def get_financial_data(self, companies):
        """Get real-time financial data for companies"""
        data = {
            "market_timestamp": datetime.now().isoformat(),
            "companies": {}
        }
        
        for ticker in companies:
            try:
                # Get company information (async)
                company_info = await self.company_service.get_company_by_ticker(ticker)
                
                # Get real-time stock data (sync)
                stock_info = self.stock_service.get_stock_data(ticker)
                
                if company_info and stock_info and 'error' not in stock_info:
                    data["companies"][ticker] = {
                        "basic_info": {
                            "name": company_info.get('name', 'Unknown'),
                            "sector": company_info.get('sector', 'Unknown'),
                            "market_cap": company_info.get('market_cap', 'N/A'),
                            "employees": company_info.get('employees', 'N/A')
                        },
                        "current_price": stock_info.get('current_price', 'N/A'),
                        "price_change": stock_info.get('price_change', 'N/A'),
                        "change_percent": stock_info.get('change_percent', 'N/A'),
                        "volume": stock_info.get('volume', 'N/A'),
                        "day_high": stock_info.get('day_high', 'N/A'),
                        "day_low": stock_info.get('day_low', 'N/A'),
                        "year_high": stock_info.get('year_high', 'N/A'),
                        "year_low": stock_info.get('year_low', 'N/A'),
                        "pe_ratio": stock_info.get('pe_ratio', 'N/A'),
                        "market_cap_current": stock_info.get('market_cap', 'N/A')
                    }
                    
                    logger.info(f"Got real-time data for {ticker}: ${stock_info.get('current_price', 'N/A')}")
                
            except Exception as e:
                logger.error(f"Error getting data for {ticker}: {e}")
                continue
        
        return data
    
    def create_system_prompt(self):
        """Create the instructions for the AI"""
        return """You are a helpful financial AI assistant with access to real-time stock market data. 

What you can do:
- Answer questions about stock prices and company performance
- Compare different companies using real financial data
- Explain financial concepts in simple terms
- Give investment insights based on current market data

How to respond:
- Use the real-time financial data provided in your responses
- Be factual and cite specific numbers when available
- For comparisons, look at price, performance, and company fundamentals
- Explain your reasoning clearly and simply
- Always mention this is for educational purposes, not financial advice
- If you don't have enough data, be honest about it
- Format responses clearly with bullet points and sections

Important: Always remind users that investment decisions require personal research and professional advice."""
    
    def create_user_prompt(self, question, financial_data):
        """Create the user prompt with question and real-time data"""
        prompt = f"User Question: {question}\n\n"
        
        if financial_data.get("companies"):
            prompt += "REAL-TIME FINANCIAL DATA:\n"
            prompt += f"Data Timestamp: {financial_data['market_timestamp']}\n\n"
            
            for ticker, company_data in financial_data["companies"].items():
                prompt += f"**{ticker} - {company_data['basic_info']['name']}**\n"
                prompt += f"- Sector: {company_data['basic_info']['sector']}\n"
                prompt += f"- Current Price: ${company_data['current_price']}\n"
                prompt += f"- Price Change: {company_data['price_change']} ({company_data['change_percent']})\n"
                prompt += f"- Day Range: ${company_data['day_low']} - ${company_data['day_high']}\n"
                prompt += f"- 52-Week Range: ${company_data['year_low']} - ${company_data['year_high']}\n"
                prompt += f"- Volume: {company_data['volume']}\n"
                prompt += f"- P/E Ratio: {company_data['pe_ratio']}\n"
                prompt += f"- Market Cap: {company_data['market_cap_current']}\n"
                prompt += f"- Employees: {company_data['basic_info']['employees']}\n\n"
        else:
            prompt += "Note: No specific companies found in the question or real-time data unavailable.\n\n"
        
        prompt += "Please provide a helpful response using the real-time data above. If this is a comparison question, analyze all companies. If it's a general financial question, provide educational insights."
        
        return prompt
    
    def figure_out_response_type(self, question, response):
        """Figure out what type of response this is based on the question"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['compare', 'versus', 'vs', 'which is better', 'between']):
            return 'comparison'
        elif any(word in question_lower for word in ['price', 'cost', 'trading at', 'worth', 'value']):
            return 'price'
        elif any(word in question_lower for word in ['analysis', 'analyze', 'performance', 'technical']):
            return 'analysis'
        elif any(word in question_lower for word in ['company', 'business', 'about', 'information']):
            return 'company'
        elif any(word in question_lower for word in ['how to', 'strategy', 'invest', 'should i']):
            return 'strategy'
        elif any(word in question_lower for word in ['what is', 'explain', 'define', 'how does']):
            return 'education'
        else:
            return 'general'
