"""
Finance Assistant API Main Application
Clean, simple, and human-readable code structure
"""
from contextlib import asynccontextmanager
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    try:
        await cache_service.connect()
        logger.info("Services initialized successfully")
    except Exception as e:
        logger.warning(f"Some services failed to initialize: {e}")
    
    yield
    
    # Shutdown
    try:
        await cache_service.disconnect()
        logger.info("Services cleaned up successfully")
    except Exception as e:
        logger.warning(f"Error during cleanup: {e}")

# Create FastAPI app
app = FastAPI(
    title="Finance Assistant API",
    description="Clean and simple financial analysis platform",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan  # Use modern lifespan context manager
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(companies.router)
app.include_router(technical_analysis.router)
app.include_router(ai_queries.router)

@app.get("/", response_model=BaseResponse)
async def root():
    """Welcome message"""
    return BaseResponse(
        message="Welcome to Finance Assistant API",
        success=True  # This matches the model
        # timestamp is auto-generated
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
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
