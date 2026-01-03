"""
Sensitivity Analysis Page
Two-way sensitivity analysis on WACC and Terminal Growth Rate
Prof. V. Ravichandran - The Mountain Path - World of Finance
"""

import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from streamlit_app.components import ComponentLibrary
from streamlit_app.config import COLORS

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
                🔍 Valuation Analysis
            </div>
            <h2 style='margin: 0; font-size: 28px; font-weight: 700;'>Sensitivity Analysis</h2>
        </div>
    </div>
    """
    st.markdown(page_header_html, unsafe_allow_html=True)
    
    st.markdown("""
    Analyze how intrinsic value changes with different discount rate and growth assumptions.
    """)
    
    ComponentLibrary.alert(
        "💡 Select a valuation from DCF Analysis page to run sensitivity analysis",
        alert_type="info"
    )
    
    st.markdown("""
    <div style='margin: 20px 0 10px 0;'>
        <div style='font-size: 13px; text-transform: uppercase; letter-spacing: 1px; color: {}; font-weight: 700;'>
            🔜 Coming Soon
        </div>
    </div>
    """.format(COLORS["dark_blue"]), unsafe_allow_html=True)
    
    st.markdown("""
    This feature will provide:
    - **Two-Way Sensitivity Table** — WACC vs Terminal Growth Rate matrix
    - **Tornado Chart** — Ranking of key value drivers
    - **Scenario Analysis** — Bull/Base/Bear case comparisons
    - **What-If Analysis** — Custom assumption adjustments
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
        Sensitivity Analysis | Prof. V. Ravichandran | © 2026
    </div>
    """
    st.markdown(page_footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    render()
