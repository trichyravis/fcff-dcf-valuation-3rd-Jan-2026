"""
Placeholder/Stub files for remaining application pages
These can be expanded based on specific needs
"""

# ===== DASHBOARD PAGE =====
# File: pages/dashboard.py

import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from streamlit_app.components import ComponentLibrary
from database.schema import FinancialDatabaseSchema

def render():
    st.subheader("Dashboard")
    st.markdown("""
    **Dashboard Overview**
    
    Displays key metrics and summaries for all loaded companies and valuations.
    """)
    
    conn = FinancialDatabaseSchema.get_connection()
    cursor = conn.cursor()
    
    # Key metrics
    cursor.execute("SELECT COUNT(*) FROM companies")
    num_companies = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM financial_periods")
    num_periods = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM dcf_calculations")
    num_valuations = cursor.fetchone()[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        ComponentLibrary.metric_card("Companies", num_companies)
    with col2:
        ComponentLibrary.metric_card("Periods", num_periods)
    with col3:
        ComponentLibrary.metric_card("Valuations", num_valuations)
    
    conn.close()


# ===== SENSITIVITY ANALYSIS PAGE =====
# File: pages/sensitivity.py

def render():
    st.subheader("Sensitivity Analysis")
    st.markdown("""
    **Two-Way Sensitivity Analysis**
    
    Analyze how valuation changes with different WACC and Terminal Growth Rate assumptions.
    """)
    
    st.info("Select a saved valuation to run sensitivity analysis")


# ===== SETTINGS PAGE =====
# File: pages/settings.py

def render():
    st.subheader("Settings")
    st.markdown("""
    **Application Settings**
    
    Configure default assumptions and application behavior.
    """)
    
    st.subheader("Default Assumptions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        default_wacc = st.slider("Default WACC", 0.01, 0.25, 0.08, 0.005)
    
    with col2:
        default_tgr = st.slider("Default Terminal Growth Rate", 0.0, 0.05, 0.025, 0.005)
    
    st.subheader("Database Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh Cache", use_container_width=True):
            st.cache_resource.clear()
            st.success("Cache cleared")
    
    with col2:
        if st.button("📊 Database Statistics", use_container_width=True):
            st.info("Database Statistics feature coming soon")
