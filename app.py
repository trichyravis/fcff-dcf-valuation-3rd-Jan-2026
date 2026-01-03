
import streamlit as st
import pandas as pd

from core.sec_data import get_cik_from_ticker, get_company_xbrl, extract_series
from core.base_year import get_base_year_operating_data
from core.fcff_projection import project_fcff
from core.dcf import dcf_valuation
from core.wacc import calculate_wacc
from core.net_debt import get_net_debt
from core.equity import get_share_count


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="FCFF–DCF Valuation Platform (10-K Based)",
    layout="wide"
)

st.title("📊 FCFF–DCF Valuation Platform (10-K Based)")

st.info(
    "Professional workflow: extract base-year operating economics from the latest SEC 10-K, "
    "project FCFF using reinvestment discipline, evaluate ROIC vs WACC, and perform intrinsic valuation."
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
        # SEC DATA
        # ---------------------------------------------
        cik = get_cik_from_ticker(ticker)
        xbrl = get_company_xbrl(cik)

        # ---------------------------------------------
        # BASE-YEAR ECONOMICS
        # ---------------------------------------------
        base = get_base_year_operating_data(xbrl, extract_series)

        st.subheader("📘 Base-Year Operating Economics (Latest 10-K)")

        c1, c2, c3 = st.columns(3)
        c1.metric("Revenue ($bn)", f"{base['revenue']/1e9:,.1f}")
        c2.metric("Operating Margin", f"{base['operating_margin']:.1%}")
        c3.metric("Effective Tax Rate", f"{base['tax_rate']:.1%}")

        # ---------------------------------------------
        # ASSUMPTIONS
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
            "Sales-to-Capital Ratio (Capital Efficiency)",
            min_value=1.0,
            max_value=6.0,
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
        df_fcff["Revenue ($bn)"] = df_fcff["Revenue"] / 1e9
        df_fcff["Reinvestment ($bn)"] = df_fcff["Reinvestment"] / 1e9

        st.subheader("📗 FCFF Forecast (Base Year + Explicit Period)")
        st.dataframe(
            df_fcff[
                ["Year", "Revenue ($bn)", "Reinvestment ($bn)", "FCFF ($bn)"]
            ],
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
        # ROIC VS WACC DIAGNOSTIC
        # ---------------------------------------------
        roic = base["operating_margin"] * (1 - base["tax_rate"]) * sales_to_capital

        st.subheader("🧮 Growth Economics Diagnostic")

        c1, c2 = st.columns(2)
        c1.metric("Implied ROIC", f"{roic:.1%}")
        c2.metric("WACC", f"{wacc:.1%}")

        if roic < wacc:
            st.error(
                "Growth is value destructive (ROIC < WACC). "
                "Negative FCFF during high-growth years is economically expected."
            )
        else:
            st.success(
                "Growth creates value (ROIC > WACC). "
                "FCFF will turn positive as reinvestment moderates."
            )

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
        # EQUITY VALUE
        # ---------------------------------------------
        net_debt = get_net_debt(xbrl, extract_series)
        shares = get_share_count(xbrl)

        equity_value = enterprise_value - net_debt
        fair_value = equity_value / shares if shares > 0 else None

        st.subheader("📈 Valuation Summary")

        c1, c2, c3 = st.columns(3)
        c1.metric("Enterprise Value ($bn)", f"{enterprise_value/1e9:,.0f}")
        c2.metric("Equity Value ($bn)", f"{equity_value/1e9:,.0f}")
        c3.metric(
            "Fair Value per Share",
            f"${fair_value:,.2f}" if fair_value else "N/A"
        )

        # ---------------------------------------------
        # EDUCATIONAL NOTES
        # ---------------------------------------------
        st.info(
            "Interpretation Notes:\n"
            "- FCFF = NOPAT − Reinvestment.\n"
            "- High growth requires heavy reinvestment, often causing negative FCFF.\n"
            "- Value is created only when ROIC exceeds WACC.\n"
            "- Terminal value drives most of intrinsic valuation."
        )

    except Exception as e:
        st.exception(e)
