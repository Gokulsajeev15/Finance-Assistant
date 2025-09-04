"""
Simple technical analysis API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime

from ..dependencies import get_stock_service, get_company_service

router = APIRouter(prefix="/api/v1/technical-analysis", tags=["technical-analysis"])

@router.get("/{ticker}")
async def get_technical_analysis(ticker: str, 
                                stock_service=Depends(get_stock_service),
                                companies_service=Depends(get_company_service)):
    """Get technical analysis for a stock - supports both tickers and company names"""
    try:
        # First try with the original ticker
        stock_data = stock_service.get_stock_data(ticker)
        actual_ticker = ticker
        
        # If it fails, try to find the ticker by searching our company database
        if "error" in stock_data:
            try:
                search_results = await companies_service.search_companies(ticker)
                
                if search_results and len(search_results) > 0:
                    # Use the best match (first result)
                    best_match = search_results[0]
                    actual_ticker = best_match["ticker"]
                    stock_data = stock_service.get_stock_data(actual_ticker)
                    
                    # If this works, continue with the data
                    if "error" not in stock_data:
                        pass  # Continue with successful data
                    else:
                        # Even the found ticker doesn't work
                        raise HTTPException(
                            status_code=400, 
                            detail=f"No data available for {ticker}. Found company '{best_match['company']}' with ticker {actual_ticker}, but no stock data available."
                        )
                else:
                    # No company found in our database
                    raise HTTPException(
                        status_code=400, 
                        detail=f"No data available for {ticker}. Company not found in our database of top 100 companies."
                    )
            except HTTPException:
                raise
            except Exception as e:
                # Search failed, provide generic error
                raise HTTPException(
                    status_code=400, 
                    detail=f"No data available for {ticker}. Unable to find matching company."
                )
        
        # Get technical indicators if available
        try:
            technical_data = stock_service.get_technical_indicators(actual_ticker)
        except:
            technical_data = {"note": "Technical indicators not available for this stock"}
        
        # Combine the data
        result = {
            "ticker": actual_ticker.upper(),
            "original_query": ticker,
            "last_updated": datetime.now().isoformat(),
            "stock_data": stock_data,
            "technical_data": technical_data
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting technical analysis: {str(e)}")

@router.get("/{ticker}/rsi")
async def get_rsi(ticker: str, stock_service=Depends(get_stock_service)):
    """Get RSI (Relative Strength Index) for a stock"""
    try:
        technical_data = stock_service.get_technical_indicators(ticker)
        
        if "error" in technical_data:
            raise HTTPException(status_code=400, detail=technical_data["error"])
        
        rsi_data = technical_data.get("rsi", {})
        
        result = {
            "ticker": ticker.upper(),
            "rsi": rsi_data,
            "last_updated": datetime.now().isoformat()
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting RSI: {str(e)}")

@router.get("/{ticker}/basic")
async def get_basic_analysis(ticker: str, stock_service=Depends(get_stock_service)):
    """Get basic stock information"""
    try:
        stock_data = stock_service.get_stock_data(ticker)
        
        if "error" in stock_data:
            raise HTTPException(status_code=400, detail=stock_data["error"])
        
        # Return just the basic info
        result = {
            "ticker": ticker.upper(),
            "data": stock_data,
            "last_updated": datetime.now().isoformat()
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting basic analysis: {str(e)}")
