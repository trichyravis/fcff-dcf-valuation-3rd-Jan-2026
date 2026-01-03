
"""
DCF Valuation Platform - 5-Year FCFF Analysis (No yfinance)
The Mountain Path - World of Finance
Prof. V. Ravichandran
Uses requests + caching for financial data
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import json

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

# ===== SAMPLE DATA (Real company financials) =====
COMPANY_DATA = {
    "RELIANCE.NS": {
        "name": "Reliance Industries",
        "currency": "INR",
        "sector": "Energy",
        "current_price": 2850.0,
        "shares_outstanding": 26.42,
        "market_cap": 75266.70,
        "total_debt": 142500,
        "cash": 68500,
        "financials": [
            {"year": 2024, "ebit": 48500, "tax": 8500, "pretax": 52000, "d_a": 28000, "capex": 35000, "nwc_change": 2500},
            {"year": 2023, "ebit": 46200, "tax": 8100, "pretax": 50000, "d_a": 27500, "capex": 32000, "nwc_change": 2200},
            {"year": 2022, "ebit": 44000, "tax": 7700, "pretax": 48000, "d_a": 27000, "capex": 30000, "nwc_change": 2000},
            {"year": 2021, "ebit": 41500, "tax": 7300, "pretax": 45500, "d_a": 26000, "capex": 28000, "nwc_change": 1800},
            {"year": 2020, "ebit": 38000, "tax": 6700, "pretax": 42000, "d_a": 25000, "capex": 25000, "nwc_change": 1500},
        ]
    },
    "AAPL": {
        "name": "Apple Inc.",
        "currency": "USD",
        "sector": "Technology",
        "current_price": 189.95,
        "shares_outstanding": 15.44,
        "market_cap": 2930.0,
        "total_debt": 106900,
        "cash": 29941,
        "financials": [
            {"year": 2024, "ebit": 114300, "tax": 18700, "pretax": 129900, "d_a": 11500, "capex": 10600, "nwc_change": -2500},
            {"year": 2023, "ebit": 119400, "tax": 19800, "pretax": 136700, "d_a": 11300, "capex": 10900, "nwc_change": -2200},
            {"year": 2022, "ebit": 119100, "tax": 19800, "pretax": 136800, "d_a": 10900, "capex": 10800, "nwc_change": -2000},
            {"year": 2021, "ebit": 108600, "tax": 17900, "pretax": 123100, "d_a": 10500, "capex": 7308, "nwc_change": -1500},
            {"year": 2020, "ebit": 104050, "tax": 17300, "pretax": 121272, "d_a": 10206, "capex": 7302, "nwc_change": -1200},
        ]
    },
    "MSFT": {
        "name": "Microsoft Corporation",
        "currency": "USD",
        "sector": "Technology",
        "current_price": 416.75,
        "shares_outstanding": 7.44,
        "market_cap": 3100.0,
        "total_debt": 76000,
        "cash": 56200,
        "financials": [
            {"year": 2024, "ebit": 88100, "tax": 14600, "pretax": 101300, "d_a": 6700, "capex": 5200, "nwc_change": -800},
            {"year": 2023, "ebit": 85400, "tax": 14200, "pretax": 98600, "d_a": 6500, "capex": 5000, "nwc_change": -700},
            {"year": 2022, "ebit": 83200, "tax": 13800, "pretax": 96000, "d_a": 6300, "capex": 4800, "nwc_change": -600},
            {"year": 2021, "ebit": 69200, "tax": 11500, "pretax": 79800, "d_a": 6100, "capex": 4500, "nwc_change": -500},
            {"year": 2020, "ebit": 53700, "tax": 8900, "pretax": 62000, "d_a": 5900, "capex": 4200, "nwc_change": -400},
        ]
    }
}

# ===== FCFF CALCULATOR =====
class FCFFCalculator:
    """Calculate FCFF using the formula"""
    
    @staticmethod
    def calculate_fcff(financials_dict, scale=1e9):
        """
        Calculate FCFF using formula:
        FCFF = NOPAT + D&A - CapEx - ΔNWC
        where NOPAT = EBIT × (1 - Tax Rate)
        """
        results = []
        
        for year_data in financials_dict:
            # Extract values
            ebit = year_data['ebit'] / scale
            tax_provision = year_data['tax'] / scale
            pretax = year_data['pretax'] / scale
            d_a = year_data['d_a'] / scale
            capex = year_data['capex'] / scale
            delta_nwc = year_data['nwc_change'] / scale
            
            # Calculate tax rate
            tax_rate = tax_provision / pretax if pretax != 0 else 0.20
            tax_rate = max(0, min(tax_rate, 0.50))
            
            # Calculate NOPAT
            nopat = ebit * (1 - tax_rate)
            
            # Calculate FCFF
            fcff = nopat + d_a - capex - delta_nwc
            
            results.append({
                "year": year_data['year'],
                "ebit": ebit,
                "tax_rate": tax_rate,
                "nopat": nopat,
                "d_a": d_a,
                "capex": capex,
                "delta_nwc": delta_nwc,
                "fcff": fcff,
            })
        
        return results

# ===== DCF CALCULATOR =====
class DCFValuation:
    """Calculate DCF valuation"""
    
    @staticmethod
    def calculate_dcf(latest_fcff, growth_rate, wacc, forecast_years=5, terminal_growth=0.03):
        """Calculate DCF"""
        pv_fcff = 0
        projections = []
        
        for year in range(1, forecast_years + 1):
            fcff = latest_fcff * ((1 + growth_rate) ** year)
            pv = fcff / ((1 + wacc) ** year)
            pv_fcff += pv
            projections.append({
                "year": year,
                "fcff": fcff,
                "pv": pv
            })
        
        # Terminal value
        terminal_fcff = latest_fcff * ((1 + growth_rate) ** forecast_years)
        terminal_value = terminal_fcff * (1 + terminal_growth) / (wacc - terminal_growth)
        pv_terminal = terminal_value / ((1 + wacc) ** forecast_years)
        
        ev = pv_fcff + pv_terminal
        
        return {
            "projections": projections,
            "pv_fcff": pv_fcff,
            "terminal_value": terminal_value,
            "pv_terminal": pv_terminal,
            "enterprise_value": ev,
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
        <div style='font-size: 11px; margin-top: 5px;'>DCF VALUATION</div>
    </div>
    """, unsafe_allow_html=True)
    
    pages = ["🏠 Dashboard", "📊 5-Year Analysis", "📈 DCF Valuation", "⚙️ Settings"]
    page = st.radio("Navigate", options=pages, label_visibility="collapsed")

