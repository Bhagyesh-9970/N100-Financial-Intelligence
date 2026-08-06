import sqlite3
from pathlib import Path
from typing import Optional, Sequence

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[3]

_EMPTY_COLUMNS = [
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
    "composite_score",
    "peer_group",
    "capital_allocation_pattern",
]


def _empty_frame(columns: Sequence[str]) -> pd.DataFrame:
    return pd.DataFrame(columns=list(columns))


def _resolve_column(df: pd.DataFrame, options: Sequence[str]) -> Optional[str]:
    for option in options:
        if option in df.columns:
            return option
    return None


def _coerce_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _find_data_files():
    candidates = []
    search_roots = [
        PROJECT_ROOT,
        PROJECT_ROOT / "data",
        PROJECT_ROOT / "src" / "data",
        PROJECT_ROOT / "assets",
    ]
    for root in search_roots:
        if not root.exists():
            continue
        for pattern in ("**/*.csv", "**/*.xlsx", "**/*.xls", "**/*.parquet", "**/*.json", "**/*.db", "**/*.sqlite", "**/*.sqlite3"):
            candidates.extend(root.glob(pattern))
    return [p for p in candidates if p.is_file()]


def _normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip() for c in out.columns]

    if "company_id" not in out.columns:
        out["company_id"] = list(range(len(out)))

    company_name_col = _resolve_column(out, ["company_name", "company", "name", "companyname", "Company Name"])
    ticker_col = _resolve_column(out, ["ticker", "symbol", "nse_ticker", "security", "Ticker"])
    sector_col = _resolve_column(out, ["sector", "broad_sector", "industry", "Sector"])
    sub_sector_col = _resolve_column(out, ["sub_sector", "subsector", "sub sector", "industry_group"])
    market_cap_col = _resolve_column(out, ["market_cap", "market_cap_crore", "market cap", "cap"])
    peer_group_col = _resolve_column(out, ["peer_group", "peer group", "group"])
    capital_pattern_col = _resolve_column(out, ["capital_allocation_pattern", "capital_pattern", "capital_allocation"])

    out["company_name"] = out[company_name_col] if company_name_col else [f"Company {i + 1}" for i in range(len(out))]
    out["ticker"] = out[ticker_col] if ticker_col else [f"STK{i + 1}" for i in range(len(out))]
    out["sector"] = out[sector_col] if sector_col else "Unknown"
    out["sub_sector"] = out[sub_sector_col] if sub_sector_col else "Unknown"
    out["market_cap"] = _coerce_numeric(out[market_cap_col]) if market_cap_col else pd.Series([pd.NA] * len(out))

    metric_aliases = {
        "return_on_equity_pct": ["return_on_equity_pct", "roe_pct", "roe", "return_on_equity", "ROE"],
        "debt_to_equity": ["debt_to_equity", "debt_equity", "d_e", "de_ratio", "debt_equity_ratio"],
        "net_profit_margin_pct": ["net_profit_margin_pct", "net_profit_margin", "npm_pct", "npm", "net_margin"],
        "revenue_cagr_5yr": ["revenue_cagr_5yr", "revenue_cagr", "cagr_5yr", "revenue_growth_5yr"],
        "pe_ratio": ["pe_ratio", "pe", "price_to_earnings", "p_e"],
        "pb_ratio": ["pb_ratio", "pb", "price_to_book", "p_b"],
        "ev_ebitda": ["ev_ebitda", "enterprise_value_ebitda", "ev_ebitda_ratio"],
        "fcf": ["fcf", "free_cash_flow", "free_cashflow", "fcf_yield"],
    }

    for std_name, aliases in metric_aliases.items():
        src_col = _resolve_column(out, aliases)
        if src_col:
            out[std_name] = _coerce_numeric(out[src_col])
        else:
            out[std_name] = pd.Series([pd.NA] * len(out))

    if "composite_score" not in out.columns:
        out["composite_score"] = pd.Series([pd.NA] * len(out))

    out["peer_group"] = out[peer_group_col] if peer_group_col else pd.Series(["Unknown"] * len(out))
    out["capital_allocation_pattern"] = out[capital_pattern_col] if capital_pattern_col else pd.Series(["Unknown"] * len(out))

    for col in _EMPTY_COLUMNS:
        if col not in out.columns:
            out[col] = pd.Series([pd.NA] * len(out))

    out["company_name"] = out["company_name"].astype(str).str.strip()
    out["ticker"] = out["ticker"].astype(str).str.strip()
    out["sector"] = out["sector"].fillna("Unknown").astype(str)

    return out[_EMPTY_COLUMNS]


