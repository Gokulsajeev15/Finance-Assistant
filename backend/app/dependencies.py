"""
Dependencies for the Finance Assistant API
"""
from .services.fortune500_service import Fortune500Service
from .services.yahoo_finance_clean import EnhancedYahooFinanceService
from .services.ai_query_processor import AIQueryProcessor
from .services.cache_service import CacheService

# Initialize services
fortune500_service = Fortune500Service()
yahoo_service = EnhancedYahooFinanceService()
ai_processor = AIQueryProcessor(yahoo_service, fortune500_service)
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
