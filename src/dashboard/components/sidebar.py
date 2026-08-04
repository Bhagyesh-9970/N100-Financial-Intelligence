import streamlit as st


def year_selector():

    years = [
        "All",
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024"
    ]

    return st.sidebar.selectbox(
        "Financial Year",
        years
    )