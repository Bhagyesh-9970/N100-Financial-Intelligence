import streamlit as st
import pandas as pd

from src.dashboard.utils.db import get_company_profile


def show():
    st.title("👤 Company Profile")

    query = st.text_input("Search company or ticker", value="AAPL").strip()

    if not query:
        st.info("Enter a company name or ticker.")
        return

    profile = get_company_profile(query)

    if profile.empty:
        st.warning("Ticker not found — please try another.")
        return

    row = profile.iloc[0]

    st.subheader(row.get("company_name", "Unknown"))
    st.write(f"Sector: {row.get('sector', 'N/A')}")
    st.write(f"Ticker: {row.get('ticker', 'N/A')}")

    metrics = st.columns(6)
    metrics[0].metric("ROE", f"{pd.to_numeric(row.get('return_on_equity_pct', 0), errors='coerce') if pd.notna(row.get('return_on_equity_pct', 0)) else 'N/A'}")
    metrics[1].metric("ROCE", f"{pd.to_numeric(row.get('roce', 0), errors='coerce') if pd.notna(row.get('roce', 0)) else 'N/A'}")
    metrics[2].metric("Net Margin", f"{pd.to_numeric(row.get('net_profit_margin_pct', 0), errors='coerce') if pd.notna(row.get('net_profit_margin_pct', 0)) else 'N/A'}")
    metrics[3].metric("D/E", f"{pd.to_numeric(row.get('debt_to_equity', 0), errors='coerce') if pd.notna(row.get('debt_to_equity', 0)) else 'N/A'}")
    metrics[4].metric("Revenue CAGR 5yr", f"{pd.to_numeric(row.get('revenue_cagr_5yr', 0), errors='coerce') if pd.notna(row.get('revenue_cagr_5yr', 0)) else 'N/A'}")
    metrics[5].metric("FCF", f"{pd.to_numeric(row.get('fcf', 0), errors='coerce') if pd.notna(row.get('fcf', 0)) else 'N/A'}")

    st.dataframe(profile[["company_name", "ticker", "sector", "market_cap"]], use_container_width=True)


def render():
    show()