def _load_dataset() -> pd.DataFrame:
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
            elif path.suffix.lower() in {".db", ".sqlite", ".sqlite3"}:
                conn = sqlite3.connect(path)
                tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
                if tables.empty:
                    conn.close()
                    continue
                table_name = tables.iloc[0, 0]
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                conn.close()
            else:
                continue
        except Exception:
            continue

        if df is not None and not df.empty:
            return _normalize_dataframe(df)

    return _empty_frame(_EMPTY_COLUMNS)


@st.cache_data(ttl=600)
def get_companies() -> pd.DataFrame:
    return _load_dataset()


@st.cache_data(ttl=600)
def get_dashboard_summary() -> pd.DataFrame:
    df = get_companies()
    if df.empty:
        return _empty_frame(["metric", "value"])

    def _safe_mean(col: str) -> float:
        s = pd.to_numeric(df[col], errors="coerce")
        return float(s.mean()) if not s.dropna().empty else 0.0

    def _safe_median(col: str) -> float:
        s = pd.to_numeric(df[col], errors="coerce")
        return float(s.median()) if not s.dropna().empty else 0.0

    debt_free = int(pd.to_numeric(df["debt_to_equity"], errors="coerce").fillna(999) <= 0.01).sum() if "debt_to_equity" in df.columns else 0

    return pd.DataFrame(
        [
            ("Total Companies", len(df)),
            ("Average ROE", _safe_mean("return_on_equity_pct")),
            ("Median P/E", _safe_median("pe_ratio")),
            ("Median D/E", _safe_median("debt_to_equity")),
            ("Debt-Free Companies", debt_free),
        ],
        columns=["metric", "value"],
    )


@st.cache_data(ttl=600)
def get_screener_data() -> pd.DataFrame:
    df = get_companies()
    if df.empty:
        return df

    if "composite_score" not in df.columns or df["composite_score"].isna().all():
        score = pd.Series([0.0] * len(df), index=df.index)
        for col in ["return_on_equity_pct", "revenue_cagr_5yr", "net_profit_margin_pct", "fcf"]:
            if col in df.columns:
                score = score + pd.to_numeric(df[col], errors="coerce").fillna(0)
        df["composite_score"] = (score / 4).fillna(0)

    return df


@st.cache_data(ttl=600)
def get_company_profile(query: Optional[str] = None) -> pd.DataFrame:
    df = get_companies()
    if df.empty or not query:
        return df

    q = str(query).strip().upper()
    result = df[df["company_name"].astype(str).str.upper().str.contains(q, na=False)]
    if result.empty and "ticker" in df.columns:
        result = df[df["ticker"].astype(str).str.upper() == q]
    return result


@st.cache_data(ttl=600)
def get_company_trends(ticker: Optional[str] = None) -> pd.DataFrame:
    df = get_companies()
    if ticker:
        df = df[df["ticker"].astype(str).str.upper() == str(ticker).strip().upper()]
    return df


@st.cache_data(ttl=600)
def get_peer_data(ticker: Optional[str] = None) -> pd.DataFrame:
    df = get_companies()
    if ticker:
        df = df[df["ticker"].astype(str).str.upper() == str(ticker).strip().upper()]
    return df


@st.cache_data(ttl=600)
def get_valuation_data() -> pd.DataFrame:
    return get_companies()


@st.cache_data(ttl=600)
def database_health() -> pd.DataFrame:
    df = get_companies()
    if df.empty:
        return pd.DataFrame([{"status": "offline", "details": "No dataset found"}])
    return pd.DataFrame([{"status": "ok", "details": "Dataset loaded successfully"}])


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