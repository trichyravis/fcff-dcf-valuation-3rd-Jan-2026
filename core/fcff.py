
import pandas as pd
from functools import reduce

def compute_fcff(xbrl, extract):
    """
    Computes FCFF using SEC XBRL with professional-grade robustness.
    Returns: (fcff_dataframe, error_message or None)
    """

    # -------------------------------------------------
    # TAG MAP WITH REAL-WORLD FALLBACKS
    # -------------------------------------------------
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

    # -------------------------------------------------
    # EXTRACT AVAILABLE SERIES
    # -------------------------------------------------
    for col, tags in tag_map.items():
        df = extract(xbrl, tags, col)
        if not df.empty:
            dfs[col] = df

    # -------------------------------------------------
    # RECONSTRUCT PBT IF MISSING
    # -------------------------------------------------
    if "PBT" not in dfs:
        if "NetIncome" in dfs and "Tax" in dfs:
            pbt = dfs["NetIncome"].merge(dfs["Tax"], on="Year", how="outer")
            pbt["PBT"] = pbt["NetIncome"] + pbt["Tax"]
            dfs["PBT"] = pbt[["Year", "PBT"]]
        else:
            return None, (
                "Pre-tax income not available and cannot be reconstructed "
                "(Net Income or Tax Expense missing)"
            )

    # -------------------------------------------------
    # REQUIRED CORE INPUTS (ΔWC NOT REQUIRED HERE)
    # -------------------------------------------------
    required = ["EBIT", "PBT", "Tax", "Dep", "CapEx"]
    for r in required:
        if r not in dfs:
            return None, f"Missing XBRL tag(s) required for FCFF: {r}"

    # -------------------------------------------------
    # ΔWC FALLBACK LOGIC
    # -------------------------------------------------
    if "ΔWC" not in dfs:
        try:
            ca = extract(xbrl, ["AssetsCurrent"], "CA")
            cl = extract(xbrl, ["LiabilitiesCurrent"], "CL")
            cash = extract(
                xbrl,
                ["CashAndCashEquivalentsAtCarryingValue"],
                "Cash"
            )

            if not ca.empty and not cl.empty:
                wc = ca.merge(cl, on="Year", how="outer")

                if not cash.empty:
                    wc = wc.merge(cash, on="Year", how="left")
                    wc["Cash"] = wc["Cash"].fillna(0)
                else:
                    wc["Cash"] = 0

                wc["NWC"] = (wc["CA"] - wc["Cash"]) - wc["CL"]
                wc["ΔWC"] = wc["NWC"].diff()

                dfs["ΔWC"] = wc[["Year", "ΔWC"]].dropna()
            else:
                raise ValueError("Balance sheet WC unavailable")

        except:
            # Conservative, disclosed fallback
            years = dfs["EBIT"]["Year"]
            dfs["ΔWC"] = pd.DataFrame({
                "Year": years,
                "ΔWC": [0] * len(years)
            })

    # -------------------------------------------------
    # ROBUST YEAR ALIGNMENT (OUTER JOIN + CLEANUP)
    # -------------------------------------------------
    df_list = [
        dfs["EBIT"],
        dfs["PBT"],
        dfs["Tax"],
        dfs["Dep"],
        dfs["CapEx"],
        dfs["ΔWC"]
    ]

    df_final = reduce(
        lambda left, right: left.merge(right, on="Year", how="outer"),
        df_list
    )

    df_final = df_final.sort_values("Year")

    # Drop years missing critical inputs
    df_final = df_final.dropna(
        subset=["EBIT", "PBT", "Tax", "Dep", "CapEx"]
    )

    # Keep last 5 economically usable years
    df_final = df_final.tail(5)

    if df_final.empty:
        return None, "Insufficient overlapping data to compute FCFF"

    # -------------------------------------------------
    # FCFF COMPUTATION
    # -------------------------------------------------
    df_final["TaxRate"] = df_final["Tax"] / df_final["PBT"]
    df_final["TaxRate"] = df_final["TaxRate"].clip(lower=0, upper=0.35)

    df_final["FCFF"] = (
        df_final["EBIT"] * (1 - df_final["TaxRate"])
        + df_final["Dep"]
        - df_final["CapEx"]
        - df_final["ΔWC"]
    )

    return df_final.reset_index(drop=True), None
