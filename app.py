
import streamlit as st
import pandas as pd

from core.sec_data import (
    get_cik_from_ticker,
    get_company_xbrl,
    extract_series
)
from core.base_year import get_base_year_operating_data
from core.fcff_projection import project_fcff
from core.dcf import dcf_valuation
from core.net_debt import get_net_debt
from core.equity import get_share_count
from core.wacc import calculate_wacc


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="FCFF–DCF Valuation Platform",
    layout="wide"
)

st.title("📊 FCFF–DCF Valuation Platform (10-K Based)")

st.info(
    "This platform performs intrinsic valuation using Free Cash Flow to the Firm (FCFF). "
    "Base-year operating data is extracted from the latest SEC 10-K, while future cash "
    "flows are projected using explicit growth and reinvestment logic."
)

# -------------------------------------------------
# USER INPUT
# -------------------------------------------------
ticker = st.text_input("Enter US Ticker", "AAPL").upper()

# -------------------------------------------------
# RUN VALUATION
# -------------------------------------------------
if st.button("Run Valuation"):

    try:
        # ---------------------------------------------
        # FETCH SEC DATA
        # ---------------------------------------------
        cik = get_cik_from_ticker(ticker)
        xbrl = get_company_xbrl(cik)

        # ---------------------------------------------
        # BASE-YEAR OPERATING ECONOMICS
        # ---------------------------------------------
        base = get_base_year_operating_data(
            xbrl,
            extract_series
        )

        st.subheader("📘 Base-Year Operating Economics (Latest 10-K)")
        c1, c2, c3 = st.columns(3)
        c1.metric("Revenue ($bn)", f"{base['revenue']/1e9:,.1f}")
        c2.metric("Operating Margin", f"{base['operating_margin']:.1%}")
        c3.metric("Tax Rate", f"{base['tax_rate']:.1%}")

        # ---------------------------------------------
        # USER ASSUMPTIONS
        # ---------------------------------------------
        st.subheader("🧠 Growth & Reinvestment Assumptions")

        growth_rates = st.multiselect(
            "Revenue Growth Assumptions (Next 5 Years)",
            [0.04, 0.06, 0.08, 0.10, 0.12, 0.15],
            default=[0.10, 0.10, 0.10, 0.08, 0.08]
        )

        if len(growth_rates) != 5:
            st.warning("Please select exactly 5 growth rates.")
            st.stop()

        sales_to_capital = st.slider(
            "Sales-to-Capital Ratio",
            min_value=1.0,
            max_value=5.0,
            value=2.5,
            step=0.1
        )

        terminal_growth = st.slider(
            "Terminal Growth Rate",
            min_value=0.02,
            max_value=0.04,
            value=0.03,
            step=0.005
        )

        # ---------------------------------------------
        # FCFF PROJECTION
        # ---------------------------------------------
        projections = project_fcff(
            base_revenue=base["revenue"],
            operating_margin=base["operating_margin"],
            tax_rate=base["tax_rate"],
            growth_rates=growth_rates,
            sales_to_capital=sales_to_capital
        )

        df_fcff = pd.DataFrame(projections)
        df_fcff["FCFF ($bn)"] = df_fcff["FCFF"] / 1e9

        st.subheader("📗 FCFF Forecast (Explicit Period)")
        st.dataframe(
            df_fcff[["Year", "Revenue", "Reinvestment", "FCFF ($bn)"]],
            use_container_width=True
        )

        # ---------------------------------------------
        # COST OF CAPITAL
        # ---------------------------------------------
        wacc_data = calculate_wacc(ticker)
        wacc = wacc_data["WACC"]

        st.subheader("📐 Cost of Capital")
        st.metric("WACC (CAPM-Based)", f"{wacc:.2%}")

        # ---------------------------------------------
        # DCF VALUATION
        # ---------------------------------------------
        valuation = dcf_valuation(
            fcff_projection=projections,
            wacc=wacc,
            terminal_growth=terminal_growth
        )

        enterprise_value = valuation["enterprise_value"]

        # ---------------------------------------------
        # CAPITAL STRUCTURE
        # ---------------------------------------------
        net_debt = get_net_debt(xbrl, extract_series)
        shares = get_share_count(xbrl)

        equity_value = enterprise_value - net_debt
        fair_value = equity_value / shares if shares > 0 else None

        st.subheader("📈 Valuation Summary")

        c1, c2, c3 = st.columns(3)
        c1.metric("Enterprise Value ($bn)", f"{enterprise_value/1e9:,.0f}")
        c2.metric("Equity Value ($bn)", f"{equity_value/1e9:,.0f}")

        if fair_value:
            c3.metric("Fair Value per Share", f"${fair_value:,.2f}")
        else:
            c3.metric("Fair Value per Share", "N/A")

        # ---------------------------------------------
        # NOTES
        # ---------------------------------------------
        st.info(
            "Notes:\n"
            "- FCFF is derived from base-year operating economics.\n"
            "- Growth is supported by explicit reinvestment (sales-to-capital).\n"
            "- Terminal growth is constrained to long-term economic limits."
        )

    except Exception as e:
        st.exception(e)
