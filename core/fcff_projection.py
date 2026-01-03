
def project_fcff(
    base_revenue,
    operating_margin,
    tax_rate,
    growth_rates,
    sales_to_capital
):
    """
    Projects FCFF using base-year operating economics and explicit reinvestment.

    Year 0 : Base year (from latest 10-K)
    Year 1+: Explicit forecast years

    Parameters
    ----------
    base_revenue : float
        Revenue from the latest 10-K (base year)
    operating_margin : float
        EBIT / Revenue
    tax_rate : float
        Effective corporate tax rate
    growth_rates : list[float]
        Revenue growth assumptions for explicit forecast period
    sales_to_capital : float
        Revenue generated per unit of invested capital

    Returns
    -------
    list[dict]
        FCFF projection including Year 0 and forecast years
    """

    projections = []

    # -------------------------------------------------
    # YEAR 0 — BASE YEAR (NO REINVESTMENT)
    # -------------------------------------------------
    ebit_0 = base_revenue * operating_margin
    nopat_0 = ebit_0 * (1 - tax_rate)

    projections.append({
        "Year": 0,
        "Revenue": base_revenue,
        "NOPAT": nopat_0,
        "Reinvestment": 0.0,
        "FCFF": nopat_0
    })

    prev_revenue = base_revenue

    # -------------------------------------------------
    # EXPLICIT FORECAST YEARS (1..N)
    # -------------------------------------------------
    for year, g in enumerate(growth_rates, start=1):
        revenue = prev_revenue * (1 + g)

        ebit = revenue * operating_margin
        nopat = ebit * (1 - tax_rate)

        # Reinvestment needed to support revenue growth
        reinvestment = (revenue - prev_revenue) / sales_to_capital

        fcff = nopat - reinvestment

        projections.append({
            "Year": year,
            "Revenue": revenue,
            "NOPAT": nopat,
            "Reinvestment": reinvestment,
            "FCFF": fcff
        })

        prev_revenue = revenue

    return projections
