"""
Company-related API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ..models.models import CompanyInfo, RankingEntry, SectorSummary
from ..dependencies import get_fortune500_service

router = APIRouter(prefix="/api/v1/companies", tags=["companies"])

@router.get("/top", response_model=List[CompanyInfo])
async def get_top_companies(fortune500_service=Depends(get_fortune500_service)):
    """Get top Fortune 500 companies"""
    return fortune500_service.get_top_companies()

@router.get("/search", response_model=List[CompanyInfo])
async def search_companies(q: str, fortune500_service=Depends(get_fortune500_service)):
    """Search for companies by name"""
    return fortune500_service.search_companies(q)

@router.get("/{company_name}", response_model=CompanyInfo)
async def get_company_info(company_name: str, fortune500_service=Depends(get_fortune500_service)):
    """Get detailed information about a specific company"""
    try:
        return fortune500_service.get_company_info(company_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Company not found: {str(e)}")

@router.get("/sector/{sector}", response_model=List[CompanyInfo])
async def get_companies_by_sector(sector: str, fortune500_service=Depends(get_fortune500_service)):
    """Get companies in a specific sector"""
    return fortune500_service.get_companies_by_sector(sector)

@router.get("/industry/{industry}", response_model=List[CompanyInfo])
async def get_companies_by_industry(industry: str, fortune500_service=Depends(get_fortune500_service)):
    """Get companies in a specific industry"""
    return fortune500_service.get_companies_by_industry(industry)
