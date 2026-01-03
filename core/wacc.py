import yfinance as yf
import numpy as np

def calculate_wacc(ticker, rf=0.04, erp=0.055, tax_rate=0.25):
    stock = yf.Ticker(ticker)
    beta = stock.info.get("beta", 1.0)

    cost_of_equity = rf + beta * erp

    market_cap = stock.info.get("marketCap", 0)
    debt = stock.balance_sheet.loc["Total Debt"].iloc[0] if "Total Debt" in stock.balance_sheet.index else 0

    total = market_cap + debt
    we = market_cap / total if total else 1
    wd = debt / total if total else 0

    cost_of_debt = 0.05  # conservative assumption

    wacc = we*cost_of_equity + wd*cost_of_debt*(1-tax_rate)

    return {
        "Beta": beta,
        "CostOfEquity": cost_of_equity,
        "WACC": wacc
    }

