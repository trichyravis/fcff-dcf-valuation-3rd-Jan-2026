
def compute_fcff(xbrl, extract):

    # -------------------------------
    # TAG MAP WITH REAL-WORLD FALLBACKS
    # -------------------------------
    tag_map = {
        "EBIT": ["OperatingIncomeLoss"],
        "PBT": [
            "IncomeBeforeTax",
            "IncomeLossFromContinuingOperationsBeforeIncomeTaxes"
        ],
        "NetIncome": [
            "NetIncomeLoss",
            "ProfitLoss"
        ],
        "Tax": ["IncomeTaxExpenseBenefit"],
        "Dep": ["DepreciationAndAmortization"],
        "CapEx": ["PaymentsToAcquirePropertyPlantAndEquipment"],
        "ΔWC": ["IncreaseDecreaseInOperatingAssets"]
    }

    dfs = {}

    # -------------------------------
    # EXTRACT WHAT WE CAN
    # -------------------------------
    for col, tags in tag_map.items():
        df = extract(xbrl, tags, col)
        if not df.empty:
            dfs[col] = df

    # -------------------------------
    # RECONSTRUCT PBT IF MISSING
    # -------------------------------
    if "PBT" not in dfs:
        if "NetIncome" in dfs and "Tax" in dfs:
            pbt = dfs["NetIncome"].merge(dfs["Tax"], on="Year", how="inner")
            pbt["PBT"] = pbt["NetIncome"] + pbt["Tax"]
            dfs["PBT"] = pbt[["Year", "PBT"]]
        else:
            return None, (
                "Pre-tax income not available and cannot be reconstructed "
                "(Net Income or Tax Expense missing)"
            )

    # -------------------------------
    # REQUIRED FOR FCFF
    # -------------------------------
    required = ["EBIT", "PBT", "Tax", "Dep", "CapEx", "ΔWC"]

    for r in required:
        if r not in dfs:
            return None, f"Missing XBRL tag(s) required for FCFF: {r}"

    # -------------------------------
    # MERGE ALL
    # -------------------------------
    df_final = dfs["EBIT"]
    for r in ["PBT", "Tax", "Dep", "CapEx", "ΔWC"]:
        df_final = df_final.merge(dfs[r], on="Year", how="inner")

    if df_final.empty:
        return None, "No overlapping 10-K years across financial statements"

    # -------------------------------
    # FCFF COMPUTATION
    # -------------------------------
    df_final["TaxRate"] = df_final["Tax"] / df_final["PBT"]
    df_final["TaxRate"] = df_final["TaxRate"].clip(lower=0, upper=0.35)

    df_final["FCFF"] = (
        df_final["EBIT"] * (1 - df_final["TaxRate"])
        + df_final["Dep"]
        - df_final["CapEx"]
        - df_final["ΔWC"]
    )

    return df_final.sort_values("Year").reset_index(drop=True), None