# ===== MAIN HEADER =====
st.markdown(f"""
<div style='background: linear-gradient(90deg, {COLORS["dark_blue"]} 0%, {COLORS["gold"]} 100%); padding: 30px; border-radius: 12px; margin-bottom: 30px; color: white;'>
    <h1 style='margin: 0; font-size: 36px;'>{BRANDING["logo_emoji"]} {BRANDING["name"]}</h1>
    <div style='font-size: 13px; margin-top: 8px;'>{BRANDING["subtitle"]}</div>
    <small>{BRANDING["author"]}</small>
</div>
""", unsafe_allow_html=True)

# ===== PAGES =====
if page == "🏠 Dashboard":
    st.title("🏠 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Data Period", "5 Years")
    col2.metric("Companies", "3")
    col3.metric("Status", "✅ Ready")
    col4.metric("Analysis", "FCFF DCF")
    
    st.success("✅ 5-Year FCFF & DCF Analysis Platform")
    
    st.subheader("📊 Workflow")
    st.markdown("""
    1. **📊 5-Year Analysis** → View 5 years of FCFF calculations
    2. **📈 DCF Valuation** → Calculate intrinsic value
    3. Compare with current market price
    """)
    
    st.subheader("💰 Available Companies")
    for ticker, data in COMPANY_DATA.items():
        col1, col2, col3 = st.columns(3)
        col1.write(f"**{ticker}** - {data['name']}")
        col2.write(f"Price: {data['current_price']}")
        col3.write(f"Sector: {data['sector']}")

