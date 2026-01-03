"""
Dashboard Page
Application overview and key metrics
Prof. V. Ravichandran - The Mountain Path - World of Finance
"""

import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from streamlit_app.components import ComponentLibrary
from streamlit_app.config import COLORS
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
                📊 Application Dashboard
            </div>
            <h2 style='margin: 0; font-size: 28px; font-weight: 700;'>Overview & Summary</h2>
        </div>
    </div>
    """
    st.markdown(page_header_html, unsafe_allow_html=True)
    
    st.markdown("**Quick summary of loaded data and recent valuations.**")
    
    conn = FinancialDatabaseSchema.get_connection()
    cursor = conn.cursor()
    
    # Key metrics section
    st.markdown("""
    <div style='margin-top: 20px; margin-bottom: 10px;'>
        <div style='font-size: 13px; text-transform: uppercase; letter-spacing: 1px; color: {}; font-weight: 700;'>
            📈 Database Summary
        </div>
    </div>
    """.format(COLORS["dark_blue"]), unsafe_allow_html=True)
    
    cursor.execute("SELECT COUNT(*) FROM companies")
    num_companies = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM financial_periods")
    num_periods = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM dcf_calculations")
    num_valuations = cursor.fetchone()[0]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ComponentLibrary.metric_card("Companies", num_companies, card_type="info")
    with col2:
        ComponentLibrary.metric_card("Periods", num_periods, card_type="info")
    with col3:
        ComponentLibrary.metric_card("Valuations", num_valuations, card_type="success")
    with col4:
        cursor.execute("SELECT COUNT(*) FROM validation_log WHERE passed = 1")
        passed_checks = cursor.fetchone()[0]
        ComponentLibrary.metric_card("Validation Checks", passed_checks, card_type="success")
    
    st.divider()
    
    # Recent valuations section
    st.markdown("""
    <div style='margin: 20px 0 10px 0;'>
        <div style='font-size: 13px; text-transform: uppercase; letter-spacing: 1px; color: {}; font-weight: 700;'>
            💼 Recent Valuations
        </div>
    </div>
    """.format(COLORS["dark_blue"]), unsafe_allow_html=True)
    
    cursor.execute("""
        SELECT 
            c.ticker, fp.fiscal_year, dc.price_per_share,
            dc.calculation_date
        FROM dcf_calculations dc
        JOIN companies c ON dc.company_id = c.id
        JOIN financial_periods fp ON dc.base_year_id = fp.id
        ORDER BY dc.calculation_date DESC
        LIMIT 5
    """)
    
    valuations = cursor.fetchall()
    
    if valuations:
        recent_html = """
        <div style='background: white; border-radius: 8px; padding: 15px; border-left: 4px solid {}; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
        """.format(COLORS["dark_blue"])
        
        for ticker, fy, price, calc_date in valuations:
            recent_html += f"""
            <div style='
                display: flex; 
                justify-content: space-between; 
                padding: 10px 0; 
                border-bottom: 1px solid #f0f0f0;
                align-items: center;
            '>
                <div style='font-weight: 600; color: {COLORS["dark_blue"]};'>{ticker} (FY{fy})</div>
                <div style='color: {COLORS["success"]}; font-weight: 600;'>${price:.2f}/share</div>
                <div style='font-size: 11px; color: #999;'>{str(calc_date)[:10]}</div>
            </div>
            """
        
        recent_html += "</div>"
        st.markdown(recent_html, unsafe_allow_html=True)
    else:
        st.info("📌 No valuations yet. Create one in **DCF Analysis** page.")
    
    st.divider()
    
    # Footer for page
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
        Dashboard | Prof. V. Ravichandran | © 2026
    </div>
    """
    st.markdown(page_footer_html, unsafe_allow_html=True)
    
    conn.close()

if __name__ == "__main__":
    render()
