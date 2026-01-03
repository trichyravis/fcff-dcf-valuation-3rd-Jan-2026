
def equity_value_from_fcff(fcff, wacc, g, net_debt, shares):
    ev = (fcff * (1 + g)) / (wacc - g)
    equity = ev - net_debt
    price = equity / shares
    return ev, equity, price
