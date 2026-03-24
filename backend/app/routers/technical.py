from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from ..dependencies import get_stock_service, get_company_service

router = APIRouter(prefix="/api/v1/technical-analysis", tags=["technical-analysis"])

_STOCK_DATA_KEYS = ["current_price", "change", "change_percent", "volume",
                    "day_high", "day_low", "52_week_high", "52_week_low"]
_TECHNICAL_KEYS = ["rsi", "sma_20", "sma_50", "ema_12", "ema_26", "bollinger_bands", "trend"]


@router.get("/{ticker}")
async def get_technical_analysis(ticker: str,
                                  stock_service=Depends(get_stock_service),
                                  companies_service=Depends(get_company_service)):
    """
    Full technical analysis for a ticker or company name.
    Makes a single API call to get both price data and indicators,
    avoiding back-to-back calls that would hit the rate limit.
    """
    try:
        actual_ticker = ticker.upper()
        full_data = stock_service.get_technical_indicators(actual_ticker)

        if "error" in full_data:
            # Input might be a company name — resolve it to a ticker first
            try:
                results = await companies_service.search_companies(ticker)
                if not results:
                    raise HTTPException(status_code=400, detail=f"Company not found: {ticker}")
                actual_ticker = results[0]["ticker"]
                full_data = stock_service.get_technical_indicators(actual_ticker)
                if "error" in full_data:
                    raise HTTPException(status_code=400, detail=full_data["error"])
            except HTTPException:
                raise
            except Exception:
                raise HTTPException(status_code=400, detail=f"Unable to resolve ticker for: {ticker}")

        return {
            "ticker": actual_ticker,
            "original_query": ticker,
            "last_updated": datetime.now().isoformat(),
            "stock_data": {k: full_data[k] for k in _STOCK_DATA_KEYS if k in full_data},
            "technical_data": {k: full_data[k] for k in _TECHNICAL_KEYS if k in full_data}
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting technical analysis: {str(e)}")


@router.get("/{ticker}/rsi")
async def get_rsi(ticker: str, stock_service=Depends(get_stock_service)):
    """RSI indicator for a given ticker."""
    try:
        data = stock_service.get_technical_indicators(ticker)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        return {
            "ticker": ticker.upper(),
            "rsi": data.get("rsi", {}),
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
