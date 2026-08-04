import plotly.express as px
import streamlit as st


def sector_donut_chart(df):

    if df.empty:
        st.warning("No sector data available.")
        return

    sector_counts = (
        df.groupby("broad_sector")
        .size()
        .reset_index(name="Companies")
    )

    fig = px.pie(
        sector_counts,
        names="broad_sector",
        values="Companies",
        hole=0.55,
        title="Sector Distribution"
    )

    fig.update_layout(
        height=500,
        legend_title="Sector"
    )

    st.plotly_chart(fig, use_container_width=True)