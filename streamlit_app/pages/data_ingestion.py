"""
Data Ingestion Page
Load SEC EDGAR 10-K data into financial database
Prof. V. Ravichandran - The Mountain Path - World of Finance
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import logging

sys.path.insert(0, str(Path(__file__).parent.parent))

from streamlit_app.components import ComponentLibrary
from database.schema import FinancialDatabaseSchema
from extraction.sec_extractor import SECEDGARExtractor

logger = logging.getLogger(__name__)

def render():
    """Render data ingestion page"""
    
    ComponentLibrary.page_header(
        "Data Ingestion",
        ["Home", "Data Management", "Ingestion"]
    )
    
    st.markdown("""
    This page allows you to fetch 10-K filing data directly from SEC EDGAR and load it into the database.
    
    **Database-First Architecture Benefits:**
    - ✓ Direct source-of-truth data from SEC filings
    - ✓ Data validation and tie-outs before valuation
    - ✓ Historical multi-year analysis capability
    - ✓ Fast query performance for calculations
    """)
    
    # Get database connection
    conn = FinancialDatabaseSchema.get_connection()
    
    # Tabs for different operations
    tab1, tab2, tab3 = st.tabs(["Load New Company", "View Loaded Companies", "Database Status"])
    
    # ===== TAB 1: Load New Company =====
    with tab1:
        st.subheader("Load Company 10-K Data from SEC EDGAR")
        
        ComponentLibrary.form_section(
            "Company Information",
            "Provide SEC filing details for the company"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            ticker = st.text_input(
                "Stock Ticker",
                placeholder="e.g., AAPL",
                help="Company stock ticker symbol"
            ).upper()
        
        with col2:
            cik = st.text_input(
                "CIK (Central Index Key)",
                placeholder="e.g., 0000320193",
                help="10-digit CIK number from SEC"
            )
        
        company_name = st.text_input(
            "Company Name",
            placeholder="e.g., Apple Inc.",
            help="Official company name"
        )
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            load_button = st.button(
                "🔄 Fetch & Load Data",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            test_button = st.button(
                "🧪 Test Connection",
                use_container_width=True
            )
        
        # Test connection
        if test_button:
            if not cik:
                ComponentLibrary.alert("Please enter CIK", alert_type="warning")
            else:
                with st.spinner("Testing SEC EDGAR connection..."):
                    extractor = SECEDGARExtractor(conn)
                    facts_json = extractor.fetch_company_facts(cik)
                    
                    if facts_json:
                        extracted_name = facts_json.get("entityName", "Unknown")
                        ComponentLibrary.alert(
                            f"✓ Successfully connected to SEC EDGAR\nCompany: {extracted_name}",
                            alert_type="success"
                        )
                    else:
                        ComponentLibrary.alert(
                            f"✗ Failed to fetch data for CIK: {cik}",
                            alert_type="danger"
                        )
        
        # Load data
        if load_button:
            if not all([ticker, cik, company_name]):
                ComponentLibrary.alert(
                    "Please fill in all fields",
                    alert_type="warning"
                )
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text("Initializing SEC EDGAR extraction...")
                    extractor = SECEDGARExtractor(conn)
                    
                    status_text.text("Fetching company facts from SEC EDGAR...")
                    progress_bar.progress(20)
                    
                    # Process company
                    success = extractor.process_company_10k(ticker, cik, company_name)
                    
                    if success:
                        progress_bar.progress(100)
                        status_text.text("✓ Data loaded successfully!")
                        
                        ComponentLibrary.alert(
                            f"Successfully loaded 10-K data for {company_name} ({ticker})",
                            alert_type="success"
                        )
                        
                        # Show summary
                        cursor = conn.cursor()
                        cursor.execute("""
                            SELECT COUNT(*) as period_count FROM financial_periods
                            WHERE ticker = ? OR company_name LIKE ?
                        """, (ticker, f"%{company_name}%"))
                        
                        periods = cursor.fetchone()[0]
                        
                        st.info(f"📊 Loaded {periods} fiscal year periods")
                    else:
                        ComponentLibrary.alert(
                            "Failed to load data. Check CIK and try again.",
                            alert_type="danger"
                        )
                        progress_bar.progress(0)
                
                except Exception as e:
                    ComponentLibrary.alert(f"Error: {str(e)}", alert_type="danger")
                    progress_bar.progress(0)
    
    # ===== TAB 2: View Loaded Companies =====
    with tab2:
        st.subheader("Loaded Companies")
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id, c.ticker, c.company_name, 
                   COUNT(DISTINCT fp.fiscal_year) as periods,
                   MAX(fp.period_end_date) as latest_period
            FROM companies c
            LEFT JOIN financial_periods fp ON c.id = fp.company_id
            GROUP BY c.id, c.ticker, c.company_name
            ORDER BY c.company_name
        """)
        
        companies = cursor.fetchall()
        
        if companies:
            df_companies = pd.DataFrame(
                companies,
                columns=["ID", "Ticker", "Company", "Periods Loaded", "Latest Period"]
            )
            
            # Remove ID column for display
            display_df = df_companies.drop("ID", axis=1)
            ComponentLibrary.financial_table(display_df)
            
            # Select company for inspection
            st.divider()
            st.subheader("Company Details")
            
            selected_ticker = st.selectbox(
                "Select Company",
                options=df_companies["Ticker"].tolist(),
                key="company_select"
            )
            
            if selected_ticker:
                cursor.execute("""
                    SELECT fp.id, fp.fiscal_year, fp.period_end_date, 
                           fp.filing_type, fp.data_quality_score
                    FROM financial_periods fp
                    JOIN companies c ON fp.company_id = c.id
                    WHERE c.ticker = ?
                    ORDER BY fp.fiscal_year DESC
                """, (selected_ticker,))
                
                periods = cursor.fetchall()
                
                if periods:
                    df_periods = pd.DataFrame(
                        periods,
                        columns=["Period ID", "Fiscal Year", "Period End", "Filing Type", "Quality Score"]
                    )
                    
                    st.write(f"**Periods for {selected_ticker}:**")
                    ComponentLibrary.financial_table(df_periods)
        else:
            ComponentLibrary.alert(
                "No companies loaded yet. Use the 'Load New Company' tab to add data.",
                alert_type="info"
            )
    
    # ===== TAB 3: Database Status =====
    with tab3:
        st.subheader("Database Status")
        
        cursor = conn.cursor()
        
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            cursor.execute("SELECT COUNT(*) FROM companies")
            num_companies = cursor.fetchone()[0]
            ComponentLibrary.metric_card("Companies", num_companies)
        
        with col2:
            cursor.execute("SELECT COUNT(*) FROM financial_periods")
            num_periods = cursor.fetchone()[0]
            ComponentLibrary.metric_card("Periods", num_periods)
        
        with col3:
            cursor.execute("SELECT COUNT(*) FROM income_statement")
            num_income = cursor.fetchone()[0]
            ComponentLibrary.metric_card("Income Items", num_income)
        
        with col4:
            cursor.execute("SELECT COUNT(*) FROM balance_sheet")
            num_bs = cursor.fetchone()[0]
            ComponentLibrary.metric_card("Balance Sheet Items", num_bs)
        
        st.divider()
        
        # Data quality
        st.subheader("Data Quality")
        
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN data_quality_score >= 0.9 THEN 1 ELSE 0 END) as excellent,
                SUM(CASE WHEN data_quality_score >= 0.7 AND data_quality_score < 0.9 THEN 1 ELSE 0 END) as good,
                SUM(CASE WHEN data_quality_score < 0.7 THEN 1 ELSE 0 END) as poor
            FROM financial_periods
        """)
        
        quality_counts = cursor.fetchone()
        excellent, good, poor = quality_counts if quality_counts else (0, 0, 0)
        
        quality_data = {
            "Quality Level": ["Excellent (≥90%)", "Good (70-90%)", "Poor (<70%)"],
            "Count": [excellent or 0, good or 0, poor or 0]
        }
        
        df_quality = pd.DataFrame(quality_data)
        st.bar_chart(df_quality.set_index("Quality Level"))
        
        st.divider()
        
        # Database file info
        st.subheader("Database File")
        
        db_path = FinancialDatabaseSchema.DB_PATH
        if db_path.exists():
            db_size_mb = db_path.stat().st_size / (1024 * 1024)
            ComponentLibrary.metric_card("Database Size", f"{db_size_mb:.2f}", unit="MB")
            st.caption(f"Location: {db_path}")
        else:
            st.warning("Database file not found")
    
    conn.close()

if __name__ == "__main__":
    render()
