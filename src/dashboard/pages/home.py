import pandas as pd
import streamlit as st

from src.dashboard.utils.db import get_dashboard_summary


def show():
    st.title("🏠 Home")
    st.write("Financial intelligence dashboard")

    summary = get_dashboard_summary()

    if summary.empty:
        st.info("No dashboard summary data is available yet.")
        return

    st.dataframe(summary, use_container_width=True)


def render():
    show()