"""
Technical analysis API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from ..models.models import TechnicalAnalysisResponse
from ..dependencies import get_yahoo_service

router = APIRouter(prefix="/api/v1/technical-analysis", tags=["technical-analysis"])

@router.get("/{ticker}", response_model=TechnicalAnalysisResponse)
async def get_technical_analysis(ticker: str, yahoo_service=Depends(get_yahoo_service)):
    """Get comprehensive technical analysis for a stock"""
    try:
        indicators = yahoo_service.get_technical_indicators(ticker)
        if "error" in indicators:
            raise HTTPException(status_code=400, detail=indicators["error"])
        
        return TechnicalAnalysisResponse(
            ticker=ticker,
            indicators=indicators.get("indicators", {}),
            price_data=indicators.get("price_data", {}),
            last_updated=indicators.get("last_updated")
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting technical analysis: {str(e)}")

@router.get("/{ticker}/rsi")
async def get_rsi(ticker: str, yahoo_service=Depends(get_yahoo_service)):
    """Get RSI indicator for a stock"""
    try:
        indicators = yahoo_service.get_technical_indicators(ticker)
        if "error" in indicators:
            raise HTTPException(status_code=400, detail=indicators["error"])
        
        rsi_data = indicators.get("indicators", {}).get("rsi", {})
        return {"ticker": ticker, "rsi": rsi_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting RSI: {str(e)}")

@router.get("/{ticker}/bollinger-bands")
async def get_bollinger_bands(ticker: str, yahoo_service=Depends(get_yahoo_service)):
    """Get Bollinger Bands for a stock"""
    try:
        indicators = yahoo_service.get_technical_indicators(ticker)
        if "error" in indicators:
            raise HTTPException(status_code=400, detail=indicators["error"])
        
        bb_data = indicators.get("indicators", {}).get("bollinger_bands", {})
        return {"ticker": ticker, "bollinger_bands": bb_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting Bollinger Bands: {str(e)}")

@router.get("/{ticker}/moving-averages")
async def get_moving_averages(ticker: str, yahoo_service=Depends(get_yahoo_service)):
    """Get moving averages for a stock"""
    try:
        indicators = yahoo_service.get_technical_indicators(ticker)
        if "error" in indicators:
            raise HTTPException(status_code=400, detail=indicators["error"])
        
        ma_data = indicators.get("indicators", {}).get("moving_averages", {})
        return {"ticker": ticker, "moving_averages": ma_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting moving averages: {str(e)}")
