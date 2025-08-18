"""
Company Database Service - Stores information about big companies

This file contains a list of famous companies that people often ask about.
For each company we store:
- Company name (like "Apple")
- Stock ticker symbol (like "AAPL") 
- What sector they're in (like "Technology")
- How big they are (Fortune 500 ranking)
- How much money they make (revenue and profit)

Think of this as our company phonebook!
"""
import logging

logger = logging.getLogger(__name__)

class SimpleCompanyService:
    """A database of big companies that people want to know about"""
    
    def __init__(self):
        # List of popular companies that people ask about
        # Each company has: name, stock symbol, sector, rank, and revenue
        self.companies = [
            {"rank": 1, "company": "Walmart", "ticker": "WMT", "sector": "Retail", "revenue": 611289, "profit": 11680},
            {"rank": 2, "company": "Amazon", "ticker": "AMZN", "sector": "Technology", "revenue": 514000, "profit": 3042},
            {"rank": 3, "company": "Apple", "ticker": "AAPL", "sector": "Technology", "revenue": 394328, "profit": 96995},
            {"rank": 4, "company": "UnitedHealth Group", "ticker": "UNH", "sector": "Healthcare", "revenue": 324162, "profit": 22081},
            {"rank": 5, "company": "CVS Health", "ticker": "CVS", "sector": "Healthcare", "revenue": 322467, "profit": 8344},
            {"rank": 6, "company": "Berkshire Hathaway", "ticker": "BRK.A", "sector": "Financial", "revenue": 302089, "profit": 96223},
            {"rank": 7, "company": "Alphabet", "ticker": "GOOGL", "sector": "Technology", "revenue": 307394, "profit": 76033},
            {"rank": 10, "company": "Microsoft", "ticker": "MSFT", "sector": "Technology", "revenue": 198270, "profit": 72474},
            {"rank": 12, "company": "Costco Wholesale", "ticker": "COST", "sector": "Retail", "revenue": 226954, "profit": 6292},
            {"rank": 18, "company": "PepsiCo", "ticker": "PEP", "sector": "Food & Drinks", "revenue": 79474, "profit": 7612},
            {"rank": 19, "company": "Home Depot", "ticker": "HD", "sector": "Retail", "revenue": 151157, "profit": 16433},
            {"rank": 20, "company": "General Motors", "ticker": "GM", "sector": "Cars", "revenue": 122485, "profit": 10019},
            {"rank": 21, "company": "Ford Motor", "ticker": "F", "sector": "Cars", "revenue": 127144, "profit": 17937},
            {"rank": 22, "company": "AT&T", "ticker": "T", "sector": "Telecom", "revenue": 168864, "profit": 20042},
            {"rank": 27, "company": "JPMorgan Chase", "ticker": "JPM", "sector": "Banking", "revenue": 119543, "profit": 37945},
            {"rank": 28, "company": "Bank of America", "ticker": "BAC", "sector": "Banking", "revenue": 89450, "profit": 27528},
            {"rank": 43, "company": "Intel", "ticker": "INTC", "sector": "Technology", "revenue": 79024, "profit": 8014},
            {"rank": 44, "company": "Netflix", "ticker": "NFLX", "sector": "Entertainment", "revenue": 31616, "profit": 5424},
            {"rank": 47, "company": "Disney", "ticker": "DIS", "sector": "Entertainment", "revenue": 82722, "profit": 3004},
            {"rank": 55, "company": "Nike", "ticker": "NKE", "sector": "Retail", "revenue": 51217, "profit": 6046},
            {"rank": 61, "company": "Coca-Cola", "ticker": "KO", "sector": "Food & Drinks", "revenue": 43004, "profit": 10042},
            {"rank": 78, "company": "McDonald's", "ticker": "MCD", "sector": "Food & Drinks", "revenue": 23223, "profit": 7545},
            {"rank": 85, "company": "Starbucks", "ticker": "SBUX", "sector": "Food & Drinks", "revenue": 32250, "profit": 4199},
            
            # Popular tech companies (not in Fortune 500 but frequently asked about)
            {"rank": 250, "company": "Tesla", "ticker": "TSLA", "sector": "Electric Vehicles", "revenue": 96773, "profit": 15000},
            {"rank": 260, "company": "Meta Platforms", "ticker": "META", "sector": "Technology", "revenue": 134902, "profit": 39098},
            {"rank": 270, "company": "NVIDIA", "ticker": "NVDA", "sector": "Technology", "revenue": 126510, "profit": 60920}
        ]
    
    def get_top_companies(self, limit=20):
        """Get the top companies (biggest ones first)"""
        try:
            # Sort by rank (lowest rank number = biggest company)
            sorted_companies = sorted(self.companies, key=lambda x: x['rank'])
            
            # Return only the number requested
            return sorted_companies[:limit]
            
        except Exception as e:
            logger.error(f"Error getting top companies: {e}")
            return []
    
    def get_company_by_ticker(self, ticker):
        """Find a company by its stock ticker (like AAPL for Apple)"""
        try:
            # Make sure ticker is uppercase
            ticker = ticker.upper()
            
            # Look through all companies
            for company in self.companies:
                if company['ticker'] == ticker:
                    return company
            
            # If we didn't find it, return None
            return None
            
        except Exception as e:
            logger.error(f"Error finding company {ticker}: {e}")
            return None
    
    def get_company_by_name(self, name):
        """Find a company by its name"""
        try:
            # Make the name lowercase for easier searching
            name = name.lower()
            
            # Look through all companies
            for company in self.companies:
                if name in company['company'].lower():
                    return company
            
            # If we didn't find it, return None
            return None
            
        except Exception as e:
            logger.error(f"Error finding company {name}: {e}")
            return None
    
    def search_companies(self, search_term):
        """Search for companies by name or ticker"""
        try:
            search_term = search_term.lower()
            results = []
            
            # Look through all companies
            for company in self.companies:
                # Check if search term is in company name or ticker
                if (search_term in company['company'].lower() or 
                    search_term in company['ticker'].lower()):
                    results.append(company)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching companies: {e}")
            return []
    
    def get_companies_by_sector(self, sector):
        """Get all companies in a specific sector (like Technology)"""
        try:
            sector = sector.lower()
            results = []
            
            for company in self.companies:
                if sector in company['sector'].lower():
                    results.append(company)
            
            # Sort by rank (biggest companies first)
            return sorted(results, key=lambda x: x['rank'])
            
        except Exception as e:
            logger.error(f"Error getting sector {sector}: {e}")
            return []
    
    def get_all_sectors(self):
        """Get list of all sectors we have companies for"""
        try:
            sectors = set()  # Use set to avoid duplicates
            
            for company in self.companies:
                sectors.add(company['sector'])
            
            return sorted(list(sectors))  # Convert back to list and sort
            
        except Exception as e:
            logger.error(f"Error getting sectors: {e}")
            return []
