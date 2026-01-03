
import pandas as pd

def compute_fcff(xbrl, extract):

    ebit = extract(xbrl, ["OperatingIncomeLoss"], "EBIT")
    tax = extract(xbrl, ["IncomeTaxExpenseBenefit"], "Tax")
    dep = extract(xbrl, ["DepreciationAndAmortization"], "Dep")
    capex = extract(
        xbrl, ["PaymentsToAcquirePropertyPlantAndEquipment"], "CapEx"
    )

    if ebit.empty or tax.empty or dep.empty or capex.empty:
        return None, "Missing required data for FCFF"

    df = ebit.merge(tax, on="Year").merge(dep, on="Year").merge(capex, on="Year")
    df = df.tail(1)

    tax_rate = (df["Tax"] / df["EBIT"]).clip(0, 0.35)

    df["FCFF"] = (
        df["EBIT"] * (1 - tax_rate)
        + df["Dep"]
        - df["CapEx"]
    )

    return df[["Year", "FCFF"]], None
