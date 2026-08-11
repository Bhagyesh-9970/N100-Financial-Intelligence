from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Any

import pandas as pd

from src.analytics.cagr import CAGRCalculator

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"
STOP_WORDS = {"AND", "THE", "OF", "FOR", "IN", "ON", "TO", "WITH", "LTD", "LIMITED", "CO", "COMPANY", "COMPANIES", "PVT", "PRIVATE", "PUBLIC", "PLC", "LLP", "CORP", "CORPORATION"}


def get_connection() -> sqlite3.Connection:
    """Create a SQLite connection for the canonical project database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _normalize_text(value: Any) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def _parse_year(value: Any) -> int | None:
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)) and not pd.isna(value):
        return int(value)
    digits = re.findall(r"\d{4}", str(value))
    if digits:
        return int(digits[0])
    return None


def _coerce_numeric(value: Any) -> float | None:
    if pd.isna(value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _read_table(table_name: str) -> pd.DataFrame:
    with get_connection() as conn:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    return df


def _read_table_with_filter(table_name: str, query: str, params: tuple[Any, ...]) -> pd.DataFrame:
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn, params=params)
    return df


def _jsonify(df: pd.DataFrame) -> list[dict[str, Any]]:
    if df.empty:
        return []
    return df.where(pd.notna(df), None).to_dict(orient="records")


def _company_name_initials(company_name: str) -> str:
    if not company_name:
        return ""
    words = re.findall(r"[A-Za-z]+", str(company_name).upper())
    filtered = [word for word in words if word not in STOP_WORDS]
    return "".join(word[0] for word in filtered[:4])


def _resolve_company_id(ticker: str) -> str:
    target = str(ticker).strip().upper()
    if not target:
        return ""

    companies = _read_table("companies")
    if not companies.empty:
        companies = companies.copy()
        companies["company_id"] = companies["company_id"].fillna("").astype(str).str.strip().str.upper()
        companies["company_name"] = companies["company_name"].fillna("").astype(str).str.strip()

        direct = companies[companies["company_id"] == target]
        if not direct.empty:
            return direct.iloc[0]["company_id"]

        name_match = companies[companies["company_name"].str.upper() == target]
        if not name_match.empty:
            return name_match.iloc[0]["company_id"]

        initials = companies[companies["company_name"].apply(lambda value: _company_name_initials(value)) == target]
        if not initials.empty:
            return initials.iloc[0]["company_id"]

        token_match = companies[companies["company_name"].str.upper().str.contains(target, na=False)]
        if not token_match.empty:
            return token_match.iloc[0]["company_id"]

    return target


def get_companies_dataframe() -> pd.DataFrame:
    """Build a company universe DataFrame from the canonical SQLite tables."""
    companies = _read_table("companies").copy()
    if companies.empty:
        return pd.DataFrame(columns=["company_id", "company_name", "sector", "broad_sector", "return_on_equity_pct", "debt_to_equity", "net_profit_margin_pct", "revenue_cagr_5yr", "fcf", "composite_score"])

    companies["company_id"] = companies["company_id"].fillna("").astype(str).str.strip().str.upper()
    companies["company_name"] = companies["company_name"].fillna("").astype(str).str.strip()
    companies["sector"] = companies["sector"].fillna("").astype(str).str.strip()
    companies["broad_sector"] = companies["broad_sector"].fillna("").astype(str).str.strip()

    sectors = _read_table("sectors").copy()
    if not sectors.empty:
        sectors["company_id"] = sectors["company_id"].fillna("").astype(str).str.strip().str.upper()
        sectors["sector"] = sectors["sector"].fillna("").astype(str).str.strip()
        sectors["broad_sector"] = sectors["broad_sector"].fillna("").astype(str).str.strip()

    ratios = _read_table("financial_ratios").copy()
    if not ratios.empty:
        ratios["company_id"] = ratios["company_id"].fillna("").astype(str).str.strip().str.upper()
        ratios["year_num"] = ratios["year"].apply(_parse_year)
        ratios = ratios.sort_values(["company_id", "year_num"], na_position="last")

    profit_loss = _read_table("profitandloss").copy()
    if not profit_loss.empty:
        profit_loss["company_id"] = profit_loss["company_id"].fillna("").astype(str).str.strip().str.upper()
        profit_loss["year_num"] = profit_loss["year"].apply(_parse_year)
        profit_loss = profit_loss.sort_values(["company_id", "year_num"], na_position="last")

    rows: list[dict[str, Any]] = []
    for _, company in companies.iterrows():
        company_id = company["company_id"]
        if not company_id:
            continue

        sector_row = sectors[sectors["company_id"] == company_id].iloc[0] if not sectors.empty and (sectors["company_id"] == company_id).any() else None
        company_ratios = ratios[ratios["company_id"] == company_id] if not ratios.empty else pd.DataFrame()
        company_pl = profit_loss[profit_loss["company_id"] == company_id] if not profit_loss.empty else pd.DataFrame()

        latest_ratio = company_ratios.iloc[-1] if not company_ratios.empty else None
        latest_pl = company_pl.iloc[-1] if not company_pl.empty else None

        roe = _coerce_numeric(latest_ratio.get("return_on_equity_pct")) if latest_ratio is not None else None
        debt_to_equity = _coerce_numeric(latest_ratio.get("debt_to_equity")) if latest_ratio is not None else None
        net_margin = _coerce_numeric(latest_ratio.get("net_profit_margin_pct")) if latest_ratio is not None else None
        opm = _coerce_numeric(latest_pl.get("opm_percentage")) if latest_pl is not None else None
        if opm is None and latest_ratio is not None:
            opm = _coerce_numeric(latest_ratio.get("operating_profit_margin_pct"))

        sales_series = [
            _coerce_numeric(value) for value in company_pl["sales"].dropna().tolist()
        ] if not company_pl.empty else []
        revenue_cagr = None
        if len(sales_series) >= 6:
            revenue_cagr, _ = CAGRCalculator.revenue_cagr_5yr(sales_series)

        fcf_series = [
            _coerce_numeric(value) for value in company_ratios["free_cash_flow_cr"].dropna().tolist()
        ] if not company_ratios.empty else []
        fcf_cagr = None
        if len(fcf_series) >= 6:
            fcf_cagr, _ = CAGRCalculator.revenue_cagr_5yr(fcf_series)

        fcf = _coerce_numeric(latest_ratio.get("free_cash_flow_cr")) if latest_ratio is not None else None
        composite_score = None
        metrics = [value for value in [roe, net_margin, revenue_cagr, fcf_cagr] if value is not None]
        if metrics:
            composite_score = round(sum(metrics) / len(metrics), 2)

        sector_value = (sector_row.get("sector") if sector_row is not None else None) or company.get("sector") or company.get("broad_sector") or "Unknown"
        broad_sector_value = (sector_row.get("broad_sector") if sector_row is not None else None) or company.get("broad_sector") or company.get("sector") or "Unknown"

        rows.append(
            {
                "company_id": company_id,
                "company_name": company["company_name"],
                "sector": sector_value,
                "broad_sector": broad_sector_value,
                "return_on_equity_pct": roe,
                "debt_to_equity": debt_to_equity,
                "net_profit_margin_pct": net_margin,
                "operating_profit_margin_pct": opm,
                "revenue_cagr_5yr": revenue_cagr,
                "fcf_cagr_5yr": fcf_cagr,
                "fcf": fcf,
                "composite_score": composite_score,
            }
        )

    return pd.DataFrame(rows)


def get_company_by_ticker(ticker: str) -> pd.DataFrame:
    df = get_companies_dataframe()
    if df.empty:
        return df
    target = _resolve_company_id(ticker)
    return df[df["company_id"].astype(str).str.upper() == target]


def get_company_table(table_name: str, ticker: str, year: int | None = None, from_year: int | None = None, to_year: int | None = None) -> pd.DataFrame:
    company_id = _resolve_company_id(ticker)
    with get_connection() as conn:
        query = f"SELECT * FROM {table_name} WHERE company_id = ?"
        params: tuple[Any, ...] = (company_id,)
        df = pd.read_sql_query(query, conn, params=params)
    if df.empty:
        return df
    if "year" in df.columns:
        df["year_num"] = df["year"].apply(_parse_year)
        if year is not None:
            df = df[df["year_num"] == year]
        if from_year is not None:
            df = df[df["year_num"] >= from_year]
        if to_year is not None:
            df = df[df["year_num"] <= to_year]
        df = df.drop(columns=["year_num"], errors="ignore")
    return df


def get_screener_dataframe(min_roe: float | None = None, max_debt: float | None = None, sector: str | None = None) -> pd.DataFrame:
    df = get_companies_dataframe()
    if df.empty:
        return df
    if min_roe is not None:
        df = df[pd.to_numeric(df["return_on_equity_pct"], errors="coerce") >= min_roe]
    if max_debt is not None:
        df = df[pd.to_numeric(df["debt_to_equity"], errors="coerce") <= max_debt]
    if sector:
        df = df[df["sector"].astype(str).str.lower() == str(sector).strip().lower()]
    return df


def get_sectors_dataframe() -> pd.DataFrame:
    df = get_companies_dataframe()
    if df.empty:
        return pd.DataFrame(columns=["sector", "companies"])
    counts = df["sector"].fillna("Unknown").astype(str).value_counts().reset_index()
    counts.columns = ["sector", "companies"]
    return counts


def get_sector_companies(sector: str) -> pd.DataFrame:
    df = get_companies_dataframe()
    if df.empty:
        return df
    return df[df["sector"].astype(str).str.lower() == str(sector).strip().lower()]


def get_peer_groups(group_name: str) -> pd.DataFrame:
    df = get_companies_dataframe()
    if df.empty:
        return df
    return df[df["sector"].astype(str).str.lower() == str(group_name).strip().lower()]


def get_market_cap(ticker: str) -> pd.DataFrame:
    company_id = _resolve_company_id(ticker)
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM market_cap WHERE company_id = ?", conn, params=(company_id,))
    return df


def get_documents(ticker: str) -> pd.DataFrame:
    company_id = _resolve_company_id(ticker)
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM documents WHERE company_id = ?", conn, params=(company_id,))
    return df


def get_portfolio_stats() -> pd.DataFrame:
    output_path = PROJECT_ROOT / "output" / "portfolio_stats.csv"
    if output_path.exists():
        return pd.read_csv(output_path)
    return pd.DataFrame(columns=["cluster_id", "cluster_name", "company_count", "mean_roe", "median_roe", "mean_debt_to_equity", "median_debt_to_equity", "revenue_cagr", "fcf_cagr", "opm"])
