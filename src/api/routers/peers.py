from fastapi import APIRouter, HTTPException

from src.api.data_access import get_company_by_ticker, get_peer_groups

router = APIRouter(tags=["peers"])


@router.get("/api/v1/peers/{group_name}")
def peer_group(group_name: str) -> list[dict]:
    df = get_peer_groups(group_name)
    if df.empty:
        raise HTTPException(status_code=404, detail="peer group not found")
    return df.where(df.notna(), None).to_dict(orient="records")


@router.get("/api/v1/companies/{ticker}/peers/compare")
def compare_peers(ticker: str) -> dict:
    df = get_company_by_ticker(ticker)
    if df.empty:
        raise HTTPException(status_code=404, detail="company not found")
    return {"ticker": ticker.upper(), "company": df.iloc[0].to_dict()}
