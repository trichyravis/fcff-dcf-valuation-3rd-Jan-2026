
import streamlit as st

from core.sec_data import *
from core.statements import *
from core.validate import validate_for_fcff
from core.fcff import compute_fcff
from core.wacc import calculate_wacc
from core.equity import get_share_count
from core.net_debt import get_net_debt
from core.dcf import equity_value_from_fcff
from core.monte_carlo import monte_carlo_dcf

st.set_page_config(page_title="10-K Valuation Platform", layout="wide")
st.title("📊 10-K Based Valuation Platform")

ticker = st.text_input("US Ticker", "AAPL")

if st.button("Load 10-K Data"):

    cik = get_cik_from_ticker(ticker)
    xbrl = get_company_xbrl(cik)

    tabs = st.tabs([
        "📥 Downloaded Data",
        "📄 Financial Statements",
        "🧠 Validation",
        "📘 FCFF",
        "📈 Valuation"
    ])

    with tabs[0]:
        st.json({"Ticker": ticker, "CIK": cik})

    with tabs[1]:
        st.subheader("Income Statement")
        st.write(build_income_statement(xbrl, extract_series))

        st.subheader("Cash Flow Statement")
        st.write(build_cashflow_statement(xbrl, extract_series))

        st.subheader("Balance Sheet")
        st.write(build_balance_sheet(xbrl, extract_series))

    with tabs[2]:
        ok, assumptions, warnings = validate_for_fcff(xbrl, extract_series)
        st.write("FCFF Feasible:", ok)
        st.write("Assumptions:", assumptions)
        st.write("Warnings:", warnings)

    with tabs[3]:
        fcff_df, err = compute_fcff(xbrl, extract_series)
        if err:
            st.error(err)
        else:
            st.dataframe(fcff_df)

    with tabs[4]:
        fcff = fcff_df["FCFF"].iloc[0]
        wacc = calculate_wacc(ticker)["WACC"]
        shares = get_share_count(xbrl)
        net_debt = get_net_debt(xbrl, extract_series)

        ev, eq, price = equity_value_from_fcff(
            fcff, wacc, 0.04, net_debt, shares
        )

        st.metric("Enterprise Value", f"${ev:,.0f}")
        st.metric("Equity Value", f"${eq:,.0f}")
        st.metric("Fair Value per Share", f"${price:,.2f}")

        mc = monte_carlo_dcf(fcff, wacc, 0.04)
        st.line_chart(mc[:300])
