
"""
DCF Valuation Platform - 5-Year Historical FCFF Analysis
The Mountain Path - World of Finance
Prof. V. Ravichandran
Analyzes 5 years of financial data and calculates DCF
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# ===== CONFIG =====
BRANDING = {
    "logo_emoji": "🏔️",
    "name": "The Mountain Path - DCF Valuation",
    "subtitle": "5-Year Financial Analysis & DCF Valuation",
    "author": "Prof. V. Ravichandran",
}

COLORS = {
    "dark_blue": "#003366",
    "light_blue": "#ADD8E6",
    "gold": "#FFD700",
}

# ===== FCFF CALCULATOR FOR 5 YEARS =====
class HistoricalFCFFCalculator:
    """Calculate FCFF for past 5 years"""
    
    @staticmethod
    def calculate_5year_fcff(ticker):
        """Get 5 years of FCFF data"""
        try:
            ticker = ticker.upper().strip()
            stock = yf.Ticker(ticker)
            
            # Get financial statements (last 5 years)
            income_stmt = stock.income_stmt
            cash_flow = stock.cashflow
            balance_sheet = stock.balance_sheet
            
            if income_stmt.empty or cash_flow.empty:
                return {"error": f"No financial data found for {ticker}"}
            
            # Get last 5 years
            years = income_stmt.columns[:5]
            
            B = 1e9  # Billions scaling
            fcff_data = []
            
            for year in years:
                try:
                    # 1. EBIT
                    ebit = income_stmt.loc['EBIT', year] / B if 'EBIT' in income_stmt.index else 0
                    
                    # 2. Tax Rate
                    pretax_income = income_stmt.loc['Pretax Income', year] if 'Pretax Income' in income_stmt.index else 1
                    tax_provision = income_stmt.loc['Tax Provision', year] if 'Tax Provision' in income_stmt.index else 0
                    tax_rate = (tax_provision / pretax_income) if (pretax_income > 0) else 0.30
                    tax_rate = max(0, min(tax_rate, 0.50))  # Clamp between 0-50%
                    
                    # 3. NOPAT
                    nopat = ebit * (1 - tax_rate)
                    
                    # 4. D&A
                    d_a = cash_flow.loc['Depreciation And Amortization', year] / B if 'Depreciation And Amortization' in cash_flow.index else 0
                    
                    # 5. CapEx
                    capex = -cash_flow.loc['Capital Expenditure', year] / B if 'Capital Expenditure' in cash_flow.index else 0
                    
                    # 6. Change in NWC
                    delta_nwc = cash_flow.loc['Change In Working Capital', year] / B if 'Change In Working Capital' in cash_flow.index else 0
                    
                    # 7. FCFF
                    fcff = nopat + d_a - capex - delta_nwc
                    
                    fcff_data.append({
                        "year": year.year,
                        "ebit": ebit,
                        "tax_rate": tax_rate,
                        "nopat": nopat,
                        "d_a": d_a,
                        "capex": capex,
                        "delta_nwc": delta_nwc,
                        "fcff": fcff,
                    })
                
                except Exception as e:
                    continue
            
            if not fcff_data:
                return {"error": "Could not extract financial data"}
            
            # Calculate metrics
            fcff_values = [d['fcff'] for d in fcff_data]
            fcff_growth_rates = []
            for i in range(len(fcff_values) - 1):
                if fcff_values[i+1] > 0 and fcff_values[i] > 0:
                    growth = (fcff_values[i+1] - fcff_values[i]) / fcff_values[i]
                    fcff_growth_rates.append(growth)
            
            avg_growth = np.mean(fcff_growth_rates) if fcff_growth_rates else 0.05
            latest_fcff = fcff_values[0] if fcff_values else 0
            
            # Get company info
            info = stock.info
            
            return {
                "success": True,
                "ticker": ticker,
                "company_name": info.get("longName", "Unknown"),
                "currency": info.get("currency", "USD"),
                "sector": info.get("sector", "Unknown"),
                "fcff_data": fcff_data,
                "latest_fcff": latest_fcff,
                "avg_growth_rate": avg_growth,
                "current_price": info.get("currentPrice", 0),
                "shares_outstanding": info.get("sharesOutstanding", 0),
                "market_cap": info.get("marketCap", 0),
                "total_debt": info.get("totalDebt", 0),
                "cash": info.get("totalCash", 0),
                "fetch_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        
        except Exception as e:
            return {"error": str(e)}

# ===== DCF CALCULATOR =====
class DCFValuation:
    """Calculate DCF valuation"""
    
    @staticmethod
    def calculate_dcf(fcff, growth_rate, wacc, forecast_years=5, terminal_growth=0.03):
        """Calculate DCF valuation"""
        pv_fcff = 0
        fcff_projections = []
        
        # Project FCFFs
        for year in range(1, forecast_years + 1):
            fcff_year = fcff * ((1 + growth_rate) ** year)
            pv = fcff_year / ((1 + wacc) ** year)
            pv_fcff += pv
            fcff_projections.append({
                "year": year,
                "fcff": fcff_year,
                "pv": pv
            })
        
        # Terminal value
        terminal_fcff = fcff * ((1 + growth_rate) ** forecast_years)
        terminal_value = terminal_fcff * (1 + terminal_growth) / (wacc - terminal_growth)
        pv_terminal = terminal_value / ((1 + wacc) ** forecast_years)
        
        # Enterprise value
        enterprise_value = pv_fcff + pv_terminal
        
        return {
            "fcff_projections": fcff_projections,
            "pv_fcff": pv_fcff,
            "terminal_value": terminal_value,
            "pv_terminal": pv_terminal,
            "enterprise_value": enterprise_value,
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
    col2.metric("Data Source", "Yahoo Finance")
    col3.metric("Analysis", "FCFF-Based")
    col4.metric("Status", "✅ Ready")
    
    st.success("✅ 5-Year Financial Analysis & DCF Platform Ready")
    
    st.subheader("📊 How It Works")
    st.markdown("""
    1. **Fetch Data** → Get 5 years of financial statements from Yahoo Finance
    2. **Calculate FCFF** → Free Cash Flow to Firm for each year
    3. **Analyze Trends** → Historical growth rates and patterns
    4. **DCF Valuation** → Project future cash flows and calculate enterprise value
    5. **Intrinsic Value** → Per share valuation based on fundamentals
    """)

elif page == "📊 5-Year Analysis":
    st.title("📊 5-Year Financial Analysis")
    st.write("Analyze 5 years of FCFF and financial metrics")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ticker = st.text_input(
            "Enter Stock Ticker",
            value="RELIANCE.NS",
            placeholder="e.g., RELIANCE.NS, AAPL, MSFT, TCS.NS"
        ).upper().strip()
    
    with col2:
        analyze_button = st.button("📊 Analyze 5Y", use_container_width=True)
    
    if analyze_button and ticker:
        with st.spinner(f"📡 Fetching 5 years of financial data for {ticker}..."):
            result = HistoricalFCFFCalculator.calculate_5year_fcff(ticker)
            
            if "error" in result:
                st.error(f"❌ Error: {result['error']}")
            else:
                data = result
                st.success(f"✅ Analyzed: {data['company_name']}")
                
                col1, col2, col3, col4 = st.columns(4)
                col1.write(f"**Ticker:** {ticker}")
                col2.write(f"**Sector:** {data['sector']}")
                col3.write(f"**Latest FCFF:** ₹{data['latest_fcff']:.2f}B")
                col4.write(f"**Avg Growth:** {data['avg_growth_rate']:.2%}")
                
                st.divider()
                st.subheader("📈 5-Year FCFF Trend")
                
                # Create DataFrame for display
                df_display = pd.DataFrame(data['fcff_data'])
                df_display = df_display[['year', 'ebit', 'tax_rate', 'nopat', 'd_a', 'capex', 'delta_nwc', 'fcff']]
                df_display.columns = ['Year', 'EBIT', 'Tax Rate', 'NOPAT', 'D&A', 'CapEx', 'Δ NWC', 'FCFF']
                
                st.dataframe(df_display, use_container_width=True)
                
                st.divider()
                st.subheader("📊 FCFF Components Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # FCFF trend
                    fcff_values = [d['fcff'] for d in data['fcff_data']]
                    years = [d['year'] for d in data['fcff_data']]
                    
                    st.line_chart(
                        pd.DataFrame({
                            'Year': years,
                            'FCFF': fcff_values
                        }).set_index('Year'),
                        use_container_width=True
                    )
                
                with col2:
                    # Components breakdown
                    latest = data['fcff_data'][0]
                    components = {
                        'NOPAT': latest['nopat'],
                        'D&A': latest['d_a'],
                        'CapEx': -latest['capex'],
                        'Δ NWC': -latest['delta_nwc']
                    }
                    
                    st.bar_chart(
                        pd.DataFrame({
                            'Component': list(components.keys()),
                            'Value': list(components.values())
                        }).set_index('Component'),
                        use_container_width=True
                    )
                
                # Store in session
                st.session_state.analysis_data = data

elif page == "📈 DCF Valuation":
    st.title("📈 DCF Valuation")
    
    if "analysis_data" not in st.session_state:
        st.warning("⚠️ Please run '5-Year Analysis' first")
    else:
        data = st.session_state.analysis_data
        
        st.success(f"Using data for: {data['company_name']}")
        
        st.subheader("⚙️ DCF Parameters")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            growth_rate = st.slider(
                "FCFF Growth Rate (%)",
                0.0,
                20.0,
                float(data['avg_growth_rate'] * 100),
                step=0.5
            ) / 100
            st.caption(f"Historical avg: {data['avg_growth_rate']:.2%}")
        
        with col2:
            wacc = st.slider(
                "WACC (%)",
                5.0,
                20.0,
                10.0,
                step=0.5
            ) / 100
        
        with col3:
            terminal_growth = st.slider(
                "Terminal Growth (%)",
                1.0,
                5.0,
                3.0,
                step=0.5
            ) / 100
        
        forecast_years = st.slider("Forecast Period (years)", 3, 10, 5)
        
        if st.button("🔄 Calculate DCF Valuation", use_container_width=True):
            # Calculate DCF
            dcf_result = DCFValuation.calculate_dcf(
                fcff=data['latest_fcff'],
                growth_rate=growth_rate,
                wacc=wacc,
                forecast_years=forecast_years,
                terminal_growth=terminal_growth
            )
            
            st.success("✅ DCF Valuation Complete")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(
                "Enterprise Value",
                f"₹{dcf_result['enterprise_value']:.2f}B"
            )
            col2.metric(
                "PV of FCFF",
                f"₹{dcf_result['pv_fcff']:.2f}B"
            )
            col3.metric(
                "PV Terminal Value",
                f"₹{dcf_result['pv_terminal']:.2f}B"
            )
            col4.metric(
                "Terminal Value",
                f"₹{dcf_result['terminal_value']:.2f}B"
            )
            
            st.divider()
            st.subheader("📊 FCFF Projections")
            
            df_projections = pd.DataFrame(dcf_result['fcff_projections'])
            st.dataframe(df_projections, use_container_width=True)
            
            st.divider()
            st.subheader("💰 Intrinsic Value Calculation")
            
            if data['shares_outstanding'] > 0:
                equity_value = (dcf_result['enterprise_value'] * 1e9) - (data['total_debt'] or 0) + (data['cash'] or 0)
                shares = data['shares_outstanding']
                intrinsic_value = equity_value / shares
                current_price = data['current_price']
                upside = ((intrinsic_value - current_price) / current_price * 100) if current_price > 0 else 0
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Intrinsic Value/Share", f"₹{intrinsic_value:.2f}")
                col2.metric("Current Price", f"₹{current_price:.2f}")
                col3.metric("Upside/Downside", f"{upside:+.1f}%")
                
                st.divider()
                st.subheader("📋 Valuation Summary")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"""
                    **Enterprise Value:** ₹{dcf_result['enterprise_value']:.2f}B
                    **Less: Net Debt:** ₹{(data['total_debt'] - data['cash'])/1e9 if data['total_debt'] else 0:.2f}B
                    **Equity Value:** ₹{equity_value/1e9:.2f}B
                    **Shares Outstanding:** {shares:.2f}B
                    """)
                
                with col2:
                    st.write(f"""
                    **Intrinsic Value/Share:** ₹{intrinsic_value:.2f}
                    **Current Market Price:** ₹{current_price:.2f}
                    **Margin of Safety:** {upside:+.1f}%
                    """)

elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    
    st.subheader("Display Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        st.selectbox("Currency Display", ["INR (₹)", "USD ($)", "EUR (€)"])
        st.checkbox("Show detailed calculations", value=True)
    
    with col2:
        st.selectbox("Number Format", ["Billions", "Millions"])
        st.checkbox("Auto-calculate on input", value=True)

st.divider()
st.markdown(f"""
<div style='text-align: center; padding: 20px; color: #666; font-size: 12px;'>
    <strong>The Mountain Path - DCF Valuation</strong><br/>
    5-Year FCFF Analysis | Prof. V. Ravichandran | v1.0
</div>
""", unsafe_allow_html=True)
