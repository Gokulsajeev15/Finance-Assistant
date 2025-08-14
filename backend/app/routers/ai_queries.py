"""
AI Query API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from ..dependencies import get_ai_processor

router = APIRouter(prefix="/api/v1/ai", tags=["ai-queries"])

@router.post("/query")
async def process_ai_query(
    query: str, 
    ai_processor=Depends(get_ai_processor)
) -> Dict[str, Any]:
    """Process a natural language query about stocks and companies"""
    try:
        if not query or len(query.strip()) < 3:
            raise HTTPException(status_code=400, detail="Query too short")
        
        result = ai_processor.process_query(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing query: {str(e)}")

@router.get("/examples")
async def get_query_examples():
    """Get example queries that the AI can handle"""
    return {
        "examples": [
            "What is the price of AAPL?",
            "Tell me about Tesla",
            "Show RSI for Microsoft",
            "What is Amazon worth?",
            "Give me info about GOOGL"
        ],
        "supported_queries": [
            "Stock prices",
            "Company information", 
            "Technical analysis",
            "RSI indicators",
            "Basic stock data"
        ]
    }
