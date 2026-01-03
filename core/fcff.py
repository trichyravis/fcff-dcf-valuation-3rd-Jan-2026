
def compute_fcff(xbrl, extract):
    tags = {
        "EBIT": "OperatingIncomeLoss",
        "PBT": "IncomeBeforeTax",
        "Tax": "IncomeTaxExpenseBenefit",
        "Dep": "DepreciationAndAmortization",
        "CapEx": "PaymentsToAcquirePropertyPlantAndEquipment",
        "ΔWC": "IncreaseDecreaseInOperatingAssets"
    }

    dfs = []

    for col, tag in tags.items():
        df = extract(xbrl, tag, col)
        if df.empty:
            return None, f"Missing XBRL tag: {tag}"
        dfs.append(df)

    df_final = dfs[0]
    for d in dfs[1:]:
        df_final = df_final.merge(d, on="Year", how="inner")

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
