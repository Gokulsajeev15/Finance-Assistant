"""
Simple company API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends

from ..models.models import CompanyInfo
from ..dependencies import get_company_service

router = APIRouter(prefix="/api/v1/companies", tags=["companies"])

@router.get("/top")
async def get_top_companies(limit: int = 20, company_service=Depends(get_company_service)):
    """Get top companies by market cap (updated every 6 hours)"""
    try:
        companies = await company_service.get_top_companies(limit)
        return companies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting companies: {str(e)}")

@router.get("/search")
async def search_companies(q: str, company_service=Depends(get_company_service)):
    """Search for companies by name"""
    try:
        companies = await company_service.search_companies(q)
        return companies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching companies: {str(e)}")

@router.get("/{company_name}")
async def get_company_info(company_name: str, company_service=Depends(get_company_service)):
    """Get detailed information about a specific company"""
    try:
        # First try to get by ticker
        company = await company_service.get_company_by_ticker(company_name)
        
        if not company:
            # Try searching by name if ticker didn't work
            search_results = await company_service.search_companies(company_name)
            if search_results:
                company = search_results[0]
        
        if not company:
            raise HTTPException(status_code=404, detail=f"Company not found: {company_name}")
        
        return company
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting company info: {str(e)}")

@router.get("/cache/info")
async def get_cache_info(company_service=Depends(get_company_service)):
    """Get information about the company data cache"""
    try:
        cache_info = company_service.get_cache_info()
        return cache_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting cache info: {str(e)}")
