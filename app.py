
import streamlit as st
from core.sec_data import *
from core.fcff import *
from core.wacc import *
from core.dcf import *
from core.monte_carlo import *
from core.sensitivity import *

st.title("📊 FCFF–DCF Valuation Platform")

ticker = st.text_input("Ticker", "AAPL")

if st.button("Run Valuation"):
    cik = get_cik_from_ticker(ticker)
    xbrl = get_company_xbrl(cik)

    fcff_df = compute_fcff(xbrl, extract_series)
    st.subheader("FCFF (5 Years)")
    st.dataframe(fcff_df)

    wacc_data = calculate_wacc(ticker)
    st.metric("WACC", f"{wacc_data['WACC']:.2%}")

    fcff_last = fcff_df["FCFF"].iloc[-1]
    mc = monte_carlo_dcf(fcff_last, wacc_data["WACC"], 0.04)
    st.subheader("Monte Carlo DCF (Distribution)")
    st.line_chart(mc[:500])
