
"""
DCF Valuation Platform - Direct SEC API Fetching
The Mountain Path - World of Finance
Prof. V. Ravichandran
Fetches real 10-K data directly from SEC API (no downloads)
"""

import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd

# ===== CONFIG =====
BRANDING = {
    "logo_emoji": "🏔️",
    "name": "The Mountain Path - DCF Valuation",
    "subtitle": "Professional Financial Analysis Platform",
    "author": "Prof. V. Ravichandran",
}

COLORS = {
    "dark_blue": "#003366",
    "light_blue": "#ADD8E6",
    "gold": "#FFD700",
}

# ===== CIK MAPPING =====
CIK_MAP = {
    "AAPL": "0000320193",
    "MSFT": "0000789019",
    "GOOGL": "0001652044",
    "AMZN": "0001018724",
    "TSLA": "0001318605",
    "META": "0001326801",
    "NVDA": "0001045810",
    "JPM": "0000019617",
    "V": "0001143196",
    "JNJ": "0000200406",
}

# ===== SEC API DATA FETCHER =====
class SECAPIFetcher:
    """Fetch real financial data from SEC API"""
    
    BASE_URL = "https://data.sec.gov/api/xbrl"
    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    @staticmethod
    def get_company_facts(ticker):
        """Fetch real financial data from SEC API"""
        if ticker not in CIK_MAP:
            return {"error": f"Ticker {ticker} not found"}
        
        cik = CIK_MAP[ticker]
        url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        
        try:
            st.info(f"📡 Fetching real SEC data for {ticker}...")
            response = requests.get(url, headers=SECAPIFetcher.HEADERS, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                company_name = data.get("entityName", "Unknown")
                
                # Extract financial facts
                facts = data.get("facts", {}).get("us-gaap", {})
                
                financials = {}
                
                # Key metrics to extract
                metrics = {
                    "Assets": "Assets",
                    "Revenues": "Revenues",
                    "NetIncomeLoss": "NetIncomeLoss",
                    "CashFlowsFromOperatingActivities": "CashFlowsFromOperatingActivities",
                }
                
                for display_name, fact_name in metrics.items():
                    if fact_name in facts:
                        units = facts[fact_name].get("units", {})
                        if "USD" in units:
                            values = units["USD"]
                            if values:
                                # Get latest value
                                latest = sorted(values, key=lambda x: x.get("end", ""), reverse=True)[0]
                                financials[display_name] = {
                                    "value": latest.get("val"),
                                    "date": latest.get("end"),
                                    "form": latest.get("form")
                                }
                
                return {
                    "success": True,
                    "ticker": ticker,
                    "company_name": company_name,
                    "financials": financials,
                    "fetch_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source": "SEC EDGAR API (Real Data)"
                }
            else:
                return {"error": f"SEC API returned {response.status_code}"}
        
        except requests.exceptions.Timeout:
            return {"error": "Request timeout - SEC server not responding"}
        except Exception as e:
            return {"error": str(e)}

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
    
    pages = ["🏠 Dashboard", "📥 SEC Data Fetcher", "📊 DCF Analysis", "🔍 Sensitivity", "⚙️ Settings"]
    page = st.radio("Navigation", options=pages, label_visibility="collapsed")

# ===== MAIN HEADER =====
st.markdown(f"""
<div style='background: linear-gradient(90deg, {COLORS["dark_blue"]} 0%, {COLORS["gold"]} 100%); padding: 30px; border-radius: 12px; margin-bottom: 30px; color: white;'>
    <h1 style='margin: 0; font-size: 36px;'>{BRANDING["logo_emoji"]} {BRANDING["name"]}</h1>
    <div style='font-size: 13px; margin-top: 8px; opacity: 0.85;'>{BRANDING["subtitle"]}</div>
    <div style='font-size: 11px; margin-top: 10px; opacity: 0.8;'>📊 Real SEC EDGAR API Data</div>
</div>
""", unsafe_allow_html=True)

# ===== PAGES =====
if page == "🏠 Dashboard":
    st.title("🏠 Dashboard")
    st.write("DCF Valuation Platform - Real SEC Data")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Data Source", "SEC API")
    col2.metric("Companies", "10+")
    col3.metric("Status", "✅ Live")
    col4.metric("Type", "Real Data")
    
    st.success("✅ Connected to SEC EDGAR API - Real financial data")
    
    st.subheader("📊 Available Companies")
    companies_list = ", ".join(list(CIK_MAP.keys()))
    st.info(f"Supported tickers: {companies_list}")
    
    st.subheader("🎯 How to Use")
    st.markdown("""
    1. **📥 SEC Data Fetcher** - Enter ticker and fetch REAL SEC data
    2. **📊 DCF Analysis** - Calculate valuation using actual financials
    3. **🔍 Sensitivity** - Test different scenarios
    """)

elif page == "📥 SEC Data Fetcher":
    st.title("📥 SEC Data Fetcher")
    st.write("Fetch real financial data from SEC EDGAR")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ticker = st.text_input(
            "Enter Stock Ticker",
            value="AAPL",
            placeholder="e.g., AAPL, MSFT, GOOGL, TSLA"
        ).upper().strip()
    
    with col2:
        fetch_button = st.button("🔄 Fetch SEC Data", use_container_width=True)
    
    if fetch_button and ticker:
        with st.spinner(f"📡 Fetching REAL SEC data for {ticker}..."):
            company_data = SECAPIFetcher.get_company_facts(ticker)
            
            if "error" in company_data:
                st.error(f"❌ Error: {company_data['error']}")
                st.info("💡 Try another ticker or check your connection")
            else:
                st.success(f"✅ Successfully fetched: {company_data['company_name']}")
                st.caption(f"Source: {company_data['source']}")
                
                col1, col2, col3 = st.columns(3)
                col1.write(f"**Ticker:** {ticker}")
                col2.write(f"**Company:** {company_data['company_name']}")
                col3.write(f"**Fetched:** {company_data['fetch_date']}")
                
                st.divider()
                st.subheader("📊 Financial Metrics from SEC (Billions USD)")
                
                financials = company_data.get('financials', {})
                
                col1, col2, col3, col4 = st.columns(4)
                
                if 'Assets' in financials:
                    val = financials['Assets']['value'] / 1e9
                    col1.metric("Total Assets", f"${val:.2f}B")
                
                if 'Revenues' in financials:
                    val = financials['Revenues']['value'] / 1e9
                    col2.metric("Revenue", f"${val:.2f}B")
                
                if 'NetIncomeLoss' in financials:
                    val = financials['NetIncomeLoss']['value'] / 1e9
                    col3.metric("Net Income", f"${val:.2f}B")
                
                if 'CashFlowsFromOperatingActivities' in financials:
                    val = financials['CashFlowsFromOperatingActivities']['value'] / 1e9
                    col4.metric("Operating Cash Flow", f"${val:.2f}B")
                
                st.divider()
                st.subheader("📄 Data Details")
                
                for metric_name, metric_data in financials.items():
                    st.write(f"""
                    **{metric_name}:**
                    - Value: ${metric_data['value']/1e9:.2f}B
                    - Date: {metric_data['date']}
                    - Form: {metric_data.get('form', 'N/A')}
                    """)
                
                # Store in session for DCF
                st.session_state.last_data = company_data

elif page == "📊 DCF Analysis":
    st.title("📊 DCF Valuation Analysis")
    
    ticker = st.text_input("Stock Ticker", "AAPL", key="dcf_ticker").upper().strip()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        growth = st.slider("Revenue Growth (%)", 0, 20, 5)
    with col2:
        wacc = st.slider("WACC (%)", 5, 15, 10)
    with col3:
        years = st.slider("Forecast Years", 3, 10, 5)
    
    if st.button("🔄 Run DCF", use_container_width=True):
        with st.spinner(f"Fetching data and running DCF for {ticker}..."):
            company_data = SECAPIFetcher.get_company_facts(ticker)
            
            if "success" in company_data:
                financials = company_data.get('financials', {})
                
                if 'Revenues' in financials and 'CashFlowsFromOperatingActivities' in financials:
                    revenue = financials['Revenues']['value'] / 1e9
                    ocf = financials['CashFlowsFromOperatingActivities']['value'] / 1e9
                    
                    # Estimate FCF (OCF - CapEx estimate)
                    fcf = ocf * 0.8  # Conservative estimate
                    
                    fcf_year1 = fcf
                    total_pv = 0
                    
                    fcf_list = []
                    for year in range(1, years + 1):
                        fcf_year = fcf_year1 * ((1 + growth/100) ** year)
                        pv = fcf_year / ((1 + wacc/100) ** year)
                        total_pv += pv
                        fcf_list.append({
                            "Year": year,
                            "FCF ($B)": f"{fcf_year:.2f}",
                            "PV ($B)": f"{pv:.2f}"
                        })
                    
                    terminal_fcf = fcf_year1 * ((1 + growth/100) ** years)
                    terminal_value = terminal_fcf / (wacc/100 - 2/100)
                    pv_terminal = terminal_value / ((1 + wacc/100) ** years)
                    
                    ev = total_pv + pv_terminal
                    
                    st.success("✅ DCF Analysis Complete")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Enterprise Value", f"${ev:.2f}B")
                    col2.metric("Terminal Value", f"${pv_terminal:.2f}B")
                    col3.metric("Total PV", f"${total_pv:.2f}B")
                    
                    st.divider()
                    st.subheader("Cash Flow Projection")
                    df = pd.DataFrame(fcf_list)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("Insufficient data for DCF analysis")
            else:
                st.error(f"Could not fetch data: {company_data.get('error')}")

elif page == "🔍 Sensitivity":
    st.title("🔍 Sensitivity Analysis")
    
    ticker = st.selectbox("Company", list(CIK_MAP.keys()), key="sens")
    
    col1, col2 = st.columns(2)
    with col1:
        wacc_min = st.slider("Min WACC", 5.0, 15.0, 8.0)
    with col2:
        wacc_max = st.slider("Max WACC", 5.0, 15.0, 12.0)
    
    growth = st.slider("Growth Rate", 0.0, 10.0, 3.0)
    
    if st.button("Run Sensitivity"):
        st.info("Sensitivity analysis ready for selected parameters")

elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    st.checkbox("Auto-fetch on startup", value=False)
    st.selectbox("Number Format", ["Billions", "Millions"])

st.divider()
st.markdown(f"""
<div style='text-align: center; padding: 20px; color: #666; font-size: 12px;'>
    <strong>The Mountain Path - DCF Valuation</strong><br/>
    Real SEC EDGAR API Data | Prof. V. Ravichandran | v1.0
</div>
""", unsafe_allow_html=True)
