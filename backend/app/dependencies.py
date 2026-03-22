from .services.companies import SimpleCompanyService
from .services.stock_data import SimpleStockService
from .services.ai import OpenAIFinancialAI

# Singleton instances — shared across all requests
company_service = SimpleCompanyService()
stock_service = SimpleStockService()
openai_ai_service = OpenAIFinancialAI(stock_service, company_service)


def get_company_service():
    return company_service


def get_stock_service():
    return stock_service


def get_openai_service():
    return openai_ai_service
