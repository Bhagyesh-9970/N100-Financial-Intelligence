import streamlit as st

# ----------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------------
# Sidebar
# ----------------------------------------------------------

st.sidebar.title("📊 N100 Financial Intelligence")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🏢 Company Profile",
        "🔍 Screener",
        "👥 Peer Comparison",
        "📈 Trend Analysis",
        "🏭 Sector Analysis",
        "💰 Capital Allocation",
        "📄 Annual Reports"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Version 1.0")

# ----------------------------------------------------------
# Routing
# ----------------------------------------------------------

if page == "🏠 Home":
    from pages import home
    home.show()

elif page == "🏢 Company Profile":
    from pages import profile
    profile.show()

elif page == "🔍 Screener":
    from pages import screener
    screener.show()

elif page == "👥 Peer Comparison":
    from pages import peers
    peers.show()

elif page == "📈 Trend Analysis":
    from pages import trends
    trends.show()

elif page == "🏭 Sector Analysis":
    from pages import sectors
    sectors.show()

elif page == "💰 Capital Allocation":
    from pages import capital
    capital.show()

elif page == "📄 Annual Reports":
    from pages import reports
    reports.show()

