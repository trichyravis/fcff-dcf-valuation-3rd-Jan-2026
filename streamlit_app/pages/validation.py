"""
Data Validation Page
Financial statement tie-outs and quality checks
Prof. V. Ravichandran - The Mountain Path - World of Finance
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from streamlit_app.components import ComponentLibrary
from database.schema import FinancialDatabaseSchema
from validation.validator import FinancialValidator

def render():
    """Render validation page"""
    
    ComponentLibrary.page_header(
        "Data Validation",
        ["Home", "Data Management", "Validation"]
    )
    
    st.markdown("""
    **Professional Data Validation & Tie-Out Engine**
    
    This page performs comprehensive validation checks on financial statement data before
    it's used for valuation calculations. This is critical for ensuring data integrity.
    
    **Validation Checks:**
    - ✓ Balance Sheet Equality (Assets = Liabilities + Equity)
    - ✓ Income Statement Reconciliation
    - ✓ Operating Cash Flow Reasonableness
    - ✓ Free Cash Flow Components
    - ✓ Depreciation & Amortization Presence
    """)
    
    # Get database connection
    conn = FinancialDatabaseSchema.get_connection()
    cursor = conn.cursor()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Run Validation", "Validation History", "Data Review"])
    
    # ===== TAB 1: Run Validation =====
    with tab1:
        st.subheader("Run Financial Data Validation")
        
        # Get available periods
        cursor.execute("""
            SELECT fp.id, c.ticker, fp.fiscal_year, fp.period_end_date
            FROM financial_periods fp
            JOIN companies c ON fp.company_id = c.id
            ORDER BY c.ticker, fp.fiscal_year DESC
        """)
        
        periods = cursor.fetchall()
        
        if not periods:
            ComponentLibrary.alert(
                "No financial periods available. Load company data first.",
                alert_type="warning"
            )
        else:
            # Create period selector
            period_options = [
                f"{p[1]} - FY{p[2]} (ending {p[3]})" 
                for p in periods
            ]
            period_map = {opt: p[0] for opt, p in zip(period_options, periods)}
            
            selected_period = st.selectbox(
                "Select Period to Validate",
                options=period_options
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                validate_button = st.button(
                    "▶️ Run Validation",
                    use_container_width=True,
                    type="primary"
                )
            
            with col2:
                validate_all = st.button(
                    "▶️ Validate All Periods",
                    use_container_width=True
                )
            
            # Run validation
            if validate_button:
                period_id = period_map[selected_period]
                
                with st.spinner("Running validation checks..."):
                    validator = FinancialValidator(conn)
                    results = validator.run_all_validations(period_id)
                
                # Display results
                st.divider()
                
                # Summary metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    ComponentLibrary.metric_card(
                        "Checks Passed",
                        results["passed"],
                        card_type="success"
                    )
                
                with col2:
                    ComponentLibrary.metric_card(
                        "Checks Failed",
                        results["failed"],
                        card_type=("danger" if results["failed"] > 0 else "success")
                    )
                
                with col3:
                    quality = results["quality_score"] * 100
                    card_type = "success" if quality >= 90 else ("warning" if quality >= 70 else "danger")
                    ComponentLibrary.metric_card(
                        "Quality Score",
                        f"{quality:.1f}%",
                        card_type=card_type
                    )
                
                st.divider()
                
                # Detailed results
                st.subheader("Validation Details")
                
                for check_name, result in results["details"].items():
                    with st.expander(f"✓ {result.get('check_name', check_name)}", expanded=True):
                        
                        # Key metrics
                        cols = st.columns(2)
                        
                        if result.get("variance") is not None:
                            with cols[0]:
                                st.metric("Variance", f"${result['variance']:,.0f}")
                            with cols[1]:
                                st.metric("Variance %", f"{result.get('variance_pct', 0):.2f}%")
                        
                        # Details
                        if result.get("note"):
                            ComponentLibrary.alert(result["note"], alert_type="info")
                        
                        if result.get("warning"):
                            ComponentLibrary.alert(result["warning"], alert_type="warning")
                        
                        # Display all available metrics
                        metrics_to_show = {k: v for k, v in result.items() 
                                         if k not in ['check_name', 'passed', 'note', 'warning', 'expected', 'actual', 'variance', 'variance_pct']}
                        
                        if metrics_to_show:
                            for key, value in metrics_to_show.items():
                                if isinstance(value, (int, float)):
                                    st.write(f"**{key.replace('_', ' ').title()}:** {value:,.0f}")
                                elif isinstance(value, (list, tuple)):
                                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
            
            # Validate all periods
            if validate_all:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                validator = FinancialValidator(conn)
                all_results = []
                
                for idx, period in enumerate(periods):
                    period_id = period[0]
                    ticker = period[1]
                    fy = period[2]
                    
                    status_text.text(f"Validating {ticker} FY{fy}...")
                    results = validator.run_all_validations(period_id)
                    all_results.append({
                        "ticker": ticker,
                        "fiscal_year": fy,
                        "passed": results["passed"],
                        "failed": results["failed"],
                        "quality": results["quality_score"]
                    })
                    
                    progress = (idx + 1) / len(periods)
                    progress_bar.progress(progress)
                
                progress_bar.progress(1.0)
                status_text.text("✓ All periods validated")
                
                # Summary table
                st.divider()
                st.subheader("Validation Summary")
                
                df_summary = pd.DataFrame(all_results)
                df_summary["Quality %"] = (df_summary["quality"] * 100).round(1)
                df_summary = df_summary.drop("quality", axis=1)
                
                ComponentLibrary.financial_table(df_summary)
    
    # ===== TAB 2: Validation History =====
    with tab2:
        st.subheader("Validation History")
        
        cursor.execute("""
            SELECT 
                vl.period_id, c.ticker, fp.fiscal_year,
                vl.check_name, vl.passed,
                vl.variance, vl.variance_pct,
                vl.check_date
            FROM validation_log vl
            JOIN financial_periods fp ON vl.period_id = fp.id
            JOIN companies c ON fp.company_id = c.id
            ORDER BY vl.check_date DESC
            LIMIT 100
        """)
        
        validation_logs = cursor.fetchall()
        
        if validation_logs:
            df_logs = pd.DataFrame(
                validation_logs,
                columns=["Period ID", "Ticker", "FY", "Check", "Passed", "Variance", "Variance %", "Date"]
            )
            
            # Format for display
            df_logs["Status"] = df_logs["Passed"].apply(lambda x: "✓ Pass" if x else "✗ Fail")
            display_df = df_logs[["Ticker", "FY", "Check", "Status", "Variance", "Variance %"]]
            
            ComponentLibrary.financial_table(display_df)
        else:
            ComponentLibrary.alert(
                "No validation history available",
                alert_type="info"
            )
    
    # ===== TAB 3: Data Review =====
    with tab3:
        st.subheader("Financial Data Review")
        
        cursor.execute("""
            SELECT fp.id, c.ticker, fp.fiscal_year, fp.period_end_date
            FROM financial_periods fp
            JOIN companies c ON fp.company_id = c.id
            ORDER BY c.ticker, fp.fiscal_year DESC
        """)
        
        periods = cursor.fetchall()
        
        if periods:
            period_options = [
                f"{p[1]} - FY{p[2]}" 
                for p in periods
            ]
            period_map = {opt: p[0] for opt, p in zip(period_options, periods)}
            
            selected_period = st.selectbox(
                "Select Period to Review",
                options=period_options,
                key="data_review"
            )
            
            period_id = period_map[selected_period]
            
            # Get financial data
            cursor.execute("""
                SELECT line_item, xbrl_tag, value FROM income_statement
                WHERE period_id = ? ORDER BY line_item
            """, (period_id,))
            
            income_data = cursor.fetchall()
            
            cursor.execute("""
                SELECT line_item, xbrl_tag, value FROM balance_sheet
                WHERE period_id = ? ORDER BY line_item
            """, (period_id,))
            
            bs_data = cursor.fetchall()
            
            cursor.execute("""
                SELECT line_item, xbrl_tag, value FROM cash_flow_statement
                WHERE period_id = ? ORDER BY line_item
            """, (period_id,))
            
            cf_data = cursor.fetchall()
            
            # Display data
            tab_is, tab_bs, tab_cf = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow"])
            
            with tab_is:
                if income_data:
                    df_is = pd.DataFrame(
                        income_data,
                        columns=["Line Item", "XBRL Tag", "Value"]
                    )
                    ComponentLibrary.financial_table(
                        df_is,
                        format_columns={"Value": "currency"}
                    )
                else:
                    st.info("No income statement data available")
            
            with tab_bs:
                if bs_data:
                    df_bs = pd.DataFrame(
                        bs_data,
                        columns=["Line Item", "XBRL Tag", "Value"]
                    )
                    ComponentLibrary.financial_table(
                        df_bs,
                        format_columns={"Value": "currency"}
                    )
                else:
                    st.info("No balance sheet data available")
            
            with tab_cf:
                if cf_data:
                    df_cf = pd.DataFrame(
                        cf_data,
                        columns=["Line Item", "XBRL Tag", "Value"]
                    )
                    ComponentLibrary.financial_table(
                        df_cf,
                        format_columns={"Value": "currency"}
                    )
                else:
                    st.info("No cash flow data available")
        else:
            ComponentLibrary.alert(
                "No financial data available",
                alert_type="info"
            )
    
    conn.close()

if __name__ == "__main__":
    render()
