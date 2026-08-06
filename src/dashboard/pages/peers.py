import streamlit as st

from src.dashboard.utils.db import get_peer_data


def show():
    st.title("🤝 Peer Comparison")

    peers = get_peer_data()

    if peers.empty:
        st.info("No peer data is available yet.")
        return

    st.dataframe(peers, use_container_width=True)


def render():
    show()