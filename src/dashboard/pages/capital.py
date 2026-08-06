import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard.utils.db import get_valuation_data


def show():
    st.title("💰 Capital Allocation")

    df = get_valuation_data()
    if df.empty:
        st.info("No capital allocation data is available yet.")
        return

    if "capital_allocation_pattern" in df.columns:
        counts = df["capital_allocation_pattern"].fillna("Unknown").astype(str).value_counts().reset_index()
        counts.columns = ["pattern", "companies"]
        fig = px.treemap(counts, path=["pattern"], values="companies")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Companies by pattern")
    st.dataframe(df[[c for c in ["company_name", "ticker", "sector", "capital_allocation_pattern"] if c in df.columns]], use_container_width=True)


def render():
    show()