"""
Dynamic Company Service - Fetches real-time Fortune 100 companies by market cap

This service dynamically fetches the top 100 companies by market capitalization
using Yahoo Finance API and stores them in an in-memory database.
No more static data!
"""
import yfinance as yf
import pandas as pd
import logging
from typing import List, Dict, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class DynamicCompanyService:
    """A service that dynamically fetches top companies by market cap"""
    
    def __init__(self):
        """Initialize the service"""
        self.companies = []
        self.last_updated = None
        self.update_interval = timedelta(hours=6)  # Update every 6 hours
        self.executor = ThreadPoolExecutor(max_workers=10)
        
        # S&P 500 tickers - we'll use these as our source for top companies
        # This is a curated list of major US companies
        self.sp500_tickers = [
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
    
    async def update_companies(self) -> bool:
        """Update the company database with real-time data"""
        try:
            logger.info("Starting dynamic company database update...")
            
            # Get company data in parallel for better performance
            company_data = await self._fetch_companies_parallel()
            
            if not company_data:
                logger.error("Failed to fetch any company data")
                return False
            
            # Sort by market cap (highest first) and take top 100
            sorted_companies = sorted(
                company_data, 
                key=lambda x: x.get('market_cap', 0), 
                reverse=True
            )
            
            self.companies = sorted_companies[:100]
            self.last_updated = datetime.now()
            
            logger.info(f"Successfully updated {len(self.companies)} companies")
            return True
            
        except Exception as e:
            logger.error(f"Error updating companies: {e}")
            return False
    
    async def _fetch_companies_parallel(self) -> List[Dict]:
        """Fetch company data in parallel for better performance"""
        try:
            loop = asyncio.get_event_loop()
            
            # Create tasks for parallel execution
            tasks = [
                loop.run_in_executor(
                    self.executor, 
                    self._fetch_single_company, 
                    ticker
                ) 
                for ticker in self.sp500_tickers
            ]
            
            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter out None results and exceptions
            company_data = [
                result for result in results 
                if result is not None and not isinstance(result, Exception)
            ]
            
            return company_data
            
        except Exception as e:
            logger.error(f"Error in parallel fetch: {e}")
            return []
    
    def _fetch_single_company(self, ticker: str) -> Optional[Dict]:
        """Fetch data for a single company"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get basic company information
            company_name = info.get('longName', ticker)
            sector = info.get('sector', 'Unknown')
            industry = info.get('industry', 'Unknown')
            market_cap = info.get('marketCap', 0)
            
            # Skip companies without market cap data
            if not market_cap or market_cap == 0:
                return None
            
            # Get recent price data
            hist = stock.history(period="5d")
            if hist.empty:
                return None
            
            current_price = float(hist['Close'].iloc[-1])
            
            # Calculate revenue and profit (in millions)
            revenue = info.get('totalRevenue', 0) // 1_000_000 if info.get('totalRevenue') else 0
            net_income = info.get('netIncomeToCommon', 0) // 1_000_000 if info.get('netIncomeToCommon') else 0
            
            return {
                'company': company_name,
                'ticker': ticker.upper(),
                'sector': sector,
                'industry': industry,
                'market_cap': market_cap,
                'current_price': current_price,
                'revenue': revenue,
                'profit': net_income,
                'rank': 0  # Will be set later based on market cap ranking
            }
            
        except Exception as e:
            logger.warning(f"Failed to fetch data for {ticker}: {e}")
            return None
    
    async def ensure_updated(self) -> bool:
        """Ensure the company data is up to date"""
        if (self.last_updated is None or 
            datetime.now() - self.last_updated > self.update_interval or
            not self.companies):
            
            return await self.update_companies()
        return True
    
    async def get_top_companies(self, limit: int = 20) -> List[Dict]:
        """Get the top companies by market cap"""
        try:
            await self.ensure_updated()
            
            # Assign ranks based on current order (sorted by market cap)
            ranked_companies = []
            for i, company in enumerate(self.companies[:limit]):
                company_copy = company.copy()
                company_copy['rank'] = i + 1
                ranked_companies.append(company_copy)
            
            return ranked_companies
            
        except Exception as e:
            logger.error(f"Error getting top companies: {e}")
            return []
    
    async def get_company_by_ticker(self, ticker: str) -> Optional[Dict]:
        """Find a company by its ticker symbol"""
        try:
            await self.ensure_updated()
            
            ticker = ticker.upper()
            for i, company in enumerate(self.companies):
                if company['ticker'] == ticker:
                    company_copy = company.copy()
                    company_copy['rank'] = i + 1
                    return company_copy
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding company {ticker}: {e}")
            return None
    
    async def get_company_by_name(self, name: str) -> Optional[Dict]:
        """Find a company by its name"""
        try:
            await self.ensure_updated()
            
            name = name.lower()
            for i, company in enumerate(self.companies):
                if name in company['company'].lower():
                    company_copy = company.copy()
                    company_copy['rank'] = i + 1
                    return company_copy
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding company {name}: {e}")
            return None
    
    async def search_companies(self, search_term: str) -> List[Dict]:
        """Search for companies by name, ticker, or sector"""
        try:
            await self.ensure_updated()
            
            search_term = search_term.lower()
            results = []
            
            for i, company in enumerate(self.companies):
                if (search_term in company['company'].lower() or 
                    search_term in company['ticker'].lower() or
                    search_term in company['sector'].lower() or
                    search_term in company['industry'].lower()):
                    
                    company_copy = company.copy()
                    company_copy['rank'] = i + 1
                    results.append(company_copy)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching companies: {e}")
            return []
    
    async def get_companies_by_sector(self, sector: str) -> List[Dict]:
        """Get all companies in a specific sector"""
        try:
            await self.ensure_updated()
            
            sector = sector.lower()
            results = []
            
            for i, company in enumerate(self.companies):
                if sector in company['sector'].lower():
                    company_copy = company.copy()
                    company_copy['rank'] = i + 1
                    results.append(company_copy)
            
            return results
            
        except Exception as e:
            logger.error(f"Error getting sector {sector}: {e}")
            return []
    
    async def get_companies_by_industry(self, industry: str) -> List[Dict]:
        """Get all companies in a specific industry"""
        try:
            await self.ensure_updated()
            
            industry = industry.lower()
            results = []
            
            for i, company in enumerate(self.companies):
                if industry in company['industry'].lower():
                    company_copy = company.copy()
                    company_copy['rank'] = i + 1
                    results.append(company_copy)
            
            return results
            
        except Exception as e:
            logger.error(f"Error getting industry {industry}: {e}")
            return []
    
    async def get_all_sectors(self) -> List[str]:
        """Get list of all sectors"""
        try:
            await self.ensure_updated()
            
            sectors = set()
            for company in self.companies:
                sectors.add(company['sector'])
            
            return sorted(list(sectors))
            
        except Exception as e:
            logger.error(f"Error getting sectors: {e}")
            return []
    
    async def get_company_info(self, company_name: str) -> Optional[Dict]:
        """Get detailed information about a specific company"""
        try:
            # First try to find by ticker
            company = await self.get_company_by_ticker(company_name)
            if company:
                return company
            
            # If not found by ticker, try by name
            company = await self.get_company_by_name(company_name)
            if company:
                return company
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting company info for {company_name}: {e}")
            return None
    
    def get_cache_info(self) -> Dict:
        """Get information about the current cache state"""
        return {
            'companies_cached': len(self.companies),
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'update_interval_hours': self.update_interval.total_seconds() / 3600,
            'cache_valid': (
                self.last_updated is not None and 
                datetime.now() - self.last_updated < self.update_interval
            ) if self.last_updated else False
        }
