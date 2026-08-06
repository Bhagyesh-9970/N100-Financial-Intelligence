import streamlit as st

from src.dashboard.utils.db import get_company_trends


def show():
    st.title("📈 Company Trends")

    trends = get_company_trends()

    if trends.empty:
        st.info("No trend data is available yet.")
        return

    st.dataframe(trends, use_container_width=True)


def render():
    show()