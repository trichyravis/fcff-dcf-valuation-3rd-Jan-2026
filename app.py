
import streamlit as st

from core.sec_data import get_cik_from_ticker, get_company_xbrl, extract_series
from core.fcff import compute_fcff
from core.wacc import calculate_wacc
from core.monte_carlo import monte_carlo_dcf
from core.equity import get_share_count
from core.net_debt import get_net_debt

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="FCFF–DCF Valuation Platform",
    layout="wide"
)

st.title("📊 FCFF–DCF Valuation Platform (10-K Based)")

# -------------------------------------------------
# USER GUIDANCE
# -------------------------------------------------
st.info(
    "ℹ️ **Important**: SEC 10-K filings typically allow computation of "
    "**only one clean FCFF year**. DCF valuation is forward-looking and "
    "relies on assumptions, not historical FCFF time series. "
    "Banks, insurers, and some NBFCs are not suitable for FCFF valuation."
)

# -------------------------------------------------
# USER INPUT
# -------------------------------------------------
ticker = st.text_input("Enter US Ticker", "AAPL")

# -------------------------------------------------
# MAIN ACTION
# -------------------------------------------------
if st.button("Run Valuation"):

    try:
        # ---------------------------------------------
        # FETCH SEC DATA
        # ---------------------------------------------
        cik = get_cik_from_ticker(ticker)
        xbrl = get_company_xbrl(cik)

        # ---------------------------------------------
        # FCFF COMPUTATION
        # ---------------------------------------------
        fcff_df, error = compute_fcff(xbrl, extract_series)

        if error:
            st.error(f"❌ FCFF computation failed: {error}")
            st.stop()

        st.subheader("📘 FCFF (Latest 10-K Year)")
        st.dataframe(fcff_df)

        if len(fcff_df) == 1:
            st.warning(
                "⚠️ FCFF computed using only the latest 10-K year. "
                "This is normal and academically correct. "
                "DCF valuation is forward-looking."
            )

        # ---------------------------------------------
        # EQUITY & CAPITAL STRUCTURE
        # ---------------------------------------------
        shares = get_share_count(xbrl)
        net_debt = get_net_debt(xbrl, extract_series)

        col1, col2 = st.columns(2)

        col1.metric(
            "Diluted Shares Outstanding",
            f"{shares:,}"
        )

        col2.metric(
            "Net Debt (Debt – Cash)",
            f"${net_debt:,.0f}"
        )

        # ---------------------------------------------
        # WACC (CAPM-BASED)
        # ---------------------------------------------
        wacc_data = calculate_wacc(ticker)

        st.metric(
            "WACC (CAPM-Based)",
            f"{wacc_data['WACC']:.2%}"
        )

        # ---------------------------------------------
        # MONTE CARLO DCF (TERMINAL VALUE DISTRIBUTION)
        # ---------------------------------------------
        fcff_last = fcff_df["FCFF"].iloc[-1]

        mc_values = monte_carlo_dcf(
            fcff_last=fcff_last,
            wacc_mean=wacc_data["WACC"],
            g_mean=0.04
        )

        st.subheader("📈 Monte Carlo DCF – Terminal Value Distribution")
        st.line_chart(mc_values[:500])

    except Exception as e:
        st.exception(e)
