from fastapi import APIRouter, HTTPException, Query

from src.api.data_access import get_company_by_ticker, get_company_table, get_companies_dataframe

router = APIRouter(tags=["companies"])


@router.get("/companies")
@router.get("/api/v1/companies")
def list_companies(limit: int = Query(25, ge=1, le=200)) -> list[dict]:
    df = get_companies_dataframe().head(limit)
    return df.where(df.notna(), None).to_dict(orient="records")


@router.get("/companies/{ticker}")
@router.get("/api/v1/companies/{ticker}")
def get_company(ticker: str) -> dict:
    df = get_company_by_ticker(ticker)
    if df.empty:
        raise HTTPException(status_code=404, detail="company not found")
    row = df.iloc[0].to_dict()
    return {"ticker": ticker.upper(), "company": row}


@router.get("/companies/{ticker}/pl")
@router.get("/api/v1/companies/{ticker}/pl")
def get_company_pl(ticker: str, year: int | None = None, from_year: int | None = None, to_year: int | None = None) -> list[dict]:
    df = get_company_table("profitandloss", ticker, year=year, from_year=from_year, to_year=to_year)
    return df.where(df.notna(), None).to_dict(orient="records")


@router.get("/companies/{ticker}/bs")
@router.get("/api/v1/companies/{ticker}/bs")
def get_company_bs(ticker: str, year: int | None = None, from_year: int | None = None, to_year: int | None = None) -> list[dict]:
    df = get_company_table("balancesheet", ticker, year=year, from_year=from_year, to_year=to_year)
    return df.where(df.notna(), None).to_dict(orient="records")


@router.get("/companies/{ticker}/cashflow")
@router.get("/api/v1/companies/{ticker}/cashflow")
def get_company_cashflow(ticker: str, year: int | None = None, from_year: int | None = None, to_year: int | None = None) -> list[dict]:
    df = get_company_table("cashflow", ticker, year=year, from_year=from_year, to_year=to_year)
    return df.where(df.notna(), None).to_dict(orient="records")


@router.get("/companies/{ticker}/ratios")
@router.get("/api/v1/companies/{ticker}/ratios")
def get_company_ratios(ticker: str, year: int | None = None, from_year: int | None = None, to_year: int | None = None) -> list[dict]:
    df = get_company_table("financial_ratios", ticker, year=year, from_year=from_year, to_year=to_year)
    return df.where(df.notna(), None).to_dict(orient="records")


@router.get("/companies/{ticker}/tearsheet")
@router.get("/api/v1/companies/{ticker}/tearsheet")
def get_company_tearsheet(ticker: str) -> dict:
    df = get_company_by_ticker(ticker)
    if df.empty:
        raise HTTPException(status_code=404, detail="company not found")
    return {"ticker": ticker.upper(), "company": df.iloc[0].to_dict()}
