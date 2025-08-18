"""
AI Query API endpoints
Simple and easy to understand!
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from ..dependencies import get_ai_processor

router = APIRouter(prefix="/api/v1/ai", tags=["ai-queries"])

@router.post("/query")
async def ask_ai_question(
    query: str, 
    ai_processor=Depends(get_ai_processor)
) -> Dict[str, Any]:
    """Ask the AI any question about money or stocks"""
    try:
        # Make sure the question isn't too short
        if not query or len(query.strip()) < 3:
            raise HTTPException(status_code=400, detail="Please ask a longer question!")
        
        # Ask our simple AI to answer the question
        answer = await ai_processor.answer_question(query)
        return answer
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Sorry, I had trouble with your question: {str(e)}")

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
