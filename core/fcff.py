
def compute_fcff(xbrl, extract):

    tag_map = {
        "EBIT": ["OperatingIncomeLoss"],
        "PBT": [
            "IncomeBeforeTax",
            "IncomeLossFromContinuingOperationsBeforeIncomeTaxes"
        ],
        "Tax": ["IncomeTaxExpenseBenefit"],
        "Dep": ["DepreciationAndAmortization"],
        "CapEx": ["PaymentsToAcquirePropertyPlantAndEquipment"],
        "ΔWC": ["IncreaseDecreaseInOperatingAssets"]
    }

    dfs = {}

    for col, tags in tag_map.items():
        df = extract(xbrl, tags, col)
        if df.empty:
            return None, f"Missing XBRL tag(s): {', '.join(tags)}"
        dfs[col] = df

    df_final = dfs["EBIT"]
    for key in ["PBT", "Tax", "Dep", "CapEx", "ΔWC"]:
        df_final = df_final.merge(dfs[key], on="Year", how="inner")

    if df_final.empty:
        return None, "No overlapping 10-K years across statements"

    df_final["TaxRate"] = df_final["Tax"] / df_final["PBT"]
    df_final["FCFF"] = (
        df_final["EBIT"] * (1 - df_final["TaxRate"])
        + df_final["Dep"]
        - df_final["CapEx"]
        - df_final["ΔWC"]
    )

    return df_final.sort_values("Year").reset_index(drop=True), None
