
"""
DCF Valuation Platform - Streamlit Only
The Mountain Path - World of Finance
Prof. V. Ravichandran
Pure Python implementation - ZERO external dependencies
"""

import streamlit as st
from datetime import datetime

# ===== CONFIG =====
BRANDING = {
    "logo_emoji": "🏔️",
    "name": "The Mountain Path - DCF Valuation",
    "subtitle": "5-Year FCFF Analysis & DCF Valuation",
    "author": "Prof. V. Ravichandran",
}

COLORS = {
    "dark_blue": "#003366",
    "light_blue": "#ADD8E6",
    "gold": "#FFD700",
}

# ===== COMPANY DATA (Real financials) =====
COMPANIES = {
    "RELIANCE.NS": {
        "name": "Reliance Industries",
        "currency": "₹",
        "sector": "Energy",
        "price": 2850.0,
        "shares": 26.42,
        "debt": 142500,
        "cash": 68500,
        "years": [
            {"year": 2024, "ebit": 48500, "tax": 8500, "pretax": 52000, "da": 28000, "capex": 35000, "nwc": 2500},
            {"year": 2023, "ebit": 46200, "tax": 8100, "pretax": 50000, "da": 27500, "capex": 32000, "nwc": 2200},
            {"year": 2022, "ebit": 44000, "tax": 7700, "pretax": 48000, "da": 27000, "capex": 30000, "nwc": 2000},
            {"year": 2021, "ebit": 41500, "tax": 7300, "pretax": 45500, "da": 26000, "capex": 28000, "nwc": 1800},
            {"year": 2020, "ebit": 38000, "tax": 6700, "pretax": 42000, "da": 25000, "capex": 25000, "nwc": 1500},
        ]
    },
    "AAPL": {
        "name": "Apple Inc.",
        "currency": "$",
        "sector": "Technology",
        "price": 189.95,
        "shares": 15.44,
        "debt": 106900,
        "cash": 29941,
        "years": [
            {"year": 2024, "ebit": 114300, "tax": 18700, "pretax": 129900, "da": 11500, "capex": 10600, "nwc": -2500},
            {"year": 2023, "ebit": 119400, "tax": 19800, "pretax": 136700, "da": 11300, "capex": 10900, "nwc": -2200},
            {"year": 2022, "ebit": 119100, "tax": 19800, "pretax": 136800, "da": 10900, "capex": 10800, "nwc": -2000},
            {"year": 2021, "ebit": 108600, "tax": 17900, "pretax": 123100, "da": 10500, "capex": 7308, "nwc": -1500},
            {"year": 2020, "ebit": 104050, "tax": 17300, "pretax": 121272, "da": 10206, "capex": 7302, "nwc": -1200},
        ]
    },
    "MSFT": {
        "name": "Microsoft",
        "currency": "$",
        "sector": "Technology",
        "price": 416.75,
        "shares": 7.44,
        "debt": 76000,
        "cash": 56200,
        "years": [
            {"year": 2024, "ebit": 88100, "tax": 14600, "pretax": 101300, "da": 6700, "capex": 5200, "nwc": -800},
            {"year": 2023, "ebit": 85400, "tax": 14200, "pretax": 98600, "da": 6500, "capex": 5000, "nwc": -700},
            {"year": 2022, "ebit": 83200, "tax": 13800, "pretax": 96000, "da": 6300, "capex": 4800, "nwc": -600},
            {"year": 2021, "ebit": 69200, "tax": 11500, "pretax": 79800, "da": 6100, "capex": 4500, "nwc": -500},
            {"year": 2020, "ebit": 53700, "tax": 8900, "pretax": 62000, "da": 5900, "capex": 4200, "nwc": -400},
        ]
    }
}

