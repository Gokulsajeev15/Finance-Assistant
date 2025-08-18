"""
Finance Assistant Services - Clean and Simple Architecture

This file imports all our main services:
1. 🏢 SimpleCompanyService - Database of Fortune 500 companies
2. 📈 SimpleStockService - Live stock data from Yahoo Finance  
3. 🤖 HuggingFaceFinancialAI - Real AI using machine learning models
4. 🗄️ CacheService - Fast data caching for better performance

All services are designed to be simple, readable, and scalable!
"""
from .company_database import SimpleCompanyService
from .stock_data_service import SimpleStockService
from .huggingface_ai import HuggingFaceFinancialAI
from .data_cache import CacheService

