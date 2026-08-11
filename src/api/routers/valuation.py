from fastapi import APIRouter, Query

from src.api.data_access import get_companies_dataframe

router = APIRouter(tags=["valuation"])


@router.get("/api/v1/market-cap/{ticker}")
def market_cap(ticker: str) -> list[dict]:
    from src.api.data_access import get_market_cap

    df = get_market_cap(ticker)
    return df.where(df.notna(), None).to_dict(orient="records")


@router.get("/api/v1/valuation")
def valuation(limit: int = Query(50, ge=1, le=200)) -> list[dict]:
    df = get_companies_dataframe().head(limit)
    return df.where(df.notna(), None).to_dict(orient="records")