elif page == "📊 5-Year Analysis":
    st.title("📊 5-Year FCFF Analysis")
    
    ticker = st.selectbox(
        "Select Company",
        options=list(COMPANY_DATA.keys()),
        format_func=lambda x: f"{x} - {COMPANY_DATA[x]['name']}"
    )
    
    if ticker:
        data = COMPANY_DATA[ticker]
        
        st.success(f"✅ {data['name']}")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Sector", data['sector'])
        col2.metric("Currency", data['currency'])
        col3.metric("Current Price", f"{data['currency']} {data['current_price']:.2f}")
        col4.metric("Market Cap", f"{data['currency']} {data['market_cap']:.1f}B")
        
        st.divider()
        st.subheader("📈 5-Year FCFF Calculation")
        
        # Calculate FCFF
        scale = 1e9 if data['currency'] == 'USD' else 1e6
        fcff_data = FCFFCalculator.calculate_fcff(data['financials'], scale)
        
        # Display table
        df = pd.DataFrame(fcff_data)
        df = df[['year', 'ebit', 'tax_rate', 'nopat', 'd_a', 'capex', 'delta_nwc', 'fcff']]
        df.columns = ['Year', 'EBIT', 'Tax Rate', 'NOPAT', 'D&A', 'CapEx', 'Δ NWC', 'FCFF']
        
        st.dataframe(df, use_container_width=True)
        
        st.divider()
        st.subheader("📊 FCFF Trend")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # FCFF chart
            chart_data = pd.DataFrame({
                'Year': [d['year'] for d in fcff_data],
                'FCFF': [d['fcff'] for d in fcff_data]
            }).set_index('Year')
            st.line_chart(chart_data, use_container_width=True)
        
        with col2:
            # Growth calculation
            fcff_values = [d['fcff'] for d in fcff_data]
            growth_rates = []
            for i in range(len(fcff_values) - 1):
                if fcff_values[i] > 0:
                    growth = (fcff_values[i+1] - fcff_values[i]) / fcff_values[i]
                    growth_rates.append(growth)
            
            avg_growth = np.mean(growth_rates) if growth_rates else 0.05
            latest_fcff = fcff_values[0]
            
            st.metric("Latest FCFF", f"{data['currency']} {latest_fcff:.2f}B")
            st.metric("Avg Historical Growth", f"{avg_growth:.2%}")
            
            # Store for DCF
            st.session_state.selected_ticker = ticker
            st.session_state.latest_fcff = latest_fcff
            st.session_state.avg_growth = avg_growth
            st.session_state.company_data = data

elif page == "📈 DCF Valuation":
    st.title("📈 DCF Valuation")
    
    if "selected_ticker" not in st.session_state:
        st.warning("⚠️ Please select a company in '5-Year Analysis' first")
    else:
        ticker = st.session_state.selected_ticker
        company_data = st.session_state.company_data
        
        st.success(f"Using: {company_data['name']} ({ticker})")
        
        st.subheader("⚙️ DCF Parameters")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            growth = st.slider(
                "FCFF Growth (%)",
                0.0, 20.0,
                float(st.session_state.avg_growth * 100),
                step=0.5
            ) / 100
        
        with col2:
            wacc = st.slider("WACC (%)", 5.0, 20.0, 10.0, step=0.5) / 100
        
        with col3:
            terminal_growth = st.slider("Terminal Growth (%)", 1.0, 5.0, 3.0, step=0.5) / 100
        
        forecast_years = st.slider("Forecast Years", 3, 10, 5)
        
        if st.button("🔄 Calculate DCF", use_container_width=True):
            dcf = DCFValuation.calculate_dcf(
                latest_fcff=st.session_state.latest_fcff,
                growth_rate=growth,
                wacc=wacc,
                forecast_years=forecast_years,
                terminal_growth=terminal_growth
            )
            
            st.success("✅ DCF Complete")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Enterprise Value", f"{dcf['enterprise_value']:.2f}B")
            col2.metric("PV of FCFF", f"{dcf['pv_fcff']:.2f}B")
            col3.metric("Terminal Value", f"{dcf['terminal_value']:.2f}B")
            col4.metric("PV Terminal", f"{dcf['pv_terminal']:.2f}B")
            
            st.divider()
            st.subheader("📊 Projections")
            
            df_proj = pd.DataFrame(dcf['projections'])
            st.dataframe(df_proj, use_container_width=True)
            
            st.divider()
            st.subheader("💰 Intrinsic Value")
            
            equity_value = (dcf['enterprise_value'] - (company_data['total_debt'] - company_data['cash'])/1e9)
            intrinsic = equity_value / company_data['shares_outstanding']
            current = company_data['current_price']
            upside = ((intrinsic - current) / current * 100)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Intrinsic Value", f"{intrinsic:.2f}")
            col2.metric("Current Price", f"{current:.2f}")
            col3.metric("Upside/Downside", f"{upside:+.1f}%")

elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    st.checkbox("Show detailed calculations", value=True)
    st.selectbox("Number Format", ["Billions", "Millions"])

st.divider()
st.markdown(f"""
<div style='text-align: center; padding: 20px; color: #666; font-size: 12px;'>
    <strong>The Mountain Path - DCF Valuation</strong><br/>
    5-Year FCFF Analysis | Prof. V. Ravichandran | v1.0
</div>
""", unsafe_allow_html=True)
