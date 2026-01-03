"""
DCF Analysis Page
Perform professional discounted cash flow valuation
Prof. V. Ravichandran - The Mountain Path - World of Finance
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

sys.path.insert(0, str(Path(__file__).parent.parent))

from streamlit_app.components import ComponentLibrary
from streamlit_app.config import DEFAULTS, VALIDATION
from database.schema import FinancialDatabaseSchema
from valuation.fcff import FCFFCalculator
from valuation.dcf import DCFValuationEngine

def render():
    """Render DCF analysis page"""
    
    ComponentLibrary.page_header(
        "DCF Valuation Analysis",
        ["Home", "Analysis", "DCF Valuation"]
    )
    
    st.markdown("""
    **Professional DCF Valuation Engine**
    
    This page implements a complete Discounted Cash Flow valuation methodology:
    1. Extract historical FCFF from validated financial data
    2. Analyze growth trends
    3. Project future FCFF (explicit period)
    4. Calculate Terminal Value using perpetuity growth
    5. Discount to present value using WACC
    6. Calculate Enterprise and Equity Value
    """)
    
    # Get database connection
    conn = FinancialDatabaseSchema.get_connection()
    cursor = conn.cursor()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["New Valuation", "Saved Valuations", "Historical Analysis"])
    
    # ===== TAB 1: New Valuation =====
    with tab1:
        st.subheader("Create New DCF Valuation")
        
        # Step 1: Select Company
        st.markdown("### Step 1: Select Company")
        
        cursor.execute("""
            SELECT DISTINCT c.id, c.ticker, c.company_name
            FROM companies c
            JOIN financial_periods fp ON c.id = fp.company_id
            WHERE fp.filing_type = '10-K'
            ORDER BY c.ticker
        """)
        
        companies = cursor.fetchall()
        
        if not companies:
            ComponentLibrary.alert(
                "No companies with 10-K data available. Load data first.",
                alert_type="warning"
            )
            return
        
        company_options = [f"{c[1]} - {c[2]}" for c in companies]
        company_map = {opt: c[0] for opt, c in zip(company_options, companies)}
        
        selected_company = st.selectbox("Select Company", options=company_options)
        company_id = company_map[selected_company]
        
        # Step 2: Select Base Period
        st.markdown("### Step 2: Select Base Period")
        
        cursor.execute("""
            SELECT id, fiscal_year, period_end_date
            FROM financial_periods
            WHERE company_id = ? AND filing_type = '10-K'
            ORDER BY fiscal_year DESC
        """, (company_id,))
        
        periods = cursor.fetchall()
        
        if not periods:
            ComponentLibrary.alert("No 10-K periods available for selected company", alert_type="warning")
            return
        
        period_options = [f"FY{p[1]} (ending {p[2]})" for p in periods]
        period_map = {opt: p[0] for opt, p in zip(period_options, periods)}
        
        selected_period = st.selectbox("Base Year", options=period_options)
        base_period_id = period_map[selected_period]
        
        st.divider()
        
        # Step 3: Valuation Assumptions
        st.markdown("### Step 3: Valuation Assumptions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            wacc = st.slider(
                "WACC (Weighted Average Cost of Capital)",
                min_value=float(VALIDATION["min_wacc"]),
                max_value=float(VALIDATION["max_wacc"]),
                value=DEFAULTS["wacc"],
                step=0.005,
                format="%.1%%",
                help="Required rate of return for discounting cash flows"
            )
            
            terminal_gr = st.slider(
                "Terminal Growth Rate",
                min_value=float(VALIDATION["min_terminal_gr"]),
                max_value=float(VALIDATION["max_terminal_gr"]),
                value=DEFAULTS["terminal_growth_rate"],
                step=0.001,
                format="%.2%%",
                help="Long-term perpetual growth rate (typically GDP growth)"
            )
        
        with col2:
            projection_years = st.slider(
                "Projection Period",
                min_value=3,
                max_value=10,
                value=DEFAULTS["projection_years"],
                step=1,
                help="Number of years for explicit forecast period"
            )
            
            # Validation
            if wacc <= terminal_gr:
                ComponentLibrary.alert(
                    "WACC must be greater than Terminal Growth Rate",
                    alert_type="danger"
                )
                return
        
        # Advanced options
        with st.expander("Advanced Options"):
            col1, col2 = st.columns(2)
            
            with col1:
                growth_assumption = st.radio(
                    "Growth Rate Assumption",
                    ["Historical CAGR", "Manual Input", "Declining Growth"]
                )
            
            with col2:
                if growth_assumption == "Manual Input":
                    manual_growth = st.number_input(
                        "Annual Growth Rate (%)",
                        value=5.0,
                        min_value=-10.0,
                        max_value=30.0,
                        step=0.5
                    ) / 100
        
        st.divider()
        
        # Calculate Valuation
        col1, col2 = st.columns([1, 1])
        
        with col1:
            calc_button = st.button(
                "🧮 Calculate Valuation",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            reset_button = st.button(
                "↻ Reset Form",
                use_container_width=True
            )
        
        if reset_button:
            st.rerun()
        
        # Perform valuation
        if calc_button:
            with st.spinner("Calculating DCF valuation..."):
                try:
                    # Initialize calculators
                    fcff_calc = FCFFCalculator(conn)
                    dcf_engine = DCFValuationEngine(conn)
                    
                    # Get historical FCFF
                    historical_fcff = fcff_calc.calculate_historical_fcff(company_id, years=5)
                    
                    if not historical_fcff:
                        ComponentLibrary.alert("Insufficient data for valuation", alert_type="warning")
                        return
                    
                    # Get growth rate
                    if growth_assumption == "Historical CAGR":
                        growth_analysis = fcff_calc.calculate_fcff_growth_rate(historical_fcff)
                        growth_rate = growth_analysis["growth_rate"]
                    else:
                        growth_rate = manual_growth if 'manual_growth' in locals() else 0.05
                    
                    # Get base FCFF
                    base_fcff = historical_fcff[-1]["fcff"]
                    
                    # Project FCFF
                    if growth_assumption == "Declining Growth":
                        # Declining growth model: start high, decline to terminal rate
                        growth_rates = [
                            growth_rate * (1 - (i / projection_years))
                            for i in range(projection_years)
                        ]
                    else:
                        growth_rates = [growth_rate] * projection_years
                    
                    fcff_projections = fcff_calc.project_fcff(
                        base_fcff,
                        growth_rates,
                        years=projection_years
                    )
                    
                    # Perform DCF valuation
                    valuation_results = dcf_engine.perform_dcf_valuation(
                        company_id=company_id,
                        base_period_id=base_period_id,
                        fcff_projections=fcff_projections,
                        wacc=wacc,
                        terminal_growth_rate=terminal_gr
                    )
                    
                    # Save results
                    dcf_calc_id = dcf_engine.save_dcf_results(valuation_results)
                    
                    # Display results
                    st.divider()
                    st.success("✓ Valuation completed successfully")
                    
                    # Key valuation metrics
                    st.markdown("### Valuation Results")
                    
                    metrics = [
                        {
                            "label": "Intrinsic Value per Share",
                            "value": valuation_results["intrinsic_value_per_share"],
                            "unit": "$",
                            "type": "success"
                        },
                        {
                            "label": "Enterprise Value",
                            "value": valuation_results["enterprise_value"],
                            "unit": "$",
                            "type": "info"
                        },
                        {
                            "label": "Equity Value",
                            "value": valuation_results["equity_value"],
                            "unit": "$",
                            "type": "info"
                        }
                    ]
                    
                    cols = st.columns(len(metrics))
                    for col, metric in zip(cols, metrics):
                        with col:
                            ComponentLibrary.metric_card(
                                metric["label"],
                                metric["value"],
                                unit=metric["unit"],
                                card_type=metric["type"]
                            )
                    
                    st.divider()
                    
                    # Valuation bridge
                    st.markdown("### Valuation Bridge")
                    
                    bridge_data = {
                        "Component": [
                            "PV(Explicit FCFF)",
                            "PV(Terminal Value)",
                            "Enterprise Value",
                            "Less: Net Debt",
                            "Equity Value",
                            "÷ Shares Outstanding",
                            "= Intrinsic Value/Share"
                        ],
                        "Value ($M)": [
                            valuation_results["pv_explicit_fcff"] / 1e6,
                            valuation_results["pv_terminal_value"] / 1e6,
                            valuation_results["enterprise_value"] / 1e6,
                            -valuation_results["net_debt"] / 1e6,
                            valuation_results["equity_value"] / 1e6,
                            valuation_results["shares_outstanding"] / 1e6,
                            valuation_results["intrinsic_value_per_share"]
                        ]
                    }
                    
                    df_bridge = pd.DataFrame(bridge_data)
                    st.dataframe(df_bridge, use_container_width=True)
                    
                    st.divider()
                    
                    # FCFF projections
                    st.markdown("### FCFF Projections")
                    
                    projection_data = {
                        "Year": list(range(1, projection_years + 1)),
                        "Growth Rate": [f"{g*100:.1f}%" for g in growth_rates],
                        "FCFF ($M)": [f/1e6 for f in fcff_projections]
                    }
                    
                    df_projections = pd.DataFrame(projection_data)
                    st.dataframe(df_projections, use_container_width=True)
                    
                    # Chart
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=projection_data["Year"],
                        y=projection_data["FCFF ($M)"],
                        name="Projected FCFF",
                        marker_color="#003366"
                    ))
                    fig.update_layout(
                        title="FCFF Projections",
                        xaxis_title="Year",
                        yaxis_title="FCFF ($M)",
                        hovermode="x unified",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Save to session state
                    st.session_state.last_valuation = valuation_results
                    st.session_state.last_dcf_id = dcf_calc_id
                    
                except Exception as e:
                    ComponentLibrary.alert(f"Error during valuation: {str(e)}", alert_type="danger")
    
    # ===== TAB 2: Saved Valuations =====
    with tab2:
        st.subheader("Saved Valuations")
        
        cursor.execute("""
            SELECT 
                dc.id, c.ticker, fp.fiscal_year,
                dc.price_per_share, dc.enterprise_value,
                dc.wacc, dc.terminal_growth_rate,
                dc.calculation_date
            FROM dcf_calculations dc
            JOIN companies c ON dc.company_id = c.id
            JOIN financial_periods fp ON dc.base_year_id = fp.id
            ORDER BY dc.calculation_date DESC
            LIMIT 20
        """)
        
        valuations = cursor.fetchall()
        
        if valuations:
            df_valuations = pd.DataFrame(
                valuations,
                columns=["ID", "Ticker", "Base FY", "Price/Share", "Enterprise Value", 
                        "WACC", "Terminal GR", "Date"]
            )
            
            # Format columns
            df_valuations["Price/Share"] = df_valuations["Price/Share"].apply(lambda x: f"${x:.2f}")
            df_valuations["Enterprise Value"] = (df_valuations["Enterprise Value"] / 1e9).apply(lambda x: f"${x:.1f}B")
            df_valuations["WACC"] = (df_valuations["WACC"] * 100).apply(lambda x: f"{x:.1f}%")
            df_valuations["Terminal GR"] = (df_valuations["Terminal GR"] * 100).apply(lambda x: f"{x:.2f}%")
            
            st.dataframe(df_valuations, use_container_width=True)
        else:
            ComponentLibrary.alert("No saved valuations yet", alert_type="info")
    
    # ===== TAB 3: Historical Analysis =====
    with tab3:
        st.subheader("Historical FCFF Analysis")
        
        cursor.execute("""
            SELECT DISTINCT c.id, c.ticker
            FROM companies c
            JOIN financial_periods fp ON c.id = fp.company_id
            ORDER BY c.ticker
        """)
        
        companies = cursor.fetchall()
        
        if companies:
            ticker_options = [c[1] for c in companies]
            ticker_map = {opt: c[0] for opt, c in zip(ticker_options, companies)}
            
            selected_ticker = st.selectbox("Select Company", options=ticker_options)
            company_id = ticker_map[selected_ticker]
            
            fcff_calc = FCFFCalculator(conn)
            historical = fcff_calc.calculate_historical_fcff(company_id, years=5)
            
            if historical:
                df_historical = pd.DataFrame(historical)
                
                # Display table
                display_cols = ["fiscal_year", "revenue", "ebit", "tax_rate", "nopat", "da", "capex", "fcff"]
                df_display = df_historical[display_cols].copy()
                df_display.columns = ["FY", "Revenue", "EBIT", "Tax Rate", "NOPAT", "D&A", "CapEx", "FCFF"]
                
                st.subheader("Historical FCFF Components")
                ComponentLibrary.financial_table(df_display, format_columns={
                    "Revenue": "currency",
                    "EBIT": "currency",
                    "Tax Rate": "percent",
                    "NOPAT": "currency",
                    "D&A": "currency",
                    "CapEx": "currency",
                    "FCFF": "currency"
                })
                
                # Growth analysis
                growth_analysis = fcff_calc.calculate_fcff_growth_rate(historical)
                
                st.subheader("Growth Analysis")
                ComponentLibrary.metric_card(
                    "Implied CAGR",
                    f"{growth_analysis['growth_rate']*100:.2f}%",
                    card_type="info"
                )
                
                # Chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df_display["FY"],
                    y=df_display["FCFF"],
                    mode="lines+markers",
                    name="FCFF",
                    line=dict(color="#003366", width=2),
                    marker=dict(size=8)
                ))
                fig.update_layout(
                    title="Historical FCFF Trend",
                    xaxis_title="Fiscal Year",
                    yaxis_title="FCFF",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
    
    conn.close()

if __name__ == "__main__":
    render()
