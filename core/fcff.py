def compute_fcff(xbrl, extract):
    ebit = extract(xbrl, "OperatingIncomeLoss", "EBIT")
    pbt  = extract(xbrl, "IncomeBeforeTax", "PBT")
    tax  = extract(xbrl, "IncomeTaxExpenseBenefit", "Tax")
    dep  = extract(xbrl, "DepreciationAndAmortization", "Dep")
    cap  = extract(xbrl, "PaymentsToAcquirePropertyPlantAndEquipment", "CapEx")
    wc   = extract(xbrl, "IncreaseDecreaseInOperatingAssets", "ΔWC")

    df = ebit.merge(pbt, on="Year").merge(tax, on="Year")
    df = df.merge(dep, on="Year").merge(cap, on="Year").merge(wc, on="Year")

    df["TaxRate"] = df["Tax"] / df["PBT"]
    df["FCFF"] = df["EBIT"]*(1-df["TaxRate"]) + df["Dep"] - df["CapEx"] - df["ΔWC"]
    return df

