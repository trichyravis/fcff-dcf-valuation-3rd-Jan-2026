
def get_net_debt(xbrl, extract):

    debt = extract(xbrl, ["LongTermDebt"], "Debt")
    cash = extract(
        xbrl,
        ["CashAndCashEquivalentsAtCarryingValue"],
        "Cash"
    )

    d = debt["Debt"].iloc[-1] if not debt.empty else 0
    c = cash["Cash"].iloc[-1] if not cash.empty else 0

    return d - c
