import streamlit as st

from src.dashboard.utils.db import database_health, get_dashboard_summary


def show():
    st.title("📑 Reports")

    health = database_health()
    st.dataframe(health, use_container_width=True)

    summary = get_dashboard_summary()
    if not summary.empty:
        st.subheader("Dashboard Summary")
        st.dataframe(summary, use_container_width=True)


def render():
    show()