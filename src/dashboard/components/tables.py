import streamlit as st


def top_companies_table(df):

    st.subheader("Top Companies")

    if df.empty:
        st.warning("No company data available.")
        return

    cols = []

    for c in [
        "company_id",
        "company_name",
        "broad_sector"
    ]:
        if c in df.columns:
            cols.append(c)

    st.dataframe(
        df[cols].head(5),
        use_container_width=True,
        hide_index=True
    )