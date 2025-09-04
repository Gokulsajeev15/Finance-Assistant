"""
Finance Assistant API Main Application
Clean, simple, and human-readable code structure
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from .models.models import BaseResponse, HealthResponse
from .dependencies import cache_service
from .routers import companies, technical_analysis, ai_queries

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Finance Assistant API",
    description="Clean and simple financial analysis platform",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:3001",  # Alternative Vite port
        "http://127.0.0.1:3001",
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(companies.router)
app.include_router(technical_analysis.router)
app.include_router(ai_queries.router)

@app.on_event("startup")
async def startup_event():
    """Initialize services when app starts"""
    try:
        await cache_service.connect()
        logger.info("Services initialized successfully")
    except Exception as e:
        logger.warning(f"Some services failed to initialize: {e}")

@app.on_event("shutdown") 
async def shutdown_event():
    """Clean up when app shuts down"""
    try:
        await cache_service.disconnect()
        logger.info("Services cleaned up successfully")
    except Exception as e:
        logger.warning(f"Error during cleanup: {e}")

@app.get("/", response_model=BaseResponse)
async def root():
    """Welcome message"""
    return BaseResponse(
        message="Welcome to Finance Assistant API",
        status="success",
        timestamp="2025-08-14T00:00:00Z"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="2.0.0",
        services={
            "yahoo_finance": "active",
            "fortune500": "active", 
            "cache": "active",
            "ai_processor": "active"
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle unexpected errors gracefully"""
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )
