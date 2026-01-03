
"""
The Mountain Path - DCF Valuation Platform
Prof. V. Ravichandran
Super Fast - No dependencies
"""

import streamlit as st

# ===== CONFIG =====
COLORS = {
    "dark_blue": "#003366",
    "light_blue": "#ADD8E6",
    "gold": "#FFD700",
}

COMPANIES = {
    "MSFT": {"name": "Microsoft", "price": 416.75, "revenue": 245.1, "income": 88.1, "fcf": 85.0, "shares": 7.44},
    "AAPL": {"name": "Apple", "price": 250.92, "revenue": 391.0, "income": 93.7, "fcf": 110.0, "shares": 15.44},
    "GOOGL": {"name": "Alphabet", "price": 155.83, "revenue": 307.4, "income": 64.7, "fcf": 85.0, "shares": 12.66},
    "AMZN": {"name": "Amazon", "price": 208.08, "revenue": 575.2, "income": 30.3, "fcf": 50.0, "shares": 10.48},
    "TSLA": {"name": "Tesla", "price": 252.51, "revenue": 81.5, "income": 14.7, "fcf": 8.5, "shares": 3.12},
}

# ===== PAGE CONFIG =====
st.set_page_config(page_title="DCF Valuation", page_icon="🏔️", layout="wide")

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown(f"<div style='background: {COLORS['dark_blue']}; padding: 15px; border-radius: 10px; color: white; text-align: center;'><h2 style='margin: 0;'>🏔️ MOUNTAIN PATH</h2><p style='margin: 5px 0;'>DCF Valuation</p></div>", unsafe_allow_html=True)
    
    page = st.radio("Navigate", ["Dashboard", "Data", "DCF Analysis", "Settings"], label_visibility="collapsed")

# ===== MAIN HEADER =====
st.markdown(f"<div style='background: linear-gradient(90deg, {COLORS['dark_blue']} 0%, {COLORS['gold']} 100%); padding: 25px; border-radius: 10px; margin-bottom: 20px; color: white;'><h1 style='margin: 0;'>🏔️ The Mountain Path</h1><p style='margin: 5px 0;'>DCF Valuation Platform</p><small>Prof. V. Ravichandran</small></div>", unsafe_allow_html=True)

# ===== PAGES =====
if page == "Dashboard":
    st.title("📊 Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Companies", "5")
    col2.metric("Data", "2024")
    col3.metric("Status", "✅")
    col4.metric("Type", "Real")
    st.success("✅ DCF Platform Ready")
    st.info(f"Available: {', '.join(list(COMPANIES.keys()))}")

elif page == "Data":
    st.title("📥 Data Ingestion")
    ticker = st.selectbox("Company", list(COMPANIES.keys()))
    
    if ticker:
        data = COMPANIES[ticker]
        st.success(f"✅ {data['name']}")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Price", f"${data['price']:.2f}")
        col2.metric("Revenue", f"${data['revenue']:.1f}B")
        col3.metric("Net Income", f"${data['income']:.1f}B")
        col4.metric("FCF", f"${data['fcf']:.1f}B")

elif page == "DCF Analysis":
    st.title("📊 DCF Valuation")
    ticker = st.selectbox("Company", list(COMPANIES.keys()), key="dcf")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        growth = st.slider("Growth (%)", 0, 20, 5)
    with col2:
        wacc = st.slider("WACC (%)", 5, 15, 10)
    with col3:
        years = st.slider("Years", 3, 10, 5)
    
    if st.button("Calculate DCF"):
        data = COMPANIES[ticker]
        fcf = data['fcf']
        
        pv_sum = 0
        for y in range(1, years + 1):
            fcf_y = fcf * ((1 + growth/100) ** y)
            pv = fcf_y / ((1 + wacc/100) ** y)
            pv_sum += pv
        
        term_fcf = fcf * ((1 + growth/100) ** years)
        term_val = term_fcf / (wacc/100 - 2/100)
        pv_term = term_val / ((1 + wacc/100) ** years)
        
        ev = pv_sum + pv_term
        per_share = ev / data['shares']
        upside = ((per_share - data['price']) / data['price'] * 100)
        
        st.success("✅ DCF Complete")
        col1, col2, col3 = st.columns(3)
        col1.metric("Enterprise Value", f"${ev:.2f}B")
        col2.metric("Per Share", f"${per_share:.2f}")
        col3.metric("Upside", f"{upside:+.1f}%")

elif page == "Settings":
    st.title("⚙️ Settings")
    st.checkbox("Dark Mode", value=True)
    st.selectbox("Format", ["Billions", "Millions"])

st.divider()
st.markdown("<div style='text-align: center; padding: 10px; color: #666; font-size: 11px;'>The Mountain Path | Prof. V. Ravichandran | DCF Valuation Platform</div>", unsafe_allow_html=True)
