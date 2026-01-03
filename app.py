
import streamlit as st
from core.sec_data import *
from core.fcff import *
from core.wacc import *
from core.dcf import *
from core.monte_carlo import *
from core.sensitivity import *

st.set_page_config(page_title="FCFF–DCF Valuation", layout="wide")
st.title("📊 FCFF–DCF Valuation Platform (10-K Based)")

# ✅ USER GUIDANCE (ADD THIS BLOCK)
st.info(
    "ℹ️ **Important Note**: Some companies (banks, insurers, NBFCs, "
    "and recent IPOs) do not report Working Capital consistently in SEC XBRL. "
    "For such firms, **FCFF cannot be reliably computed**, and the model "
    "will gracefully stop with an explanation."
)

# USER INPUT
ticker = st.text_input("Enter US Ticker", "AAPL")

# ACTION
if st.button("Run Valuation"):

    try:
        cik = get_cik_from_ticker(ticker)
        xbrl = get_company_xbrl(cik)

        fcff_df, error = compute_fcff(xbrl, extract_series)

        if error:
            st.error(f"❌ FCFF computation failed: {error}")
            st.stop()

        if fcff_df.empty:
            st.warning("⚠️ FCFF data unavailable for this company.")
            st.stop()

        # DISPLAY FCFF
        st.subheader("📘 FCFF (Last 5 Years)")
        st.dataframe(fcff_df)

        fcff_last = fcff_df["FCFF"].iloc[-1]

        # WACC
        wacc_data = calculate_wacc(ticker)
        st.metric("WACC", f"{wacc_data['WACC']:.2%}")

        # MONTE CARLO
        mc_values = monte_carlo_dcf(
            fcff_last=fcff_last,
            wacc_mean=wacc_data["WACC"],
            g_mean=0.04
        )

        st.subheader("📈 Monte Carlo DCF (Terminal Value Distribution)")
        st.line_chart(mc_values[:500])

    except Exception as e:
        st.exception(e)