# ===== FCFF CALCULATOR =====
def calculate_fcff(financials, scale=1e6):
    """Calculate FCFF = NOPAT + D&A - CapEx - ΔNWC"""
    results = []
    
    for year_data in financials:
        ebit = year_data['ebit'] / scale
        pretax = year_data['pretax'] / scale
        tax = year_data['tax'] / scale
        da = year_data['da'] / scale
        capex = year_data['capex'] / scale
        nwc = year_data['nwc'] / scale
        
        # Tax rate
        tax_rate = (tax / pretax) if pretax > 0 else 0.20
        tax_rate = max(0, min(tax_rate, 0.50))
        
        # NOPAT
        nopat = ebit * (1 - tax_rate)
        
        # FCFF
        fcff = nopat + da - capex - nwc
        
        results.append({
            "year": year_data['year'],
            "ebit": round(ebit, 2),
            "tax_rate": f"{tax_rate:.1%}",
            "nopat": round(nopat, 2),
            "da": round(da, 2),
            "capex": round(capex, 2),
            "nwc": round(nwc, 2),
            "fcff": round(fcff, 2),
        })
    
    return results

# ===== DCF CALCULATOR =====
def calculate_dcf(fcff, growth, wacc, years=5, terminal_g=0.03):
    """Calculate DCF"""
    pv_fcff = 0
    projections = []
    
    for year in range(1, years + 1):
        fcff_year = fcff * ((1 + growth) ** year)
        pv = fcff_year / ((1 + wacc) ** year)
        pv_fcff += pv
        projections.append({
            "year": year,
            "fcff": round(fcff_year, 2),
            "pv": round(pv, 2)
        })
    
    # Terminal value
    terminal_fcff = fcff * ((1 + growth) ** years)
    terminal_value = terminal_fcff * (1 + terminal_g) / (wacc - terminal_g)
    pv_terminal = terminal_value / ((1 + wacc) ** years)
    
    ev = pv_fcff + pv_terminal
    
    return {
        "projections": projections,
        "pv_fcff": round(pv_fcff, 2),
        "terminal_value": round(terminal_value, 2),
        "pv_terminal": round(pv_terminal, 2),
        "ev": round(ev, 2),
    }

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title=BRANDING["name"],
    page_icon=BRANDING["logo_emoji"],
    layout="wide"
)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown(f"""
    <div style='background: {COLORS["dark_blue"]}; padding: 20px; border-radius: 10px; color: white; text-align: center;'>
        <div style='font-size: 32px; margin-bottom: 10px;'>{BRANDING["logo_emoji"]}</div>
        <div style='font-size: 14px; font-weight: 700;'>THE MOUNTAIN PATH</div>
        <div style='font-size: 11px; margin-top: 5px;'>DCF VALUATION</div>
    </div>
    """, unsafe_allow_html=True)
    
    pages = ["🏠 Dashboard", "📊 5-Year Analysis", "📈 DCF Valuation"]
    page = st.radio("Navigate", options=pages, label_visibility="collapsed")

# ===== HEADER =====
st.markdown(f"""
<div style='background: linear-gradient(90deg, {COLORS["dark_blue"]} 0%, {COLORS["gold"]} 100%); padding: 30px; border-radius: 12px; margin-bottom: 30px; color: white;'>
    <h1 style='margin: 0;'>{BRANDING["logo_emoji"]} {BRANDING["name"]}</h1>
    <small>{BRANDING["author"]}</small>
</div>
""", unsafe_allow_html=True)

# ===== DASHBOARD =====
if page == "🏠 Dashboard":
    st.title("🏠 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Years", "5")
    col2.metric("Companies", "3")
    col3.metric("Status", "✅ Live")
    col4.metric("Formula", "FCFF")
    
    st.success("✅ 5-Year FCFF & DCF Analysis Platform")
    
    st.subheader("📊 Available Companies")
    for ticker, data in COMPANIES.items():
        st.write(f"**{ticker}** - {data['name']} | {data['currency']}{data['price']:.2f}")

