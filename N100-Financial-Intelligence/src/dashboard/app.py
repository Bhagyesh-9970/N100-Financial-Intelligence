import streamlit as st
from pages import home, profile, screener, peers, trends, sectors, capital, reports

def main():
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose a page", 
                                      ["Home", "Profile", "Screener", "Peers", 
                                       "Trends", "Sectors", "Capital", "Reports"])

    if app_mode == "Home":
        home.show()
    elif app_mode == "Profile":
        profile.show()
    elif app_mode == "Screener":
        screener.show()
    elif app_mode == "Peers":
        peers.show()
    elif app_mode == "Trends":
        trends.show()
    elif app_mode == "Sectors":
        sectors.show()
    elif app_mode == "Capital":
        capital.show()
    elif app_mode == "Reports":
        reports.show()

if __name__ == "__main__":
    main()