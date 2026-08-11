from fastapi import APIRouter, HTTPException

from src.api.data_access import get_sector_companies, get_sectors_dataframe

router = APIRouter(tags=["sectors"])


@router.get("/sectors")
@router.get("/api/v1/sectors")
def list_sectors() -> list[dict]:
    return get_sectors_dataframe().to_dict(orient="records")


@router.get("/sectors/{sector}/companies")
@router.get("/api/v1/sectors/{sector}/companies")
def sector_companies(sector: str) -> list[dict]:
    df = get_sector_companies(sector)
    if df.empty:
        raise HTTPException(status_code=404, detail="sector not found")
    return df.where(df.notna(), None).to_dict(orient="records")
