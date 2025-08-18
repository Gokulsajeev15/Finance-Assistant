"""
Technical analysis API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from datetime import datetime

from ..dependencies import get_yahoo_service

router = APIRouter(prefix="/api/v1/technical-analysis", tags=["technical-analysis"])

@router.get("/{ticker}")
async def get_technical_analysis(ticker: str, yahoo_service=Depends(get_yahoo_service)):
    """Get comprehensive technical analysis for a stock"""
    try:
        # Get stock data and technical indicators
        stock_data = yahoo_service.get_stock_data(ticker)
        technical_data = yahoo_service.get_technical_indicators(ticker)
        
        if "error" in stock_data:
            raise HTTPException(status_code=400, detail=stock_data["error"])
        
        if "error" in technical_data:
            raise HTTPException(status_code=400, detail=technical_data["error"])
        
        # Combine the data
        result = {
            "ticker": ticker,
            "last_updated": datetime.now(),
            "stock_data": stock_data,
            "technical_data": technical_data
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting technical analysis: {str(e)}")

@router.get("/{ticker}/rsi")
async def get_rsi(ticker: str, yahoo_service=Depends(get_yahoo_service)):
    """Get RSI indicator for a stock"""
    try:
        technical_data = yahoo_service.get_technical_indicators(ticker)
        if "error" in technical_data:
            raise HTTPException(status_code=400, detail=technical_data["error"])
        
        rsi_data = technical_data.get("rsi", {})
        return {"ticker": ticker, "rsi": rsi_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting RSI: {str(e)}")

@router.get("/{ticker}/bollinger-bands")
async def get_bollinger_bands(ticker: str, yahoo_service=Depends(get_yahoo_service)):
    """Get Bollinger Bands for a stock"""
    try:
        technical_data = yahoo_service.get_technical_indicators(ticker)
        if "error" in technical_data:
            raise HTTPException(status_code=400, detail=technical_data["error"])
        
        # Since we don't have Bollinger Bands in the current service, return a placeholder
        return {"ticker": ticker, "bollinger_bands": {"message": "Bollinger Bands not yet implemented"}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting Bollinger Bands: {str(e)}")

@router.get("/{ticker}/moving-averages")
async def get_moving_averages(ticker: str, yahoo_service=Depends(get_yahoo_service)):
    """Get moving averages for a stock"""
    try:
        technical_data = yahoo_service.get_technical_indicators(ticker)
        if "error" in technical_data:
            raise HTTPException(status_code=400, detail=technical_data["error"])
        
        ma_data = {
            "sma_20": technical_data.get("sma_20"),
            "sma_50": technical_data.get("sma_50"),
            "trend": technical_data.get("trend")
        }
        return {"ticker": ticker, "moving_averages": ma_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting moving averages: {str(e)}")
