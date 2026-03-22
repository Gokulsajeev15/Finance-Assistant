from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os
from dotenv import load_dotenv

load_dotenv()

from .models.models import BaseResponse
from .routers import companies, technical, ai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Finance Assistant API",
    description="AI-powered financial analysis with real-time stock data",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(companies.router)
app.include_router(technical.router)
app.include_router(ai.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Finance Assistant API",
        "status": "running",
        "version": "3.0.0"
    }


@app.get("/health")
async def health_check():
    ai_status = "ready" if (os.getenv('HF_TOKEN') or os.getenv('OPENAI_API_KEY')) else "needs_api_key"
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
    logger.error(f"Unexpected error: {error}")
    return JSONResponse(
        status_code=500,
        content={"error": "Something went wrong", "detail": str(error)}
    )
