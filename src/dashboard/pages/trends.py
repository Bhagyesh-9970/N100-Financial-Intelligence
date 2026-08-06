import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard.utils.db import get_company_trends


def show():
    st.title("📈 Company Trends")

    df = get_company_trends()
    if df.empty:
        st.info("No trend data is available yet.")
        return

    query = st.text_input("Search company", placeholder="e.g. RELIANCE")
    if not query:
        st.info("Enter a company to view trend data.")
        return

    matched = df[df["company_name"].astype(str).str.upper().str.contains(query.upper(), na=False)]
    if matched.empty and "ticker" in df.columns:
        matched = df[df["ticker"].astype(str).str.upper() == query.upper()]

    if matched.empty:
        st.warning("No matching company found.")
        return

    row = matched.iloc[0]
    st.subheader(row.get("company_name", "Unknown"))

    metric_options = [m for m in ["return_on_equity_pct", "net_profit_margin_pct", "debt_to_equity", "revenue_cagr_5yr", "pe_ratio", "pb_ratio", "fcf"] if m in df.columns]
    selected_metrics = st.multiselect("Metrics", metric_options, default=metric_options[:2] if len(metric_options) >= 2 else metric_options)

    if selected_metrics:
        trend_table = pd.DataFrame({
            "metric": selected_metrics,
            "value": [row.get(m, None) for m in selected_metrics],
        })
        st.dataframe(trend_table, use_container_width=True)

    st.dataframe(matched[[c for c in ["company_name", "ticker", "sector", "peer_group", "composite_score"] if c in matched.columns]], use_container_width=True)


def render():
    show()