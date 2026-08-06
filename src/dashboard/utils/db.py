import sqlite3
from pathlib import Path
from typing import Optional, Sequence

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[3]
_DB_CACHE = None


def _empty_frame(columns: Sequence[str]) -> pd.DataFrame:
    return pd.DataFrame(columns=list(columns))


def _find_data_files():
    files = []
    for pattern in ("**/*.csv", "**/*.xlsx", "**/*.xls", "**/*.parquet", "**/*.json", "**/*.db", "**/*.sqlite", "**/*.sqlite3"):
        files.extend(PROJECT_ROOT.glob(pattern))
    return [p for p in files if p.is_file()]


def _load_dataset() -> pd.DataFrame:
    global _DB_CACHE
    if _DB_CACHE is not None:
        return _DB_CACHE

    for path in _find_data_files():
        try:
            if path.suffix.lower() == ".csv":
                df = pd.read_csv(path)
            elif path.suffix.lower() in {".xlsx", ".xls"}:
                df = pd.read_excel(path)
            elif path.suffix.lower() == ".parquet":
                df = pd.read_parquet(path)
            elif path.suffix.lower() == ".json":
                df = pd.read_json(path)
            else:
                continue
        except Exception:
            continue

        if df is not None and not df.empty:
            _DB_CACHE = df
            return df

    _DB_CACHE = _empty_frame(
        [
            "company_id",
            "company_name",
            "ticker",
            "sector",
            "sub_sector",
            "market_cap",
            "return_on_equity_pct",
            "debt_to_equity",
            "net_profit_margin_pct",
            "revenue_cagr_5yr",
            "pe_ratio",
            "pb_ratio",
            "ev_ebitda",
            "fcf",
        ]
    )
    return _DB_CACHE


def _ensure_columns(df: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    out = df.copy()
    for column in columns:
        if column not in out.columns:
            out[column] = pd.NA
    return out


@st.cache_data(ttl=600)
def get_companies() -> pd.DataFrame:
    df = _load_dataset()
    return _ensure_columns(
        df,
        [
            "company_id",
            "company_name",
            "ticker",
            "sector",
            "sub_sector",
            "market_cap",
            "return_on_equity_pct",
            "debt_to_equity",
            "net_profit_margin_pct",
            "revenue_cagr_5yr",
            "pe_ratio",
            "pb_ratio",
            "ev_ebitda",
            "fcf",
        ],
    )


@st.cache_data(ttl=600)
def get_ratios(ticker: Optional[str] = None, year: Optional[int] = None) -> pd.DataFrame:
    df = get_companies()
    if ticker:
        df = df[df["ticker"].astype(str).str.upper() == str(ticker).strip().upper()]
    if year and "year" in df.columns:
        df = df[df["year"] == year]
    return df


@st.cache_data(ttl=600)
def get_pl(ticker: Optional[str] = None) -> pd.DataFrame:
    return get_companies()


@st.cache_data(ttl=600)
def get_bs(ticker: Optional[str] = None) -> pd.DataFrame:
    return get_companies()


@st.cache_data(ttl=600)
def get_cf(ticker: Optional[str] = None) -> pd.DataFrame:
    return get_companies()


@st.cache_data(ttl=600)
def get_sectors() -> pd.DataFrame:
    df = get_companies()
    if df.empty:
        return _empty_frame(["sector", "companies"])
    counts = df["sector"].fillna("Unknown").astype(str).value_counts().reset_index()
    counts.columns = ["sector", "companies"]
    return counts


@st.cache_data(ttl=600)
def get_peers(group_name: Optional[str] = None) -> pd.DataFrame:
    df = get_companies()
    if group_name:
        if "peer_group" in df.columns:
            df = df[df["peer_group"].astype(str).str.lower() == str(group_name).strip().lower()]
    return df


@st.cache_data(ttl=600)
def get_valuation(ticker: Optional[str] = None) -> pd.DataFrame:
    df = get_companies()
    if ticker:
        df = df[df["ticker"].astype(str).str.upper() == str(ticker).strip().upper()]
    return df


@st.cache_data(ttl=600)
def database_health() -> pd.DataFrame:
    df = get_companies()
    if df.empty:
        return pd.DataFrame([{"status": "offline", "details": "No data source found."}])
    return pd.DataFrame([{"status": "ok", "details": "Data source loaded."}])


@st.cache_data(ttl=600)
def get_dashboard_summary() -> pd.DataFrame:
    df = get_companies()
    if df.empty:
        return _empty_frame(["metric", "value"])

    summary = pd.DataFrame(
        [
            ("Total Companies", len(df)),
            ("Average ROE", df["return_on_equity_pct"].mean() if "return_on_equity_pct" in df.columns else 0),
            ("Median P/E", df["pe_ratio"].median() if "pe_ratio" in df.columns else 0),
            ("Median D/E", df["debt_to_equity"].median() if "debt_to_equity" in df.columns else 0),
        ],
        columns=["metric", "value"],
    )
    return summary


@st.cache_data(ttl=600)
def get_screener_data() -> pd.DataFrame:
    return get_companies()


@st.cache_data(ttl=600)
def get_company_profile(query: Optional[str] = None) -> pd.DataFrame:
    df = get_companies()
    if not query:
        return df
    query = str(query).strip().upper()
    if "ticker" in df.columns:
        df = df[df["ticker"].astype(str).str.upper() == query]
    if df.empty and "company_name" in df.columns:
        df = df[df["company_name"].astype(str).str.upper().str.contains(query, na=False)]
    return df


@st.cache_data(ttl=600)
def get_company_pl(ticker: Optional[str] = None) -> pd.DataFrame:
    return get_companies()


@st.cache_data(ttl=600)
def get_company_ratios(ticker: Optional[str] = None) -> pd.DataFrame:
    return get_ratios(ticker=ticker)


@st.cache_data(ttl=600)
def get_company_trends(ticker: Optional[str] = None) -> pd.DataFrame:
    return get_companies()


@st.cache_data(ttl=600)
def get_peer_data(ticker: Optional[str] = None) -> pd.DataFrame:
    df = get_peers()
    if ticker and "ticker" in df.columns:
        df = df[df["ticker"].astype(str).str.upper() == str(ticker).strip().upper()]
    return df


@st.cache_data(ttl=600)
def get_valuation_data(ticker: Optional[str] = None) -> pd.DataFrame:
    return get_valuation(ticker=ticker)