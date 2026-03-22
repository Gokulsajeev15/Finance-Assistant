import yfinance as yf
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SimpleCompanyService:

    def __init__(self):
        self.companies = []
        self.last_updated = None
        self.update_interval = timedelta(hours=6)
        self.executor = ThreadPoolExecutor(max_workers=10)
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
        try:
            logger.info("Refreshing company database...")
            company_data = await self._fetch_all()
            if company_data:
                company_data.sort(key=lambda x: x.get('market_cap', 0), reverse=True)
                self.companies = company_data[:100]
                self.last_updated = datetime.now()
                logger.info(f"Updated {len(self.companies)} companies")
                return True
            logger.warning("No company data received")
            return False
        except Exception as e:
            logger.error(f"Error updating companies: {e}")
            return False

    async def _fetch_all(self):
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(self.executor, self._fetch_one, symbol)
            for symbol in self.major_symbols
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        valid = [r for r in results if r is not None and not isinstance(r, Exception)]
        logger.info(f"Fetched data for {len(valid)} companies")
        return valid

    def _fetch_one(self, symbol):
        try:
            info = yf.Ticker(symbol).info
            market_cap = info.get('marketCap', 0)
            if not market_cap:
                return None

            revenue = (info.get('totalRevenue') or info.get('revenue') or
                       info.get('totalRevenueTTM') or info.get('revenueQuarterlyGrowth'))

            profit = (info.get('netIncomeToCommon') or info.get('netIncome') or
                      (info.get('trailingEps', 0) * info.get('sharesOutstanding', 0)
                       if info.get('trailingEps') and info.get('sharesOutstanding') else None))

            def fmt(val):
                if not val or not isinstance(val, (int, float)) or val <= 0:
                    return None
                if val >= 1e9:
                    return f"${val / 1e9:.1f}B"
                if val >= 1e6:
                    return f"${val / 1e6:.1f}M"
                return f"${val / 1e3:.1f}K"

            name = info.get('longName', symbol)
            return {
                'rank': 0,
                'company': name,
                'name': name,
                'ticker': symbol,
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'market_cap': market_cap,
                'employees': info.get('fullTimeEmployees', 'N/A'),
                'revenue': fmt(revenue),
                'profit': fmt(profit),
            }
        except Exception as e:
            logger.error(f"Error fetching {symbol}: {e}")
            return None

    async def get_top_companies(self, limit=20):
        await self._ensure_fresh()
        companies = self.companies[:limit]
        for i, c in enumerate(companies):
            c['rank'] = i + 1
        return companies

    async def get_company_by_ticker(self, ticker):
        await self._ensure_fresh()
        for c in self.companies:
            if c['ticker'].upper() == ticker.upper():
                return c
        # Not in cache — try fetching directly
        return self._fetch_one(ticker.upper())

    async def search_companies(self, search_term):
        await self._ensure_fresh()

        term = search_term.lower().strip()

        # Map common aliases to actual company names for better matching
        aliases = {
            "google": "alphabet", "facebook": "meta", "fb": "meta",
            "tesla motors": "tesla", "gm": "general motors",
            "ge": "general electric", "jpmorgan": "jpmorgan chase",
            "jp morgan": "jpmorgan chase", "jpm": "jpmorgan chase",
            "coca cola": "coca-cola", "coke": "coca-cola", "pepsi": "pepsico",
            "mcdonalds": "mcdonald", "mc donald": "mcdonald",
            "walmart": "wal-mart", "berkshire": "berkshire hathaway",
            "visa inc": "visa", "mastercard inc": "mastercard"
        }
        resolved = aliases.get(term, term)

        matches = []
        seen = set()

        for c in self.companies:
            name = c['company'].lower()
            ticker = c['ticker'].lower()

            if term == ticker or resolved == ticker:
                matches.insert(0, c)
            elif term == name or resolved == name:
                matches.insert(0, c)
            elif term in name or resolved in name:
                matches.append(c)
            else:
                for word in name.split():
                    if word.startswith(term) or word.startswith(resolved):
                        matches.append(c)
                        break

        unique = []
        for c in matches:
            if c['ticker'] not in seen:
                seen.add(c['ticker'])
                unique.append(c)

        return unique[:10]

    async def _ensure_fresh(self):
        if (not self.companies or not self.last_updated or
                datetime.now() - self.last_updated > self.update_interval):
            await self.update_companies()

    def get_cache_info(self):
        return {
            'total_companies': len(self.companies),
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'update_interval_hours': self.update_interval.total_seconds() / 3600
        }
