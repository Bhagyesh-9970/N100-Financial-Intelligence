import pandas as pd
import streamlit as st

from src.dashboard.utils.db import get_screener_data


def show():
    st.title("🔍 Stock Screener")

    df = get_screener_data()
    if df.empty:
        st.warning("No screener data available.")
        return

    for column in ["return_on_equity_pct", "debt_to_equity", "net_profit_margin_pct", "revenue_cagr_5yr", "pe_ratio", "pb_ratio", "fcf"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    st.sidebar.subheader("Filters")

    if "roe_min" not in st.session_state:
        st.session_state.roe_min = 15.0
    if "debt_max" not in st.session_state:
        st.session_state.debt_max = 1.0
    if "npm_min" not in st.session_state:
        st.session_state.npm_min = 0.0
    if "fcf_min" not in st.session_state:
        st.session_state.fcf_min = 0.0
    if "revenue_cagr_min" not in st.session_state:
        st.session_state.revenue_cagr_min = 0.0
    if "pe_max" not in st.session_state:
        st.session_state.pe_max = 50.0
    if "pb_max" not in st.session_state:
        st.session_state.pb_max = 10.0

    def set_preset(preset):
        presets = {
            "Quality": {"roe_min": 15.0, "debt_max": 1.0, "npm_min": 8.0, "fcf_min": 0.0, "revenue_cagr_min": 0.0, "pe_max": 40.0, "pb_max": 6.0},
            "Value": {"roe_min": 8.0, "debt_max": 0.8, "npm_min": 0.0, "fcf_min": 0.0, "revenue_cagr_min": 0.0, "pe_max": 25.0, "pb_max": 3.0},
            "Growth": {"roe_min": 20.0, "debt_max": 1.5, "npm_min": 10.0, "fcf_min": 1.0, "revenue_cagr_min": 10.0, "pe_max": 60.0, "pb_max": 8.0},
            "Dividend": {"roe_min": 10.0, "debt_max": 1.0, "npm_min": 5.0, "fcf_min": 0.0, "revenue_cagr_min": 0.0, "pe_max": 35.0, "pb_max": 5.0},
            "Debt-Free": {"roe_min": 12.0, "debt_max": 0.2, "npm_min": 0.0, "fcf_min": 0.0, "revenue_cagr_min": 0.0, "pe_max": 30.0, "pb_max": 4.0},
            "Turnaround": {"roe_min": 5.0, "debt_max": 1.5, "npm_min": -5.0, "fcf_min": -1.0, "revenue_cagr_min": -5.0, "pe_max": 70.0, "pb_max": 12.0},
        }
        values = presets.get(preset, {})
        st.session_state.roe_min = values.get("roe_min", 15.0)
        st.session_state.debt_max = values.get("debt_max", 1.0)
        st.session_state.npm_min = values.get("npm_min", 0.0)
        st.session_state.fcf_min = values.get("fcf_min", 0.0)
        st.session_state.revenue_cagr_min = values.get("revenue_cagr_min", 0.0)
        st.session_state.pe_max = values.get("pe_max", 50.0)
        st.session_state.pb_max = values.get("pb_max", 10.0)

    preset_cols = st.sidebar.columns(3)
    for idx, preset in enumerate(["Quality", "Value", "Growth"]):
        if preset_cols[idx].button(preset):
            set_preset(preset)

    preset_cols2 = st.sidebar.columns(3)
    for idx, preset in enumerate(["Dividend", "Debt-Free", "Turnaround"]):
        if preset_cols2[idx].button(preset):
            set_preset(preset)

    roe_min = st.sidebar.slider("Minimum ROE (%)", 0.0, 100.0, key="roe_min")
    debt_max = st.sidebar.slider("Maximum Debt/Equity", 0.0, 5.0, key="debt_max")
    npm_min = st.sidebar.slider("Minimum Net Profit Margin (%)", -50.0, 100.0, key="npm_min")
    fcf_min = st.sidebar.slider("Minimum FCF", -100.0, 1000.0, key="fcf_min")
    revenue_cagr_min = st.sidebar.slider("Minimum Revenue CAGR 5yr (%)", -100.0, 100.0, key="revenue_cagr_min")
    pe_max = st.sidebar.slider("Maximum P/E", 0.0, 200.0, key="pe_max")
    pb_max = st.sidebar.slider("Maximum P/B", 0.0, 100.0, key="pb_max")

    sector_list = ["All"] + sorted(df["sector"].fillna("Unknown").astype(str).unique().tolist())
    sector = st.sidebar.selectbox("Sector", sector_list)

    filtered = df.copy()

    if "return_on_equity_pct" in filtered.columns:
        filtered = filtered[filtered["return_on_equity_pct"].fillna(-999) >= roe_min]
    if "debt_to_equity" in filtered.columns:
        filtered = filtered[filtered["debt_to_equity"].fillna(999) <= debt_max]
    if "net_profit_margin_pct" in filtered.columns:
        filtered = filtered[filtered["net_profit_margin_pct"].fillna(-999) >= npm_min]
    if "fcf" in filtered.columns:
        filtered = filtered[filtered["fcf"].fillna(-999) >= fcf_min]
    if "revenue_cagr_5yr" in filtered.columns:
        filtered = filtered[filtered["revenue_cagr_5yr"].fillna(-999) >= revenue_cagr_min]
    if "pe_ratio" in filtered.columns:
        filtered = filtered[filtered["pe_ratio"].fillna(999) <= pe_max]
    if "pb_ratio" in filtered.columns:
        filtered = filtered[filtered["pb_ratio"].fillna(999) <= pb_max]

    if sector != "All":
        filtered = filtered[filtered["sector"].fillna("Unknown").astype(str) == sector]

    c1, c2 = st.columns(2)
    c1.metric("Companies Found", len(filtered))
    c2.metric("Total Companies", len(df))

    st.markdown("---")
    display_cols = [c for c in ["company_name", "ticker", "sector", "composite_score", "return_on_equity_pct", "debt_to_equity", "net_profit_margin_pct", "pe_ratio", "pb_ratio", "fcf"] if c in filtered.columns]
    st.dataframe(filtered[display_cols], use_container_width=True)

    csv_bytes = filtered[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download CSV", csv_bytes, "screener_export.csv", "text/csv")


def render():
    show()