import streamlit as st

from src.dashboard.utils.db import get_screener_data


def show():
    st.title("🏭 Sectors")

    df = get_screener_data()

    if df.empty:
        st.info("No sector data is available yet.")
        return

    sector_counts = df["sector"].fillna("Unknown").astype(str).value_counts().reset_index()
    sector_counts.columns = ["sector", "companies"]

    st.dataframe(sector_counts, use_container_width=True)


def render():
    show()