import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard.utils.db import get_screener_data


def show():
    st.title("🏭 Sector Analysis")

    df = get_screener_data()
    if df.empty:
        st.info("No sector data is available yet.")
        return

    plot_df = df.copy()
    plot_df["market_cap"] = pd.to_numeric(plot_df["market_cap"], errors="coerce")
    plot_df["return_on_equity_pct"] = pd.to_numeric(plot_df["return_on_equity_pct"], errors="coerce")
    plot_df = plot_df.dropna(subset=["market_cap", "return_on_equity_pct"])

    if not plot_df.empty:
        fig = px.scatter(
            plot_df,
            x="market_cap",
            y="return_on_equity_pct",
            size="market_cap",
            color="sector",
            hover_name="company_name",
            size_max=50,
        )
        st.plotly_chart(fig, use_container_width=True)

    sector_summary = df.groupby("sector").agg(
        companies=("company_name", "count"),
        avg_roe=("return_on_equity_pct", "mean"),
    ).reset_index()
    st.subheader("Sector summary")
    st.dataframe(sector_summary, use_container_width=True)


def render():
    show()