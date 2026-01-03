
import pandas as pd
from functools import reduce

def compute_fcff(xbrl, extract):
    """
    Compute FCFF from a single SEC 10-K.
    Accepts ONE usable FCFF year (correct finance logic).
    Returns: (df, error_message or None)
    """

    tag_map = {
        "EBIT": ["OperatingIncomeLoss"],
        "PBT": [
            "IncomeBeforeTax",
            "IncomeLossFromContinuingOperationsBeforeIncomeTaxes"
        ],
        "NetIncome": ["NetIncomeLoss", "ProfitLoss"],
        "Tax": ["IncomeTaxExpenseBenefit"],
        "Dep": ["DepreciationAndAmortization"],
        "CapEx": ["PaymentsToAcquirePropertyPlantAndEquipment"],
        "ΔWC": ["IncreaseDecreaseInOperatingAssets"]
    }

    dfs = {}

    # Extract available series
    for col, tags in tag_map.items():
        df = extract(xbrl, tags, col)
        if not df.empty:
            dfs[col] = df

    # Reconstruct PBT if missing
    if "PBT" not in dfs:
        if "NetIncome" in dfs and "Tax" in dfs:
            pbt = dfs["NetIncome"].merge(dfs["Tax"], on="Year", how="outer")
            pbt["PBT"] = pbt["NetIncome"] + pbt["Tax"]
            dfs["PBT"] = pbt[["Year", "PBT"]]
        else:
            return None, "Pre-tax income unavailable (cannot reconstruct)"

    # Required inputs
    for r in ["EBIT", "PBT", "Tax", "Dep", "CapEx"]:
        if r not in dfs:
            return None, f"Missing XBRL tag required for FCFF: {r}"

    # ΔWC fallback
    if "ΔWC" not in dfs:
        years = dfs["EBIT"]["Year"]
        dfs["ΔWC"] = pd.DataFrame({
            "Year": years,
            "ΔWC": [0] * len(years)
        })

    # Align data
    df_list = [
        dfs["EBIT"],
        dfs["PBT"],
        dfs["Tax"],
        dfs["Dep"],
        dfs["CapEx"],
        dfs["ΔWC"]
    ]

    df_final = reduce(
        lambda l, r: l.merge(r, on="Year", how="outer"),
        df_list
    ).sort_values("Year")

    df_final = df_final.dropna(
        subset=["EBIT", "PBT", "Tax", "Dep", "CapEx"]
    )

    # Keep latest year only (10-K reality)
    df_final = df_final.tail(1)

    if df_final.empty:
        return None, "Unable to compute FCFF from 10-K data"

    # FCFF calculation
    df_final["TaxRate"] = (df_final["Tax"] / df_final["PBT"]).clip(0, 0.35)

    df_final["FCFF"] = (
        df_final["EBIT"] * (1 - df_final["TaxRate"])
        + df_final["Dep"]
        - df_final["CapEx"]
        - df_final["ΔWC"]
    )

    return df_final.reset_index(drop=True), None
