import streamlit as st


def show_kpi_cards(summary: dict):
    """
    Display dashboard KPI cards.
    """

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    with col1:
        st.metric(
            label="Average ROE",
            value=f"{summary.get('average_roe', 0):.2f}%"
        )

    with col2:
        st.metric(
            label="Median Debt/Equity",
            value=f"{summary.get('median_de', 0):.2f}"
        )

    with col3:
        st.metric(
            label="Total Companies",
            value=int(summary.get("total_companies", 0))
        )

    with col4:
        st.metric(
            label="Debt Free Companies",
            value=int(summary.get("debt_free", 0))
        )

    with col5:
        st.metric(
            label="Average Net Profit Margin",
            value=f"{summary.get('average_npm', 0):.2f}%"
        )

    with col6:
        st.metric(
            label="Average Asset Turnover",
            value=f"{summary.get('average_asset_turnover', 0):.2f}"
        )