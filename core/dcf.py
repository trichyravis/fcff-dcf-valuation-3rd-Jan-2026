
import numpy as np

def dcf_equity_value(fcff, wacc, g, net_debt, shares):
    n = len(fcff)
    years = np.arange(1, n+1)

    pv_fcff = np.sum(fcff / (1+wacc)**years)
    tv = fcff[-1]*(1+g)/(wacc-g)
    pv_tv = tv/(1+wacc)**n

    ev = pv_fcff + pv_tv
    equity = ev - net_debt
    price = equity / shares

    return {
        "EnterpriseValue": ev,
        "EquityValue": equity,
        "FairPrice": price
    }
