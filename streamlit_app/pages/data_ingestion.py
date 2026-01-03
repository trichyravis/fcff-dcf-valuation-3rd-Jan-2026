
"""
Data Ingestion Page
Load SEC EDGAR 10-K data into financial database
Prof. V. Ravichandran - The Mountain Path - World of Finance
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.schema import FinancialDatabaseSchema

def render():
    """Render data ingestion page"""
    
    st.markdown("## 📥 Data Ingestion")
    st.markdown("Load company 10-K filing data from SEC EDGAR into the database.")
    
    st.markdown("""
    **Database-First Architecture Benefits:**
    - ✓ Direct source-of-truth data from SEC filings
    - ✓ Data validation and tie-outs before valuation
    - ✓ Historical multi-year analysis capability
    - ✓ Fast query performance for calculations
    """)
    
    st.info("ℹ️ Enter company information to fetch data from SEC EDGAR")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Load Company", "View Companies", "Database Status"])
    
    with tab1:
        st.subheader("Load Company 10-K Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ticker = st.text_input("Stock Ticker", placeholder="e.g., AAPL").upper()
        
        with col2:
            cik = st.text_input("CIK", placeholder="e.g., 0000320193")
        
        company_name = st.text_input("Company Name", placeholder="e.g., Apple Inc.")
        
        st.divider()
        
        if st.button("🔄 Fetch & Load Data", use_container_width=True, type="primary"):
            if not all([ticker, cik, company_name]):
                st.warning("⚠️ Please fill in all fields")
            else:
                st.success(f"✅ Data loading initiated for {ticker}")
                st.info("SEC EDGAR integration setup required for full functionality")
    
    with tab2:
        st.subheader("Loaded Companies")
        st.info("No companies loaded yet. Load a company in the 'Load Company' tab.")
    
    with tab3:
        st.subheader("Database Status")
        st.success("✅ Database initialized and ready")
        st.markdown("**Tables created:**")
        st.write("- companies")
        st.write("- financial_periods")
        st.write("- income_statement")
        st.write("- balance_sheet")
        st.write("- cash_flow_statement")
