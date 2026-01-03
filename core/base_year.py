
def get_base_year_operating_data(xbrl, extract):

    revenue_df = extract(
        xbrl,
        ["Revenues"],
        "Revenue"
    )

    ebit_df = extract(
        xbrl,
        ["OperatingIncomeLoss"],
        "EBIT"
    )

    if revenue_df.empty or ebit_df.empty:
        raise ValueError("Base-year Revenue or EBIT not available from 10-K")

    revenue = revenue_df.iloc[0]["Revenue"]
    ebit = ebit_df.iloc[0]["EBIT"]

    tax_df = extract(
        xbrl,
        ["IncomeTaxExpenseBenefit"],
        "Tax"
    )

    pretax_df = extract(
        xbrl,
        [
            "IncomeLossFromContinuingOperationsBeforeIncomeTaxes",
            "IncomeBeforeTax"
        ],
        "PretaxIncome"
    )

    if not tax_df.empty and not pretax_df.empty:
        tax_rate = tax_df.iloc[0]["Tax"] / pretax_df.iloc[0]["PretaxIncome"]
        tax_rate = min(max(tax_rate, 0.15), 0.30)
    else:
        tax_rate = 0.21

    operating_margin = ebit / revenue
    nopat = ebit * (1 - tax_rate)

    return {
        "revenue": revenue,
        "ebit": ebit,
        "nopat": nopat,
        "operating_margin": operating_margin,
        "tax_rate": tax_rate
    }
