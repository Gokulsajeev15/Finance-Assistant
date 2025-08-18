"""
Dependencies for the Finance Assistant API
Clean, descriptive file names that make sense!
"""
from .services.company_database import SimpleCompanyService
from .services.stock_data_service import SimpleStockService
from .services.ai_financial_assistant import SimpleFinancialAI
from .services.data_cache import CacheService

# Create all our services
fortune500_service = SimpleCompanyService()
yahoo_service = SimpleStockService()
ai_processor = SimpleFinancialAI(yahoo_service, fortune500_service)
cache_service = CacheService()

def get_fortune500_service():
    """Get Fortune 500 service instance"""
    return fortune500_service

def get_yahoo_service():
    """Get Yahoo Finance service instance"""
    return yahoo_service

def get_ai_processor():
    """Get AI query processor instance"""
    return ai_processor

def get_cache_service():
    """Get cache service instance"""
    return cache_service
