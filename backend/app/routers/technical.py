from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from ..dependencies import get_stock_service, get_company_service

router = APIRouter(prefix="/api/v1/technical-analysis", tags=["technical-analysis"])


@router.get("/{ticker}")
async def get_technical_analysis(ticker: str,
                                  stock_service=Depends(get_stock_service),
                                  companies_service=Depends(get_company_service)):
    """Full technical analysis for a ticker or company name."""
    try:
        stock_data = stock_service.get_stock_data(ticker)
        actual_ticker = ticker

        if "error" in stock_data:
            # Input might be a company name — resolve it to a ticker
            try:
                results = await companies_service.search_companies(ticker)
                if not results:
                    raise HTTPException(status_code=400, detail=f"Company not found: {ticker}")
                actual_ticker = results[0]["ticker"]
                stock_data = stock_service.get_stock_data(actual_ticker)
                if "error" in stock_data:
                    raise HTTPException(
                        status_code=400,
                        detail=f"No stock data for {actual_ticker} (resolved from '{ticker}')"
                    )
            except HTTPException:
                raise
            except Exception:
                raise HTTPException(status_code=400, detail=f"Unable to resolve ticker for: {ticker}")

        try:
            technical_data = stock_service.get_technical_indicators(actual_ticker)
        except Exception:
            technical_data = {"note": "Technical indicators unavailable"}

        return {
            "ticker": actual_ticker.upper(),
            "original_query": ticker,
            "last_updated": datetime.now().isoformat(),
            "stock_data": stock_data,
            "technical_data": technical_data
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting technical analysis: {str(e)}")


@router.get("/{ticker}/rsi")
async def get_rsi(ticker: str, stock_service=Depends(get_stock_service)):
    """RSI indicator for a given ticker."""
    try:
        technical_data = stock_service.get_technical_indicators(ticker)
        if "error" in technical_data:
            raise HTTPException(status_code=400, detail=technical_data["error"])
        return {
            "ticker": ticker.upper(),
            "rsi": technical_data.get("rsi", {}),
            "last_updated": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting RSI: {str(e)}")


@router.get("/{ticker}/basic")
async def get_basic_analysis(ticker: str, stock_service=Depends(get_stock_service)):
    """Basic stock price info without indicators."""
    try:
        stock_data = stock_service.get_stock_data(ticker)
        if "error" in stock_data:
            raise HTTPException(status_code=400, detail=stock_data["error"])
        return {
            "ticker": ticker.upper(),
            "data": stock_data,
            "last_updated": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting basic analysis: {str(e)}")
