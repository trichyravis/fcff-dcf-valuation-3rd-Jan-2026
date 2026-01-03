def get_net_debt(xbrl, extract):
    """
    Net Debt = Debt – Cash
    """

    debt_tags = [
        "LongTermDebt",
        "LongTermDebtCurrent"
    ]

    cash_tags = [
        "CashAndCashEquivalentsAtCarryingValue",
        "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"
    ]

    debt = 0
    cash = 0

    for tag in debt_tags:
        try:
            debt += extract(xbrl, [tag], "Debt")["Debt"].iloc[-1]
        except:
            pass

    for tag in cash_tags:
        try:
            cash += extract(xbrl, [tag], "Cash")["Cash"].iloc[-1]
        except:
            pass

    return debt - cash

