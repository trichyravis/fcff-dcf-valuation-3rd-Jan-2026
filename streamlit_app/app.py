
"""
DCF Valuation Platform - Main Application
The Mountain Path - World of Finance
All pages integrated into single file
Prof. V. Ravichandran
"""

import streamlit as st
from pathlib import Path
import sys

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))

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
    "success": "#00AA00",
    "neutral": "#999999",
    "light_gray": "#EEEEEE"
}

FEATURES = {
    "dark_mode": False,
    "export": True,
    "comparison": True,
    "sensitivity": True
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
    sidebar_header = f"""
    <div style='
        background: linear-gradient(135deg, {COLORS["dark_blue"]} 0%, {COLORS["dark_blue"]} 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    '>
        <div style='text-align: center; color: white;'>
            <div style='font-size: 32px; margin-bottom: 10px;'>{BRANDING["logo_emoji"]}</div>
            <div style='font-size: 14px; font-weight: 700; letter-spacing: 0.5px;'>
                THE MOUNTAIN PATH
            </div>
            <div style='font-size: 11px; margin-top: 5px; opacity: 0.9;'>
                WORLD OF FINANCE
            </div>
        </div>
    </div>
    """
    st.markdown(sidebar_header, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='
        color: {}; 
        font-size: 12px; 
        text-transform: uppercase; 
        letter-spacing: 1px; 
        margin-bottom: 10px;
        padding-left: 5px;
        font-weight: 700;
    '>
        📍 Navigation
    </div>
    """.format(COLORS["dark_blue"]), unsafe_allow_html=True)
    
    pages = [
        "🏠 Dashboard",
        "📥 Data Ingestion",
        "✓ Data Validation",
        "📊 DCF Analysis",
        "🔍 Sensitivity Analysis",
        "⚙️ Settings"
    ]
    
    page = st.radio("Select Page", options=pages, label_visibility="collapsed")
    st.divider()
    
    st.markdown("""
    <div style='
        color: {}; 
        font-size: 12px; 
        text-transform: uppercase; 
        letter-spacing: 1px; 
        margin-bottom: 10px;
        padding-left: 5px;
        font-weight: 700;
    '>
        👤 Professional
    </div>
    """.format(COLORS["dark_blue"]), unsafe_allow_html=True)
    
    author_card = f"""
    <div style='
        background: linear-gradient(135deg, {COLORS["light_blue"]} 0%, rgba(173,216,230,0.3) 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid {COLORS["gold"]};
        margin-bottom: 15px;
    '>
        <div style='font-weight: 700; color: {COLORS["dark_blue"]}; margin-bottom: 5px; font-size: 13px;'>
            {BRANDING['author']}
        </div>
        <div style='font-size: 11px; color: #666; line-height: 1.5;'>
            {BRANDING['byline'].replace(chr(10), '<br/>')}
        </div>
    </div>
    """
    st.markdown(author_card, unsafe_allow_html=True)

# ===== MAIN HEADER =====
main_header = f"""
<div style='
    background: linear-gradient(90deg, {COLORS["dark_blue"]} 0%, {COLORS["dark_blue"]} 70%, {COLORS["gold"]} 100%);
    padding: 30px 40px;
    border-radius: 12px;
    margin-bottom: 30px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    color: white;
'>
    <div style='display: flex; align-items: center; justify-content: space-between;'>
        <div>
            <div style='font-size: 12px; letter-spacing: 2px; text-transform: uppercase; opacity: 0.9; margin-bottom: 8px;'>
                🏛️ INSTITUTIONAL FINANCIAL ANALYSIS
            </div>
            <h1 style='margin: 0; font-size: 36px; font-weight: 700; letter-spacing: -0.5px;'>
                {BRANDING["logo_emoji"]} {BRANDING["name"]}
            </h1>
            <div style='font-size: 13px; margin-top: 8px; opacity: 0.85;'>
                {BRANDING["subtitle"]}
            </div>
        </div>
        <div style='text-align: right; font-size: 11px; opacity: 0.8;'>
            <div style='margin-bottom: 4px;'><strong>Prof. V. Ravichandran</strong></div>
            <div>28+ Years Corporate Finance</div>
            <div>10+ Years Academic Excellence</div>
        </div>
    </div>
</div>
"""
st.markdown(main_header, unsafe_allow_html=True)

# ===== PAGE CONTENT =====
try:
    if page == "🏠 Dashboard":
        st.title("🏠 Dashboard")
        st.write("Welcome to the Dashboard")
        st.info("Dashboard content here")
        
    elif page == "📥 Data Ingestion":
        st.title("📥 Data Ingestion")
        st.write("Load company data from SEC EDGAR")
        col1, col2 = st.columns(2)
        with col1:
            ticker = st.text_input("Company Ticker", placeholder="e.g., AAPL")
        with col2:
            if st.button("Load Data"):
                st.success(f"Loading data for {ticker}")
        
    elif page == "✓ Data Validation":
        st.title("✓ Data Validation")
        st.write("Validate loaded financial data")
        st.info("Validation checks here")
        
    elif page == "📊 DCF Analysis":
        st.title("📊 DCF Analysis")
        st.write("DCF Valuation Analysis")
        st.info("DCF analysis content here")
        
    elif page == "🔍 Sensitivity Analysis":
        st.title("🔍 Sensitivity Analysis")
        st.write("Test valuation sensitivity")
        st.slider("Discount Rate", 0.0, 20.0, 10.0)
        st.slider("Growth Rate", 0.0, 10.0, 3.0)
        
    elif page == "⚙️ Settings":
        st.title("⚙️ Settings")
        st.write("Configure app settings")
        st.checkbox("Enable Dark Mode")
        st.checkbox("Enable Export")

except Exception as e:
    st.error(f"Error loading page: {str(e)}")
    st.write(f"Error type: {type(e).__name__}")

# ===== FOOTER =====
st.divider()
footer_html = f"""
<div style='
    background: linear-gradient(90deg, rgba(0,51,102,0.05) 0%, rgba(255,215,0,0.05) 100%);
    padding: 30px 40px;
    border-radius: 10px;
    margin-top: 40px;
    border-top: 3px solid {COLORS["gold"]};
'>
    <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 30px; text-align: center;'>
        <div>
            <div style='font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: {COLORS["dark_blue"]}; font-weight: 700; margin-bottom: 5px;'>
                Application
            </div>
            <div style='font-size: 12px; color: #666;'>
                The Mountain Path<br/>DCF Valuation
            </div>
        </div>
        <div>
            <div style='font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: {COLORS["dark_blue"]}; font-weight: 700; margin-bottom: 5px;'>
                Creator
            </div>
            <div style='font-size: 12px; color: #666;'>
                Prof. V. Ravichandran
            </div>
        </div>
        <div>
            <div style='font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: {COLORS["dark_blue"]}; font-weight: 700; margin-bottom: 5px;'>
                Version
            </div>
            <div style='font-size: 12px; color: #666;'>
                1.0 Production
            </div>
        </div>
    </div>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
