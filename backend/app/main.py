"""
Simple Finance Assistant API Main Application
Now powered by OpenAI GPT-4o mini with real-time financial data
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from .models.models import BaseResponse, HealthResponse
from .routers import companies, technical, ai

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Finance Assistant API",
    description="Simple AI-powered financial analysis with real-time data",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS to allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite dev server  
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
# Include routers
app.include_router(companies.router)
app.include_router(technical.router)
app.include_router(ai.router)

@app.get("/")
async def root():
    """Welcome message"""
    return {
        "message": "Welcome to Finance Assistant API",
        "status": "running",
        "version": "3.0.0"
    }

@app.get("/health")
async def health_check():
    """Check if everything is working"""
    ai_status = "ready" if os.getenv('OPENAI_API_KEY') else "needs_api_key"
    
    return {
        "status": "healthy",
        "version": "3.0.0",
        "services": {
            "yahoo_finance": "active",
            "companies": "active", 
            "openai_ai": ai_status
        }
    }

@app.exception_handler(Exception)
async def handle_errors(request, error):
    """Handle any unexpected errors"""
    logger.error(f"Unexpected error: {error}")
    return JSONResponse(
        status_code=500,
        content={"error": "Something went wrong", "detail": str(error)}
    )
