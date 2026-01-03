
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
    # REQUIRED FOR FCFF (ΔWC REMOVED HERE)
    # -------------------------------
    required = ["EBIT", "PBT", "Tax", "Dep", "CapEx"]

    for r in required:
        if r not in dfs:
            return None, f"Missing XBRL tag(s) required for FCFF: {r}"

    # -------------------------------
    # ΔWC FALLBACK LOGIC (⬅️ THIS IS THE KEY ADDITION)
    # -------------------------------
    if "ΔWC" not in dfs:
        try:
            # Compute ΔWC from Balance Sheet
            ca = extract(xbrl, ["AssetsCurrent"], "CA")
            cl = extract(xbrl, ["LiabilitiesCurrent"], "CL")
            cash = extract(
                xbrl,
                ["CashAndCashEquivalentsAtCarryingValue"],
                "Cash"
            )

            if not ca.empty and not cl.empty:
                wc = ca.merge(cl, on="Year", how="inner")

                if not cash.empty:
                    wc = wc.merge(cash, on="Year", how="left")
                    wc["Cash"] = wc["Cash"].fillna(0)
                else:
                    wc["Cash"] = 0

                wc["NWC"] = (wc["CA"] - wc["Cash"]) - wc["CL"]
                wc["ΔWC"] = wc["NWC"].diff()

                dfs["ΔWC"] = wc[["Year", "ΔWC"]].dropna()
            else:
                raise Exception("Balance sheet WC unavailable")

        except:
            # Final conservative fallback
            years = dfs["EBIT"]["Year"]
            dfs["ΔWC"] = pd.DataFrame({
                "Year": years,
                "ΔWC": [0] * len(years)
            })

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
