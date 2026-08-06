import pandas as pd
import streamlit as st

from src.dashboard.utils.db import get_screener_data


def show():
    st.title("🔍 Stock Screener")

    df = get_screener_data()

    if df.empty:
        st.warning("No screener data available.")
        return

    for column in ["return_on_equity_pct", "debt_to_equity", "net_profit_margin_pct"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    st.sidebar.subheader("Filters")

    roe = st.sidebar.slider("Minimum ROE (%)", 0.0, 100.0, 15.0)
    debt = st.sidebar.slider("Maximum Debt/Equity", 0.0, 5.0, 1.0)
    npm = st.sidebar.slider("Minimum Net Profit Margin (%)", -50.0, 100.0, 0.0)

    sector_list = ["All"] + sorted(
        df["sector"].fillna("Unknown").astype(str).unique().tolist()
    )
    sector = st.sidebar.selectbox("Sector", sector_list)

    filtered = df.copy()

    if "return_on_equity_pct" in filtered.columns:
        filtered = filtered[filtered["return_on_equity_pct"].fillna(0) >= roe]

    if "debt_to_equity" in filtered.columns:
        filtered = filtered[filtered["debt_to_equity"].fillna(999) <= debt]

    if "net_profit_margin_pct" in filtered.columns:
        filtered = filtered[filtered["net_profit_margin_pct"].fillna(-999) >= npm]

    if sector != "All":
        filtered = filtered[filtered["sector"].fillna("Unknown").astype(str) == sector]

    c1, c2 = st.columns(2)
    c1.metric("Companies Found", len(filtered))
    c2.metric("Total Companies", len(df))

    st.markdown("---")
    st.dataframe(filtered, use_container_width=True)

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download CSV", csv, "stock_screener.csv", "text/csv")


def render():
    show()