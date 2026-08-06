import pandas as pd
import streamlit as st

from src.dashboard.utils.db import get_company_profile


def show():
    st.title("👤 Company Profile")

    query = st.text_input("Search company or ticker", placeholder="e.g. RELIANCE or RELIANCEIND")
    if not query:
        st.info("Enter a company name or ticker to view the profile.")
        return

    profile = get_company_profile(query)
    if profile.empty:
        st.warning("Ticker not found — please try another.")
        return

    row = profile.iloc[0]

    st.subheader(row.get("company_name", "Unknown"))
    st.write(f"Sector: {row.get('sector', 'N/A')}")
    st.write(f"Ticker: {row.get('ticker', 'N/A')}")
    st.write(f"Sub-sector: {row.get('sub_sector', 'N/A')}")

    metrics = st.columns(6)
    metrics[0].metric("ROE", f"{pd.to_numeric(row.get('return_on_equity_pct', pd.NA), errors='coerce').item() if pd.notna(row.get('return_on_equity_pct', pd.NA)) else 'N/A'}")
    metrics[1].metric("ROCE", f"{row.get('roce', 'N/A')}")
    metrics[2].metric("Net Margin", f"{row.get('net_profit_margin_pct', 'N/A')}")
    metrics[3].metric("D/E", f"{row.get('debt_to_equity', 'N/A')}")
    metrics[4].metric("Revenue CAGR 5yr", f"{row.get('revenue_cagr_5yr', 'N/A')}")
    metrics[5].metric("FCF", f"{row.get('fcf', 'N/A')}")

    st.markdown("---")
    st.subheader("Key details")
    display_cols = [c for c in ["company_name", "ticker", "sector", "sub_sector", "market_cap", "pe_ratio", "pb_ratio", "ev_ebitda"] if c in profile.columns]
    st.dataframe(profile[display_cols], use_container_width=True)


def render():
    show()