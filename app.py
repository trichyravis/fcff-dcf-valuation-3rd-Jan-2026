
import streamlit as st

from core.sec_data import (
    get_cik_from_ticker,
    get_company_xbrl,
    extract_series
)
from core.statements import (
    build_income_statement,
    build_cashflow_statement,
    build_balance_sheet
)
from core.validate import validate_for_fcff
from core.fcff import compute_fcff
from core.wacc import calculate_wacc
from core.equity import get_share_count
from core.net_debt import get_net_debt
from core.dcf import equity_value_from_fcff
from core.monte_carlo import monte_carlo_dcf

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="10-K Based Valuation Platform",
    layout="wide"
)

st.title("📊 10-K Based Valuation Platform")

st.info(
    "ℹ️ **Professional Workflow**: This platform first downloads and displays "
    "official SEC 10-K data, then validates feasibility, computes FCFF "
    "(latest year only), and finally performs valuation. "
    "10-K filings typically allow computation of **only one FCFF year**."
)

# -------------------------------------------------
# USER INPUT
# -------------------------------------------------
ticker = st.text_input("Enter US Ticker", "AAPL")

# -------------------------------------------------
# MAIN ACTION
# -------------------------------------------------
if st.button("Load 10-K Data"):

    try:
        # ---------------------------------------------
        # DOWNLOAD SEC DATA
        # ---------------------------------------------
        cik = get_cik_from_ticker(ticker)
        xbrl = get_company_xbrl(cik)

        # ---------------------------------------------
        # UI TABS
        # ---------------------------------------------
        tabs = st.tabs([
            "📥 Downloaded 10-K Data",
            "📄 Financial Statements",
            "🧠 Validation & Assumptions",
            "📘 FCFF",
            "📈 Valuation"
        ])

        # ---------------------------------------------
        # TAB 1 — METADATA
        # ---------------------------------------------
      with tabs[1]:
        st.subheader("📄 Income Statement (10-K)")
        income = build_income_statement(xbrl, extract_series)
        for name, df in income.items():
            st.markdown(f"**{name}**")
            st.dataframe(df)

        st.subheader("📄 Cash Flow Statement (10-K)")
        cashflow = build_cashflow_statement(xbrl, extract_series)
        for name, df in cashflow.items():
            st.markdown(f"**{name}**")
            st.dataframe(df)

        st.subheader("📄 Balance Sheet (10-K)")
        balance = build_balance_sheet(xbrl, extract_series)
        for name, df in balance.items():
            st.markdown(f"**{name}**")
            st.dataframe(df)


        # ---------------------------------------------
        # TAB 2 — RAW FINANCIAL STATEMENTS
        # ---------------------------------------------
        with tabs[1]:
            st.subheader("Income Statement (10-K)")
            st.write(build_income_statement(xbrl, extract_series))

            st.subheader("Cash Flow Statement (10-K)")
            st.write(build_cashflow_statement(xbrl, extract_series))

            st.subheader("Balance Sheet (10-K)")
            st.write(build_balance_sheet(xbrl, extract_series))

        # ---------------------------------------------
        # TAB 3 — VALIDATION & ASSUMPTIONS
        # ---------------------------------------------
        with tabs[2]:
            feasible, assumptions, warnings = validate_for_fcff(
                xbrl, extract_series
            )

            st.write("### FCFF Feasibility")
            st.write("✔ Suitable for FCFF valuation" if feasible else "❌ Not suitable")

            if assumptions:
                st.warning("**Assumptions Used:**")
                for a in assumptions:
                    st.write(f"- {a}")

            if warnings:
                st.info("**Warnings:**")
                for w in warnings:
                    st.write(f"- {w}")

        # ---------------------------------------------
        # TAB 4 — FCFF
        # ---------------------------------------------
        fcff_df = None

        with tabs[3]:
            fcff_df, err = compute_fcff(xbrl, extract_series)

            if err:
                st.error(f"❌ FCFF computation failed: {err}")
            else:
                st.subheader("📘 FCFF (Latest 10-K Year)")
                st.dataframe(fcff_df)

                st.warning(
                    "⚠️ FCFF is computed using the **latest 10-K year only**. "
                    "This is standard and academically correct. "
                    "DCF valuation is forward-looking."
                )

        # ---------------------------------------------
        # TAB 5 — VALUATION (DEFENSIVE)
        # ---------------------------------------------
        with tabs[4]:
            if fcff_df is None or fcff_df.empty:
                st.warning(
                    "⚠️ Valuation cannot proceed because FCFF is unavailable. "
                    "Please review the Financial Statements and Validation tabs."
                )
                st.stop()

            # SAFE TO PROCEED
            fcff = fcff_df["FCFF"].iloc[0]

            # Capital structure
            shares = get_share_count(xbrl)
            net_debt = get_net_debt(xbrl, extract_series)

            # WACC
            wacc = calculate_wacc(ticker)["WACC"]

            # Valuation
            ev, equity, price = equity_value_from_fcff(
                fcff=fcff,
                wacc=wacc,
                g=0.04,
                net_debt=net_debt,
                shares=shares
            )

            col1, col2, col3 = st.columns(3)

            col1.metric("Enterprise Value", f"${ev:,.0f}")
            col2.metric("Equity Value", f"${equity:,.0f}")
            col3.metric("Fair Value per Share", f"${price:,.2f}")

            # Monte Carlo
            st.subheader("📈 Monte Carlo DCF (Terminal Value Distribution)")
            mc = monte_carlo_dcf(fcff, wacc, 0.04)
            st.line_chart(mc[:300])

    except Exception as e:
        st.exception(e)
