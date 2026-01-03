"""
Settings Page
Application configuration and preferences
Prof. V. Ravichandran - The Mountain Path - World of Finance
"""

import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from streamlit_app.components import ComponentLibrary
from streamlit_app.config import COLORS, DEFAULTS
from database.schema import FinancialDatabaseSchema

def render():
    # Professional page header
    page_header_html = f"""
    <div style='
        background: linear-gradient(90deg, {COLORS["dark_blue"]} 0%, {COLORS["light_blue"]} 100%);
        padding: 25px 30px;
        border-radius: 10px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 5px solid {COLORS["gold"]};
    '>
        <div style='color: white;'>
            <div style='font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.9; margin-bottom: 5px;'>
                ⚙️ System Configuration
            </div>
            <h2 style='margin: 0; font-size: 28px; font-weight: 700;'>Settings & Configuration</h2>
        </div>
    </div>
    """
    st.markdown(page_header_html, unsafe_allow_html=True)
    
    st.markdown("**Configure default assumptions and application behavior.**")
    
    tab1, tab2, tab3 = st.tabs(["Defaults", "Database", "About"])
    
    with tab1:
        st.markdown("""
        <div style='margin: 20px 0 15px 0;'>
            <div style='font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: {}; font-weight: 700;'>
                💰 Default Valuation Assumptions
            </div>
        </div>
        """.format(COLORS["dark_blue"]), unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            default_wacc = st.slider(
                "Default WACC",
                min_value=0.01,
                max_value=0.25,
                value=DEFAULTS["wacc"],
                step=0.005,
                format="%.1%%"
            )
            st.caption("Discount rate for DCF calculations")
        
        with col2:
            default_tgr = st.slider(
                "Default Terminal Growth Rate",
                min_value=0.0,
                max_value=0.05,
                value=DEFAULTS["terminal_growth_rate"],
                step=0.005,
                format="%.2%%"
            )
            st.caption("Long-term perpetual growth rate")
        
        st.divider()
        
        default_tax = st.slider(
            "Default Tax Rate",
            min_value=0.0,
            max_value=0.5,
            value=DEFAULTS["tax_rate"],
            step=0.01,
            format="%.1%%"
        )
        st.caption("Effective tax rate for NOPAT calculations")
        
        if st.button("💾 Save Defaults", use_container_width=True, type="primary"):
            st.session_state.default_wacc = default_wacc
            st.session_state.default_tgr = default_tgr
            st.session_state.default_tax = default_tax
            st.success("✓ Settings saved to session")
    
    with tab2:
        st.markdown("""
        <div style='margin: 20px 0 15px 0;'>
            <div style='font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: {}; font-weight: 700;'>
                🗄️ Database Management
            </div>
        </div>
        """.format(COLORS["dark_blue"]), unsafe_allow_html=True)
        
        conn = FinancialDatabaseSchema.get_connection()
        cursor = conn.cursor()
        
        # Statistics
        cursor.execute("SELECT COUNT(*) FROM companies")
        num_companies = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM financial_periods")
        num_periods = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM income_statement")
        num_income = cursor.fetchone()[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ComponentLibrary.metric_card("Companies", num_companies)
        with col2:
            ComponentLibrary.metric_card("Periods", num_periods)
        with col3:
            ComponentLibrary.metric_card("Data Points", num_income)
        
        st.divider()
        
        st.markdown("""
        <div style='margin: 20px 0 15px 0;'>
            <div style='font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: {}; font-weight: 700;'>
                🔧 Advanced Options
            </div>
        </div>
        """.format(COLORS["dark_blue"]), unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Clear Cache", use_container_width=True):
                st.cache_resource.clear()
                st.cache_data.clear()
                st.success("✓ Cache cleared successfully")
        
        with col2:
            if st.button("⚠️ Reset Database", use_container_width=True):
                if st.checkbox("I understand this will delete all data"):
                    FinancialDatabaseSchema.drop_all_tables()
                    FinancialDatabaseSchema.initialize_database()
                    st.success("✓ Database reset")
        
        conn.close()
    
    with tab3:
        st.markdown("""
        <div style='margin: 20px 0 15px 0;'>
            <div style='font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: {}; font-weight: 700;'>
                🏔️ About This Platform
            </div>
        </div>
        """.format(COLORS["dark_blue"]), unsafe_allow_html=True)
        
        about_html = f"""
        <div style='
            background: linear-gradient(135deg, {COLORS["light_blue"]} 0%, rgba(173,216,230,0.2) 100%);
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid {COLORS["gold"]};
            margin-bottom: 20px;
        '>
            <div style='font-weight: 700; color: {COLORS["dark_blue"]}; margin-bottom: 10px; font-size: 14px;'>
                The Mountain Path - DCF Valuation Platform
            </div>
            <div style='font-size: 12px; line-height: 1.6; color: #333;'>
                A professional-grade financial analysis tool for:
                <ul style='margin: 10px 0; padding-left: 20px;'>
                    <li>SEC EDGAR data extraction and integration</li>
                    <li>Financial data validation and tie-outs</li>
                    <li>FCFF-based DCF valuation</li>
                    <li>Sensitivity and scenario analysis</li>
                </ul>
            </div>
        </div>
        """
        st.markdown(about_html, unsafe_allow_html=True)
        
        st.markdown("""
        **Developed By**
        
        **Prof. V. Ravichandran**
        - 28+ Years Corporate Finance & Banking Experience
        - 10+ Years Academic Excellence
        - Specialized in Financial Risk Management & Modeling
        
        **Technology Stack**
        
        - Python 3.x
        - Streamlit (Web Application Framework)
        - SQLite (Database)
        - Pandas & NumPy (Data Analysis)
        - Plotly (Visualization)
        
        **Features**
        
        ✓ Direct SEC EDGAR 10-K extraction  
        ✓ Comprehensive financial statement validation  
        ✓ Historical FCFF calculation  
        ✓ Professional DCF valuation engine  
        ✓ Multi-year scenario analysis  
        ✓ Enterprise value to equity value bridge  
        ✓ Sensitivity analysis framework
        """)
    
    st.divider()
    
    # Footer
    page_footer_html = f"""
    <div style='
        text-align: center;
        padding: 20px;
        margin-top: 30px;
        border-top: 2px solid {COLORS["light_blue"]};
        color: #999;
        font-size: 11px;
    '>
        <strong style='color: {COLORS["dark_blue"]};'>The Mountain Path - World of Finance</strong><br/>
        Settings & Configuration | Prof. V. Ravichandran | © 2026
    </div>
    """
    st.markdown(page_footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    render()
