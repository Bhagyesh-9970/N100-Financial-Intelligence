import streamlit as st

from utils.db import (
    get_dashboard_summary,
    get_companies,
    get_sectors,
)

from components.kpi_cards import show_kpi_cards
from components.charts import sector_donut_chart
from components.tables import top_companies_table
from components.sidebar import year_selector


def show():
    """
    Home Dashboard Screen
    """

    st.title("📊 Nifty 100 Financial Intelligence Dashboard")

    st.markdown(
        """
        Welcome to the **Nifty 100 Financial Intelligence Platform**.

        This dashboard provides an overview of all listed companies,
        financial health, sector distribution and performance metrics.
        """
    )

    # ==============================
    # Sidebar Filters
    # ==============================

    selected_year = year_selector()

    st.sidebar.markdown("---")
    st.sidebar.success(f"Selected Year : {selected_year}")

    # ==============================
    # KPI Section
    # ==============================

    summary = get_dashboard_summary()

    show_kpi_cards(summary)

    st.divider()

    # ==============================
    # Sector Distribution
    # ==============================

    st.subheader("📈 Sector Distribution")

    sectors = get_sectors()

    if sectors.empty:
        st.warning("No sector data available.")
    else:
        sector_donut_chart(sectors)

    st.divider()

    # ==============================
    # Top Companies
    # ==============================

    st.subheader("🏆 Top Companies")

    companies = get_companies()

    if companies.empty:
        st.warning("No company data found.")
    else:
        top_companies_table(companies)

    st.divider()

    # ==============================
    # Footer
    # ==============================

    st.caption(
        "N100 Financial Intelligence Platform | Sprint 4 Dashboard"
    )