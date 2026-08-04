import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboard.utils.db import (
    get_companies,
    get_company_profile,
    get_company_pl,
    get_company_ratios,
    get_company_pros_cons,
)


# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------

def safe_value(value, suffix=""):
    if pd.isna(value):
        return "N/A"
    return f"{round(float(value),2)}{suffix}"


def latest_row(df):
    if df.empty:
        return None

    temp = df.copy()

    try:
        temp["year_sort"] = (
            temp["year"]
            .astype(str)
            .str.extract(r"(\d{4})")[0]
            .astype(float)
        )
        temp = temp.sort_values("year_sort")
    except:
        pass

    return temp.iloc[-1]


# ---------------------------------------------------
# Render Page
# ---------------------------------------------------

def render():

    st.title("📈 Company Profile")

    companies = get_companies()

    company_options = (
        companies["company_id"].astype(str)
        + " - "
        + companies["company_name"].astype(str)
    ).unique()

    selected = st.selectbox(
        "Search Company",
        sorted(company_options)
    )

    ticker = selected.split(" - ")[0]

    profile = get_company_profile(ticker)
    ratios = get_company_ratios(ticker)
    pl = get_company_pl(ticker)
    proscons = get_company_pros_cons(ticker)

    if profile.empty:

        st.warning("Ticker not found.")
        return

    company = profile.iloc[0]

    # ---------------------------------------------
    # Company Card
    # ---------------------------------------------

    st.markdown("---")

    st.subheader(company["company_name"])

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            f"""
**Ticker**

{company["company_id"]}
"""
        )

        st.markdown(
            f"""
**ISIN**

{company["isin"] if pd.notna(company["isin"]) else "N/A"}
"""
        )

    with c2:

        st.markdown(
            f"""
**Sector**

{company["sector"] if pd.notna(company["sector"]) else "N/A"}
"""
        )

        st.markdown(
            f"""
**Broad Sector**

{company["broad_sector"] if pd.notna(company["broad_sector"]) else "N/A"}
"""
        )

    with c3:

        st.markdown(
            f"""
**Industry**

{company["industry"] if pd.notna(company["industry"]) else "N/A"}
"""
        )

    st.markdown("---")

    # ---------------------------------------------
    # KPI Cards
    # ---------------------------------------------

    latest_ratio = latest_row(ratios)

    latest_pl = latest_row(pl)

    if latest_ratio is not None:

        c1, c2, c3 = st.columns(3)

        c4, c5, c6 = st.columns(3)

        with c1:

            st.metric(
                "ROE",
                safe_value(
                    latest_ratio["return_on_equity_pct"],
                    "%"
                )
            )

        with c2:

            st.metric(
                "Net Profit Margin",
                safe_value(
                    latest_ratio["net_profit_margin_pct"],
                    "%"
                )
            )

        with c3:

            st.metric(
                "Debt / Equity",
                safe_value(
                    latest_ratio["debt_to_equity"]
                )
            )

        with c4:

            st.metric(
                "Interest Coverage",
                safe_value(
                    latest_ratio["interest_coverage"]
                )
            )

        with c5:

            st.metric(
                "Free Cash Flow",
                safe_value(
                    latest_ratio["free_cash_flow_cr"]
                )
            )

        with c6:

            revenue = (
                latest_pl["sales"]
                if latest_pl is not None
                else None
            )

            st.metric(
                "Revenue",
                safe_value(revenue)
            )

    st.markdown("---")

        # =====================================================
    # Revenue vs Net Profit
    # =====================================================

    if not pl.empty:

        plot_df = pl.copy()

        plot_df["year"] = plot_df["year"].astype(str)

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=plot_df["year"],
                y=plot_df["sales"],
                name="Revenue"
            )
        )

        fig.add_trace(
            go.Bar(
                x=plot_df["year"],
                y=plot_df["net_profit"],
                name="Net Profit"
            )
        )

        fig.update_layout(

            title="Revenue vs Net Profit",

            barmode="group",

            xaxis_title="Year",

            yaxis_title="Crores",

            height=500

        )

        st.plotly_chart(fig, use_container_width=True)

    else:

        st.info("Revenue history unavailable.")

    st.markdown("---")

    # =====================================================
    # ROE Trend
    # =====================================================

    if not ratios.empty:

        trend_df = ratios.copy()

        trend_df["year"] = trend_df["year"].astype(str)

        fig2 = px.line(

            trend_df,

            x="year",

            y="return_on_equity_pct",

            markers=True,

            title="Return on Equity Trend"

        )

        fig2.update_layout(

            xaxis_title="Year",

            yaxis_title="ROE (%)",

            height=450

        )

        st.plotly_chart(fig2, use_container_width=True)

    else:

        st.info("ROE history unavailable.")

    st.markdown("---")

    # =====================================================
    # Financial Ratios Table
    # =====================================================

    st.subheader("Financial Ratios")

    if ratios.empty:

        st.warning("No ratio data available.")

    else:

        display_cols = [

            "year",

            "return_on_equity_pct",

            "net_profit_margin_pct",

            "debt_to_equity",

            "interest_coverage",

            "asset_turnover",

            "free_cash_flow_cr"

        ]

        st.dataframe(

            ratios[display_cols],

            use_container_width=True,

            hide_index=True

        )

    st.markdown("---")

    # =====================================================
    # Profit & Loss Table
    # =====================================================

    st.subheader("Profit & Loss")

    if pl.empty:

        st.warning("No Profit & Loss data available.")

    else:

        display_cols = [

            "year",

            "sales",

            "expenses",

            "operating_profit",

            "net_profit",

            "eps"

        ]

        st.dataframe(

            pl[display_cols],

            use_container_width=True,

            hide_index=True

        )

    st.markdown("---")

    # =====================================================
    # Pros & Cons
    # =====================================================

    st.subheader("Pros & Cons")

    if proscons.empty:

        st.info("No Pros / Cons available.")

    else:

        left, right = st.columns(2)

        with left:

            st.success("Pros")

            for value in proscons["pros"].dropna():

                if str(value).strip():

                    st.markdown(f"✅ {value}")

        with right:

            st.error("Cons")

            for value in proscons["cons"].dropna():

                if str(value).strip():

                    st.markdown(f"❌ {value}")

    st.markdown("---")

    st.success("Company profile loaded successfully.")