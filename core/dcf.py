
def dcf_valuation(fcff_projection, wacc, terminal_growth):

    pv_fcff = []
    for i, row in enumerate(fcff_projection, start=1):
        pv_fcff.append(row["FCFF"] / (1 + wacc) ** i)

    terminal_fcff = fcff_projection[-1]["FCFF"] * (1 + terminal_growth)
    terminal_value = terminal_fcff / (wacc - terminal_growth)
    pv_terminal = terminal_value / (1 + wacc) ** len(fcff_projection)

    enterprise_value = sum(pv_fcff) + pv_terminal

    return {
        "enterprise_value": enterprise_value,
        "pv_fcff": pv_fcff,
        "pv_terminal": pv_terminal
    }
