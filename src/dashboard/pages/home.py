import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard.utils.db import get_companies, get_dashboard_summary


def show():
    st.title("🏠 Home")
    st.caption("N100 Financial Intelligence dashboard")

    df = get_companies()
    summary = get_dashboard_summary()

    if df.empty:
        st.info("No company data is available yet.")
        return

    metric_map = summary.set_index("metric")["value"].to_dict()

    cols = st.columns(5)
    cols[0].metric("Total Companies", int(metric_map.get("Total Companies", 0)))
    cols[1].metric("Average ROE", f"{metric_map.get('Average ROE', 0):.2f}%")
    cols[2].metric("Median P/E", f"{metric_map.get('Median P/E', 0):.2f}")
    cols[3].metric("Median D/E", f"{metric_map.get('Median D/E', 0):.2f}")
    cols[4].metric("Debt-Free Companies", int(metric_map.get("Debt-Free Companies", 0)))

    if "sector" in df.columns:
        sector_counts = df["sector"].fillna("Unknown").astype(str).value_counts().reset_index()
        sector_counts.columns = ["sector", "companies"]
        fig = px.pie(sector_counts, values="companies", names="sector", hole=0.45)
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top companies")
    top_df = df.copy()
    if "composite_score" in top_df.columns:
        top_df = top_df.sort_values("composite_score", ascending=False)
    else:
        top_df = top_df.sort_values("company_name", ascending=True)

    display_cols = [c for c in ["company_name", "ticker", "sector", "composite_score"] if c in top_df.columns]
    st.dataframe(top_df[display_cols].head(10), use_container_width=True)


def render():
    show()