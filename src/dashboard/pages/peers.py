import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard.utils.db import get_peer_data


def show():
    st.title("🤝 Peer Comparison")

    df = get_peer_data()
    if df.empty:
        st.info("No peer data is available yet.")
        return

    group_values = df["peer_group"].fillna("Unknown").astype(str).tolist()
    group_options = sorted(set(group_values))
    group_options = ["All"] + group_options

    selected_group = st.selectbox("Peer group", group_options)

    if selected_group != "All":
        df = df[df["peer_group"].fillna("Unknown").astype(str) == selected_group]

    if df.empty:
        st.warning("No companies found for the selected group.")
        return

    company_options = df["company_name"].astype(str).tolist()
    selected_company = st.selectbox("Benchmark company", company_options)

    row = df[df["company_name"].astype(str) == selected_company].iloc[0]
    metrics = [m for m in ["return_on_equity_pct", "net_profit_margin_pct", "revenue_cagr_5yr", "pe_ratio", "pb_ratio"] if m in df.columns]

    if len(metrics) >= 2:
        plot_df = pd.DataFrame({
            "metric": metrics + metrics,
            "value": [pd.to_numeric(row.get(m, 0), errors="coerce") for m in metrics] + [pd.to_numeric(df[m].mean(), errors="coerce") if m in df.columns else 0 for m in metrics],
            "type": ["Selected company"] * len(metrics) + ["Group average"] * len(metrics),
        })
        fig = px.bar(plot_df, x="metric", y="value", color="type", barmode="group")
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df[[c for c in ["company_name", "ticker", "sector", "peer_group", "composite_score"] if c in df.columns]], use_container_width=True)


def render():
    show()