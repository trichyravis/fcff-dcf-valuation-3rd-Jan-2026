
"""
DCF Valuation Platform - Main Application
The Mountain Path - World of Finance
Prof. V. Ravichandran
"""

import streamlit as st

# ===== CONFIG =====
BRANDING = {
    "logo_emoji": "🏔️",
    "name": "The Mountain Path - DCF Valuation",
    "subtitle": "Professional Financial Analysis Platform",
    "author": "Prof. V. Ravichandran",
    "byline": "28+ Years Corporate Finance & Banking Experience\n10+ Years Academic Excellence"
}

COLORS = {
    "dark_blue": "#003366",
    "light_blue": "#ADD8E6",
    "gold": "#FFD700",
}

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title=BRANDING["name"],
    page_icon=BRANDING["logo_emoji"],
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown(f"""
    <div style='background: {COLORS["dark_blue"]}; padding: 20px; border-radius: 10px; color: white; text-align: center;'>
        <div style='font-size: 32px; margin-bottom: 10px;'>{BRANDING["logo_emoji"]}</div>
        <div style='font-size: 14px; font-weight: 700;'>THE MOUNTAIN PATH</div>
        <div style='font-size: 11px; margin-top: 5px;'>WORLD OF FINANCE</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<div style='color: {COLORS["dark_blue"]}; font-size: 12px; font-weight: 700; margin: 15px 0;'>📍 NAVIGATION</div>", unsafe_allow_html=True)
    
    pages = [
        "🏠 Dashboard",
        "📥 Data Ingestion",
        "✓ Data Validation",
        "📊 DCF Analysis",
        "🔍 Sensitivity Analysis",
        "⚙️ Settings"
    ]
    
    page = st.radio("Navigation", options=pages, label_visibility="collapsed")
    
    st.divider()
    
    st.markdown(f"<div style='color: {COLORS["dark_blue"]}; font-size: 12px; font-weight: 700; margin: 15px 0;'>👤 PROFESSIONAL</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background: {COLORS["light_blue"]}; padding: 15px; border-radius: 8px; border-left: 4px solid {COLORS["gold"]}; font-size: 11px;'>
        <div style='font-weight: 700; color: {COLORS["dark_blue"]}; margin-bottom: 5px;'>{BRANDING['author']}</div>
        <div>28+ Years Corporate Finance<br/>10+ Years Academic Excellence</div>
    </div>
    """, unsafe_allow_html=True)

# ===== MAIN HEADER =====
st.markdown(f"""
<div style='background: linear-gradient(90deg, {COLORS["dark_blue"]} 0%, {COLORS["gold"]} 100%); padding: 30px; border-radius: 12px; margin-bottom: 30px; color: white;'>
    <div style='font-size: 12px; letter-spacing: 2px; text-transform: uppercase; opacity: 0.9; margin-bottom: 8px;'>🏛️ INSTITUTIONAL FINANCIAL ANALYSIS</div>
    <h1 style='margin: 0; font-size: 36px; font-weight: 700;'>{BRANDING["logo_emoji"]} {BRANDING["name"]}</h1>
    <div style='font-size: 13px; margin-top: 8px; opacity: 0.85;'>{BRANDING["subtitle"]}</div>
</div>
""", unsafe_allow_html=True)

# ===== PAGE CONTENT =====
if page == "🏠 Dashboard":
    st.title("🏠 Dashboard")
    st.write("Welcome to the Dashboard")
    st.metric("Companies", 0)
    st.metric("Periods", 0)
    st.metric("Valuations", 0)
    
elif page == "📥 Data Ingestion":
    st.title("📥 Data Ingestion")
    st.write("Load company data from SEC EDGAR")
    ticker = st.text_input("Company Ticker", placeholder="e.g., AAPL")
    if st.button("Load Data"):
        st.success(f"Loading: {ticker}")
    
elif page == "✓ Data Validation":
    st.title("✓ Data Validation")
    st.write("Validate financial data")
    st.info("Validation checks ready")
    
elif page == "📊 DCF Analysis":
    st.title("📊 DCF Analysis")
    st.write("DCF Valuation Analysis")
    st.slider("Discount Rate", 0.0, 20.0, 10.0)
    
elif page == "🔍 Sensitivity Analysis":
    st.title("🔍 Sensitivity Analysis")
    st.write("Test valuation assumptions")
    st.slider("Sensitivity Range", 0.0, 100.0, 50.0)
    
elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    st.write("Configure app")
    st.checkbox("Enable Export")
    st.checkbox("Enable Comparison")

# ===== FOOTER =====
st.divider()
st.markdown(f"""
<div style='text-align: center; padding: 30px; color: #666; font-size: 12px; border-top: 3px solid {COLORS["gold"]};'>
    <div style='margin-bottom: 15px;'>
        <strong>The Mountain Path - DCF Valuation Platform</strong><br/>
        Prof. V. Ravichandran | Version 1.0 Production
    </div>
</div>
""", unsafe_allow_html=True)
