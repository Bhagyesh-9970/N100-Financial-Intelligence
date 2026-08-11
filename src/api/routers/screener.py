import pandas as pd
from fastapi import APIRouter, HTTPException, Query

from src.api.data_access import get_screener_dataframe

router = APIRouter(tags=["screener"])


@router.get("/screener")
@router.get("/api/v1/screener")
def screener(limit: int = Query(50, ge=1, le=200), min_roe: float | None = None, max_debt: float | None = None, sector: str | None = None) -> list[dict]:
    if min_roe is not None and min_roe < 0:
        raise HTTPException(status_code=400, detail="min_roe must be non-negative")
    if max_debt is not None and max_debt < 0:
        raise HTTPException(status_code=400, detail="max_debt must be non-negative")
    df = get_screener_dataframe(min_roe=min_roe, max_debt=max_debt, sector=sector)
    return df.head(limit).where(df.notna(), None).to_dict(orient="records")
