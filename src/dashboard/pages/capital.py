import streamlit as st

from src.dashboard.utils.db import get_valuation_data


def show():
    st.title("💰 Capital & Valuation")

    valuation = get_valuation_data()

    if valuation.empty:
        st.info("No valuation data is available yet.")
        return

    st.dataframe(valuation, use_container_width=True)


def render():
    show()