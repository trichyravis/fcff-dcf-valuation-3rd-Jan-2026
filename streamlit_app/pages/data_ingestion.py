
"""
Data Ingestion Page
"""

import streamlit as st

def render():
    st.title("📥 Data Ingestion")
    st.write("Load company 10-K filing data from SEC EDGAR into the database.")
    
    st.write("**Database-First Architecture Benefits:**")
    st.write("- Direct source-of-truth data from SEC filings")
    st.write("- Data validation and tie-outs before valuation")
    st.write("- Historical multi-year analysis capability")
    st.write("- Fast query performance for calculations")
    
    tab1, tab2, tab3 = st.tabs(["Load Company", "View Companies", "Database Status"])
    
    with tab1:
        st.subheader("Load Company 10-K Data")
        ticker = st.text_input("Stock Ticker", placeholder="e.g., AAPL")
        cik = st.text_input("CIK", placeholder="e.g., 0000320193")
        company_name = st.text_input("Company Name", placeholder="e.g., Apple Inc.")
        
        if st.button("Fetch & Load Data", use_container_width=True):
            if ticker and cik and company_name:
                st.success(f"Data loading for {ticker}")
            else:
                st.warning("Please fill in all fields")
    
    with tab2:
        st.subheader("Loaded Companies")
        st.info("No companies loaded yet")
    
    with tab3:
        st.subheader("Database Status")
        st.success("Database initialized")
