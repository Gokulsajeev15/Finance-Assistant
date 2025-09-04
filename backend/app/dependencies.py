"""
Simple dependencies for the Finance Assistant API
Now with OpenAI and real-time Yahoo Finance data!
"""
from .services.companies import SimpleCompanyService
from .services.stock_data import SimpleStockService
from .services.ai import OpenAIFinancialAI

# Create all our services
company_service = SimpleCompanyService()
stock_service = SimpleStockService()
openai_ai_service = OpenAIFinancialAI(stock_service, company_service)

def get_company_service():
    """Get company service instance (top 100 by market cap)"""
    return company_service

def get_stock_service():
    """Get Yahoo Finance service instance"""
    return stock_service

def get_openai_service():
    """Get OpenAI AI service instance"""
    return openai_ai_service
