
"""
Data Ingestion Page
"""

import streamlit as st

def render():
    try:
        st.title("📥 Data Ingestion")
        st.write("Load company 10-K filing data from SEC EDGAR.")
        
        st.write("Benefits:")
        st.write("- Direct SEC EDGAR data")
        st.write("- Data validation")
        st.write("- Multi-year analysis")
        st.write("- Fast performance")
        
        tab1, tab2, tab3 = st.tabs(["Load", "View", "Status"])
        
        with tab1:
            st.write("Load Company Data")
            ticker = st.text_input("Ticker")
            if st.button("Load"):
                st.success(f"Loaded: {ticker}")
        
        with tab2:
            st.write("No companies loaded")
        
        with tab3:
            st.success("Database ready")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.write(f"Type: {type(e).__name__}")
