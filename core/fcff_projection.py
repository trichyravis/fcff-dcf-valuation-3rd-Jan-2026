def project_fcff(
    base_revenue,
    operating_margin,
    tax_rate,
    growth_rates,
    sales_to_capital
):
    projections = []
    prev_revenue = base_revenue

    for year, g in enumerate(growth_rates, start=1):
        revenue = prev_revenue * (1 + g)
        ebit = revenue * operating_margin
        nopat = ebit * (1 - tax_rate)

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

