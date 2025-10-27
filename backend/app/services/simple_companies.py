"""
Simple Company Service - Gets real-time Fortune 100 companies by market value

This service gets the top 100 companies by market value using Yahoo Finance.
Easy to understand and modify!
"""
import yfinance as yf
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

# Create a logger to track what happens
logger = logging.getLogger(__name__)

class SimpleCompanyService:
    """Simple service that gets top companies by market value"""
    
    def __init__(self):
        """Set up the service"""
        self.companies = []
        self.last_updated = None
        self.update_interval = timedelta(hours=6)  # Update every 6 hours
        self.executor = ThreadPoolExecutor(max_workers=10)
        
        # List of major US company stock symbols
        self.major_symbols = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-A', 'UNH', 'JNJ',
            'JPM', 'V', 'PG', 'XOM', 'HD', 'CVX', 'MA', 'PFE', 'ABBV', 'BAC',
            'KO', 'AVGO', 'PEP', 'TMO', 'WMT', 'COST', 'DIS', 'ABT', 'MRK', 'ACN',
            'VZ', 'NFLX', 'CRM', 'DHR', 'LIN', 'TXN', 'NKE', 'WFC', 'RTX', 'UPS',
            'QCOM', 'HON', 'T', 'MDT', 'LOW', 'UNP', 'IBM', 'INTC', 'CAT', 'SPGI',
            'AXP', 'GS', 'BLK', 'INTU', 'ISRG', 'NEE', 'PLD', 'BA', 'TJX', 'AMD',
            'SCHW', 'SYK', 'AMAT', 'CVS', 'DE', 'LMT', 'ADI', 'MDLZ', 'GILD', 'ADP',
            'CI', 'MMC', 'TMUS', 'TGT', 'SO', 'BMY', 'CL', 'MO', 'ZTS', 'SHW',
            'CB', 'DUK', 'ITW', 'CSX', 'CME', 'EQIX', 'ICE', 'AON', 'PYPL', 'WM',
            'COP', 'USB', 'GD', 'NSC', 'SBUX', 'FCX', 'APD', 'HUM', 'MCD', 'ECL'
        ]
    
    async def update_companies(self):
        """Update the company database with real-time data"""
        try:
            logger.info("Starting company database update...")
            
            # Get company data for all symbols
            company_data = await self.get_all_company_data()
            
            if company_data:
                # Sort companies by market value (biggest first)
                company_data.sort(key=lambda x: x.get('market_cap', 0), reverse=True)
                
                # Store the top 100 companies
                self.companies = company_data[:100]
                self.last_updated = datetime.now()
                
                logger.info(f"Updated {len(self.companies)} companies successfully!")
                return True
            else:
                logger.warning("No company data received")
                return False
                
        except Exception as e:
            logger.error(f"Error updating companies: {e}")
            return False
    
    async def get_all_company_data(self):
        """Get data for all companies using parallel processing"""
        try:
            loop = asyncio.get_event_loop()
            
            # Create tasks to get all company data at once
            tasks = []
            for symbol in self.major_symbols:
                task = loop.run_in_executor(self.executor, self.get_single_company, symbol)
                tasks.append(task)
            
            # Wait for all tasks to finish
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter out any failed results
            valid_companies = []
            for result in results:
                if result is not None and not isinstance(result, Exception):
                    valid_companies.append(result)
            
            logger.info(f"Successfully got data for {len(valid_companies)} companies")
            return valid_companies
            
        except Exception as e:
            logger.error(f"Error getting company data: {e}")
            return []
    
    def get_single_company(self, symbol):
        """Get data for a single company"""
        try:
            # Get company information from Yahoo Finance
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # Extract basic company information
            company_name = info.get('longName', symbol)
            sector = info.get('sector', 'Unknown')
            industry = info.get('industry', 'Unknown')
            market_cap = info.get('marketCap', 0)
            employees = info.get('fullTimeEmployees', 'N/A')
            
            # Get financial data - try multiple field names
            revenue = (info.get('totalRevenue') or 
                      info.get('revenue') or 
                      info.get('totalRevenueTTM') or
                      info.get('revenueQuarterlyGrowth'))
            
            revenue_formatted = None
            if revenue and isinstance(revenue, (int, float)) and revenue > 0:
                # Convert to billions for readability
                if revenue >= 1e9:
                    revenue_formatted = f"${revenue/1e9:.1f}B"
                elif revenue >= 1e6:
                    revenue_formatted = f"${revenue/1e6:.1f}M"
                else:
                    revenue_formatted = f"${revenue/1e3:.1f}K"
            
            # Get profit data - try multiple field names
            profit = (info.get('netIncomeToCommon') or 
                     info.get('netIncome') or
                     info.get('trailingEps', 0) * info.get('sharesOutstanding', 0) if 
                     info.get('trailingEps') and info.get('sharesOutstanding') else None)
            
            profit_formatted = None
            if profit and isinstance(profit, (int, float)) and profit > 0:
                # Convert to billions for readability
                if profit >= 1e9:
                    profit_formatted = f"${profit/1e9:.1f}B"
                elif profit >= 1e6:
                    profit_formatted = f"${profit/1e6:.1f}M"
                else:
                    profit_formatted = f"${profit/1e3:.1f}K"
            
            # Skip companies without market cap data
            if not market_cap or market_cap == 0:
                return None
            
            # Create company data dictionary
            company_data = {
                'rank': 0,  # Will be set after sorting
                'company': company_name,
                'ticker': symbol,
                'sector': sector,
                'industry': industry,
                'market_cap': market_cap,
                'employees': employees,
                'revenue': revenue_formatted,  # Add formatted revenue
                'profit': profit_formatted,    # Add formatted profit
                'name': company_name  # For compatibility
            }
            
            return company_data
            
        except Exception as e:
            logger.error(f"Error getting data for {symbol}: {e}")
            return None
    
    async def get_top_companies(self, limit=20):
        """Get the top companies by market value"""
        # Update data if it's old or empty
        await self.ensure_fresh_data()
        
        # Return the requested number of companies
        companies_to_return = self.companies[:limit]
        
        # Add rank numbers
        for i, company in enumerate(companies_to_return):
            company['rank'] = i + 1
        
        return companies_to_return
    
    async def get_company_by_ticker(self, ticker):
        """Find a company by its stock symbol"""
        # Update data if needed
        await self.ensure_fresh_data()
        
        # Look for the company
        for company in self.companies:
            if company['ticker'].upper() == ticker.upper():
                return company
        
        # If not found, try to get it directly
        company_data = self.get_single_company(ticker.upper())
        if company_data:
            return company_data
        
        return None
    
    async def search_companies(self, search_term):
        """Search for companies by name with flexible matching and common aliases"""
        # Update data if needed
        await self.ensure_fresh_data()
        
        search_term = search_term.lower().strip()
        matching_companies = []
        
        # Common company aliases/alternative names
        aliases = {
            "google": "alphabet",
            "facebook": "meta", 
            "fb": "meta",
            "tesla motors": "tesla",
            "gm": "general motors", 
            "ge": "general electric",
            "jpmorgan": "jpmorgan chase",
            "jp morgan": "jpmorgan chase",
            "jpm": "jpmorgan chase",
            "coca cola": "coca-cola",
            "coke": "coca-cola",
            "pepsi": "pepsico",
            "mcdonalds": "mcdonald",
            "mc donald": "mcdonald",
            "walmart": "wal-mart",
            "berkshire": "berkshire hathaway",
            "visa inc": "visa",
            "mastercard inc": "mastercard"
        }
        
        # Check if search term has a known alias
        original_search = search_term
        if search_term in aliases:
            search_term = aliases[search_term]
        
        # Look for matches in company names with different strategies
        for company in self.companies:
            company_name = company['company'].lower()
            ticker = company['ticker'].lower()
            
            # Exact ticker match (highest priority)
            if original_search == ticker or search_term == ticker:
                matching_companies.insert(0, company)
                continue
            
            # Exact company name match (high priority)
            if original_search == company_name or search_term == company_name:
                matching_companies.insert(0, company)
                continue
                
            # Company name contains search term (either original or alias)
            if original_search in company_name or search_term in company_name:
                matching_companies.append(company)
                continue
                
            # Company name words start with search term
            company_words = company_name.split()
            for word in company_words:
                if word.startswith(original_search) or word.startswith(search_term):
                    matching_companies.append(company)
                    break
        
        # Remove duplicates while preserving order
        seen = set()
        unique_matches = []
        for company in matching_companies:
            if company['ticker'] not in seen:
                seen.add(company['ticker'])
                unique_matches.append(company)
        
        return unique_matches[:10]  # Return top 10 matches
    
    async def ensure_fresh_data(self):
        """Make sure we have recent company data"""
        # Check if we need to update the data
        if (not self.companies or 
            not self.last_updated or 
            datetime.now() - self.last_updated > self.update_interval):
            
            logger.info("Company data is old, updating...")
            await self.update_companies()
    
    def get_cache_info(self):
        """Get information about the cached data"""
        return {
            'total_companies': len(self.companies),
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'update_interval_hours': self.update_interval.total_seconds() / 3600
        }
