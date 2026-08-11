from fastapi import APIRouter, HTTPException

from src.api.data_access import get_company_by_ticker, get_documents

router = APIRouter(tags=["documents"])


@router.get("/api/v1/companies/{ticker}/documents")
def documents(ticker: str) -> list[dict]:
    if get_company_by_ticker(ticker).empty:
        raise HTTPException(status_code=404, detail="company not found")
    df = get_documents(ticker)
    return df.where(df.notna(), None).to_dict(orient="records")
