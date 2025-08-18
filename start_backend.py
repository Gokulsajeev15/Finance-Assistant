#!/usr/bin/env python3
"""
Backend Startup Script - Easy way to start the Finance Assistant API

This script starts our Python backend server that provides:
- Stock data and company information
- AI-powered financial assistant
- Technical analysis and market insights

Just run: python start_backend.py
"""

import uvicorn
import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Starting Finance Assistant Backend API...")
    print("API will be available at: http://localhost:8000")
    print("Documentation at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
