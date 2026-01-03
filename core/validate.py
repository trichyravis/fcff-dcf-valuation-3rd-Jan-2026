
def validate_for_fcff(xbrl, extract):
    assumptions = []
    warnings = []

    ebit = extract(xbrl, ["OperatingIncomeLoss"], "EBIT")
    if ebit.empty:
        return False, ["EBIT missing"], []

    wc = extract(xbrl, ["IncreaseDecreaseInOperatingAssets"], "ΔWC")
    if wc.empty:
        assumptions.append("ΔWC not reported; assumed 0")

    warnings.append("Only one FCFF year available from 10-K")

    return True, assumptions, warnings