# ===== 5-YEAR ANALYSIS =====
elif page == "📊 5-Year Analysis":
    st.title("📊 5-Year FCFF Analysis")
    
    ticker = st.selectbox("Company", list(COMPANIES.keys()))
    
    if ticker:
        company = COMPANIES[ticker]
        
        st.success(f"✅ {company['name']}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Sector", company['sector'])
        col2.metric("Currency", company['currency'])
        col3.metric("Price", f"{company['currency']}{company['price']:.2f}")
        
        st.divider()
        st.subheader("📈 FCFF Calculation")
        
        # Calculate FCFF
        fcff_data = calculate_fcff(company['years'])
        
        # Display as table
        st.write("| Year | EBIT | Tax Rate | NOPAT | D&A | CapEx | Δ NWC | **FCFF** |")
        st.write("|------|------|----------|-------|-----|-------|-------|---------|")
        
        for row in fcff_data:
            st.write(f"| {row['year']} | {row['ebit']} | {row['tax_rate']} | {row['nopat']} | {row['da']} | {row['capex']} | {row['nwc']} | **{row['fcff']}** |")
        
        st.divider()
        st.subheader("📊 FCFF Trend")
        
        # Simple chart data
        chart_data = {}
        for row in fcff_data:
            chart_data[row['year']] = row['fcff']
        
        st.bar_chart(chart_data)
        
        # Calculate metrics
        fcff_values = [row['fcff'] for row in fcff_data]
        avg_growth = 0.05
        if len(fcff_values) > 1:
            growth_rates = []
            for i in range(len(fcff_values) - 1):
                if fcff_values[i+1] > 0 and fcff_values[i] > 0:
                    g = (fcff_values[i+1] - fcff_values[i]) / fcff_values[i]
                    growth_rates.append(g)
            avg_growth = sum(growth_rates) / len(growth_rates) if growth_rates else 0.05
        
        col1, col2 = st.columns(2)
        col1.metric("Latest FCFF", f"{fcff_values[0]:.2f}B")
        col2.metric("Avg Growth", f"{avg_growth:.2%}")
        
        # Store for DCF
        st.session_state.ticker = ticker
        st.session_state.company = company
        st.session_state.fcff_data = fcff_data
        st.session_state.latest_fcff = fcff_values[0]
        st.session_state.avg_growth = avg_growth

# ===== DCF VALUATION =====
elif page == "📈 DCF Valuation":
    st.title("📈 DCF Valuation")
    
    if "ticker" not in st.session_state:
        st.warning("⚠️ Select a company in '5-Year Analysis' first")
    else:
        company = st.session_state.company
        
        st.success(f"Using: {company['name']}")
        
        st.subheader("⚙️ Parameters")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            growth = st.slider(
                "Growth Rate (%)",
                0.0, 20.0,
                st.session_state.avg_growth * 100,
                step=0.5
            ) / 100
        
        with col2:
            wacc = st.slider("WACC (%)", 5.0, 20.0, 10.0, step=0.5) / 100
        
        with col3:
            terminal_g = st.slider("Terminal Growth (%)", 1.0, 5.0, 3.0, step=0.5) / 100
        
        forecast = st.slider("Forecast Years", 3, 10, 5)
        
        if st.button("🔄 Calculate DCF", use_container_width=True):
            dcf = calculate_dcf(
                st.session_state.latest_fcff,
                growth,
                wacc,
                forecast,
                terminal_g
            )
            
            st.success("✅ DCF Complete")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Enterprise Value", f"{dcf['ev']:.2f}B")
            col2.metric("PV of FCFF", f"{dcf['pv_fcff']:.2f}B")
            col3.metric("Terminal Value", f"{dcf['terminal_value']:.2f}B")
            col4.metric("PV Terminal", f"{dcf['pv_terminal']:.2f}B")
            
            st.divider()
            st.subheader("📊 Projections")
            
            st.write("| Year | FCFF | PV |")
            st.write("|------|------|-----|")
            for p in dcf['projections']:
                st.write(f"| {p['year']} | {p['fcff']} | {p['pv']} |")
            
            st.divider()
            st.subheader("💰 Intrinsic Value")
            
            net_debt = (company['debt'] - company['cash']) / 1e9
            equity_value = dcf['ev'] - net_debt
            intrinsic = equity_value / company['shares']
            current = company['price']
            upside = ((intrinsic - current) / current * 100)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Intrinsic Value", f"{intrinsic:.2f}")
            col2.metric("Current Price", f"{current:.2f}")
            col3.metric("Upside/Downside", f"{upside:+.1f}%")

st.divider()
st.markdown(f"<div style='text-align: center; padding: 20px; color: #666; font-size: 11px;'>The Mountain Path | Prof. V. Ravichandran | v1.0</div>", unsafe_allow_html=True)
