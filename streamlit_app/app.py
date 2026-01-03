
"""
DCF Valuation Platform - Main Application
The Mountain Path - World of Finance
Multi-page Streamlit application for professional financial analysis
Prof. V. Ravichandran
"""

import streamlit as st
import sys
import importlib
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from streamlit_app.config import BRANDING, COLORS, FEATURES
from streamlit_app.styles import apply_styles
from streamlit_app.components import ComponentLibrary
from database.schema import FinancialDatabaseSchema

# Page configuration
st.set_page_config(
    page_title=BRANDING["name"],
    page_icon=BRANDING["logo_emoji"],
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply styles
apply_styles(st)

# Initialize database
@st.cache_resource
def init_database():
    """Initialize database on first run"""
    FinancialDatabaseSchema.initialize_database()
    return FinancialDatabaseSchema.get_connection()

# Initialize session state
if "database_initialized" not in st.session_state:
    init_database()
    st.session_state.database_initialized = True

if "selected_company" not in st.session_state:
    st.session_state.selected_company = None

if "selected_period" not in st.session_state:
    st.session_state.selected_period = None

# ===== PROFESSIONAL SIDEBAR STYLING =====
with st.sidebar:
    # Sidebar header with branding
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
    
    # Navigation section
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
    
    pages = {
        "🏠 Dashboard": "pages/01_dashboard.py",
        "📥 Data Ingestion": "pages/02_data_ingestion.py",
        "✓ Data Validation": "pages/03_validation.py",
        "📊 DCF Analysis": "pages/04_dcf_analysis.py",
        "🔍 Sensitivity Analysis": "pages/05_sensitivity.py",
        "⚙️ Settings": "pages/06_settings.py"
    }
    
    page = st.radio("Select Page", options=list(pages.keys()), label_visibility="collapsed")
    st.divider()
    
    # About section
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
    
    st.divider()
    
    # Features section
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
        ⚡ Features
    </div>
    """.format(COLORS["dark_blue"]), unsafe_allow_html=True)
    
    for feature_name, enabled in FEATURES.items():
        status = "✓ Enabled" if enabled else "✗ Disabled"
        status_color = COLORS["success"] if enabled else COLORS["neutral"]
        feature_label = feature_name.replace("_", " ").title()
        st.caption(f"<span style='color: {status_color};'>{status}</span> — {feature_label}", unsafe_allow_html=True)
    
    st.divider()
    
    # Sidebar footer
    sidebar_footer = f"""
    <div style='
        text-align: center;
        padding: 15px;
        border-top: 1px solid {COLORS["light_gray"]};
        margin-top: 20px;
        color: #999;
        font-size: 11px;
    '>
        <div style='margin-bottom: 8px;'>
            <strong style='color: {COLORS["dark_blue"]}; font-size: 12px;'>Version</strong><br/>
            1.0 Production Ready
        </div>
        <div style='font-size: 10px; opacity: 0.7;'>
            © 2026 Mountain Path Finance<br/>
            All Rights Reserved
        </div>
    </div>
    """
    st.markdown(sidebar_footer, unsafe_allow_html=True)

# ===== MAIN CONTENT AREA HEADER =====
# Professional header for main content
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

# Route to selected page
# Route to selected page
import importlib

if page == "🏠 Dashboard":
    dashboard_page = importlib.import_module('streamlit_app.pages.dashboard')
    dashboard_page.render()

elif page == "📥 Data Ingestion":
    ingestion_page = importlib.import_module('streamlit_app.pages.data_ingestion')
    ingestion_page.render()

elif page == "✓ Data Validation":
    validation_page = importlib.import_module('streamlit_app.pages.validation')
    validation_page.render()

elif page == "📊 DCF Analysis":
    dcf_page = importlib.import_module('streamlit_app.pages.dcf_analysis')
    dcf_page.render()

elif page == "🔍 Sensitivity Analysis":
    sensitivity_page = importlib.import_module('streamlit_app.pages.sensitivity')
    sensitivity_page.render()

elif page == "⚙️ Settings":
    settings_page = importlib.import_module('streamlit_app.pages.settings')
    settings_page.render()

# ===== PROFESSIONAL FOOTER =====
st.divider()

footer_html = f"""
<div style='
    background: linear-gradient(90deg, rgba(0,51,102,0.05) 0%, rgba(255,215,0,0.05) 100%);
    padding: 30px 40px;
    border-radius: 10px;
    margin-top: 40px;
    border-top: 3px solid {COLORS["gold"]};
    border-bottom: 1px solid {COLORS["light_blue"]};
'>
    <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 30px; text-align: center;'>
        <div>
            <div style='font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: {COLORS["dark_blue"]}; font-weight: 700; margin-bottom: 5px;'>
                Application
            </div>
            <div style='font-size: 12px; color: #666;'>
                The Mountain Path<br/>DCF Valuation Platform
            </div>
        </div>
        <div>
            <div style='font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: {COLORS["dark_blue"]}; font-weight: 700; margin-bottom: 5px;'>
                Creator
            </div>
            <div style='font-size: 12px; color: #666;'>
                Prof. V. Ravichandran<br/>
                <span style='font-size: 11px; color: #999;'>28+ Years Finance | 10+ Years Academic</span>
            </div>
        </div>
        <div>
            <div style='font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: {COLORS["dark_blue"]}; font-weight: 700; margin-bottom: 5px;'>
                Version
            </div>
            <div style='font-size: 12px; color: #666;'>
                1.0 Production Ready<br/>
                <span style='font-size: 11px; color: #999;'>January 2026</span>
            </div>
        </div>
    </div>
    <div style='
        text-align: center; 
        margin-top: 20px; 
        padding-top: 20px; 
        border-top: 1px solid {COLORS["light_blue"]};
        color: #999; 
        font-size: 10px;
    '>
        <strong style='color: {COLORS["dark_blue"]}; font-size: 11px;'>
            🏔️ The Mountain Path - World of Finance
        </strong><br/>
        Professional Financial Analysis Platform | © 2026 All Rights Reserved<br/>
        <span style='color: {COLORS["success"]}; margin-top: 5px; display: inline-block;'>
            ✓ Production Ready | Database-First Architecture | SEC EDGAR Integration
        </span>
    </div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
