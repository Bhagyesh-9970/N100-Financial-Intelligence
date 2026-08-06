import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

st.set_option("client.showSidebarNavigation", False)
st.set_page_config(page_title="N100 Financial Intelligence", layout="wide")

from src.dashboard.pages import (
    home,
    profile,
    screener,
    peers,
    trends,
    sectors,
    capital,
    reports,
)

PAGES = {
    "Home": home.show,
    "Profile": profile.show,
    "Screener": screener.show,
    "Peers": peers.show,
    "Trends": trends.show,
    "Sectors": sectors.show,
    "Capital": capital.show,
    "Reports": reports.show,
}

st.sidebar.title("N100 Financial Intelligence")
selection = st.sidebar.radio("Navigation", list(PAGES.keys()), key="page_selection")
PAGES[selection]()

