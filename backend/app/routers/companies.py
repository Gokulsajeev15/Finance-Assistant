"""
Company-related API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ..models.models import CompanyInfo, RankingEntry, SectorSummary
from ..dependencies import get_fortune500_service

router = APIRouter(prefix="/api/v1/companies", tags=["companies"])

@router.get("/top", response_model=List[CompanyInfo])
async def get_top_companies(limit: int = 20, fortune500_service=Depends(get_fortune500_service)):
    """Get top companies by market cap (dynamically updated)"""
    companies = await fortune500_service.get_top_companies(limit)
    return companies

@router.get("/search", response_model=List[CompanyInfo])
async def search_companies(q: str, fortune500_service=Depends(get_fortune500_service)):
    """Search for companies by name"""
    companies = await fortune500_service.search_companies(q)
    return companies

@router.get("/{company_name}", response_model=CompanyInfo)
async def get_company_info(company_name: str, fortune500_service=Depends(get_fortune500_service)):
    """Get detailed information about a specific company"""
    try:
        company = await fortune500_service.get_company_info(company_name)
        if not company:
            raise HTTPException(status_code=404, detail=f"Company not found: {company_name}")
        return company
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Company not found: {str(e)}")

@router.get("/sector/{sector}", response_model=List[CompanyInfo])
async def get_companies_by_sector(sector: str, fortune500_service=Depends(get_fortune500_service)):
    """Get companies in a specific sector"""
    companies = await fortune500_service.get_companies_by_sector(sector)
    return companies

@router.get("/industry/{industry}", response_model=List[CompanyInfo])
async def get_companies_by_industry(industry: str, fortune500_service=Depends(get_fortune500_service)):
    """Get companies in a specific industry"""
    companies = await fortune500_service.get_companies_by_industry(industry)
    return companies

@router.get("/cache/info")
async def get_cache_info(fortune500_service=Depends(get_fortune500_service)):
    """Get information about the company data cache"""
    return fortune500_service.get_cache_info()

@router.post("/cache/refresh")
async def refresh_companies(fortune500_service=Depends(get_fortune500_service)):
    """Force refresh the company database"""
    success = await fortune500_service.update_companies()
    return {
        "success": success,
        "message": "Company database refreshed successfully" if success else "Failed to refresh database",
        "companies_loaded": len(fortune500_service.companies) if success else 0
    }
